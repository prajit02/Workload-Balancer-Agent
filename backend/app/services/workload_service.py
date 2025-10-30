import os
import re
import json
import google.generativeai as genai
from collections import defaultdict

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash-lite")
# gemini-2.5-flash
# gemini-2.5-flash-lite
# gemini-2.0-flash-exp

def normalize_comments(comments):
    """
    Ensure comments is a list of strings.
    Because ado_client may pass a single cleaned string, we convert appropriately.
    """
    if isinstance(comments, list):
        texts = []
        for c in comments:
            if isinstance(c, dict):
                texts.append(c.get("text", ""))
            elif isinstance(c, str):
                texts.append(c)
            else:
                texts.append(str(c))
        return texts

    elif isinstance(comments, str):
        return [comments.strip()]

    return []


def analyze_single_workitem(workitem):
    """
    Analyze a single work item with Gemini based on its title + comments.
    Returns workload_score + reason + raw response.
    """
    title = workitem.get("fields", {}).get("System.Title", "Untitled")
    comments_raw = workitem.get("comments", [])
    comment_texts = normalize_comments(comments_raw)

    prompt = f"""
You are an AI assistant helping with workload evaluation on software teams.

You will receive:
- A work item title
- A list of user comments

Your job:
1. Determine how demanding the work seems based on complexity, blockers, rework, or urgency.
2. Assign a workload score from 1 (very light) to 10 (extremely heavy).
3. Provide a short reason in 1 sentence.

Return JSON with EXACTLY this structure (no markdown, no extra keys):

{{
  "score": <1-10 number>,
  "reason": "<short explanation>"
}}

Title: {title}

Comments:
{json.dumps(comment_texts, indent=2)}
"""

    try:
        response = model.generate_content(prompt)
        raw_text = getattr(response, "text", "").strip()

        # Try to parse JSON
        try:
            parsed = json.loads(raw_text)
            score = int(parsed.get("score", 0))
            reason = parsed.get("reason", "")
        except:
            match = re.search(r"\b([1-9]|10)\b", raw_text)
            score = int(match.group(1)) if match else 0
            reason = raw_text

        return {
            "score": score,
            "reason": reason,
            "raw": raw_text
        }

    except Exception as e:
        print("Error in Gemini call:", e)
        return {
            "score": 0,
            "reason": "Gemini error",
            "error": str(e)
        }


def summarize_team_analysis(analyzed_items):
    """
    After all work items are scored, group by user
    and call Gemini to evaluate team-level distribution.
    """

    user_map = defaultdict(lambda: {"tasks": [], "total_score": 0})
    for wi in analyzed_items:
        assigned = (
            wi.get("fields", {})
              .get("System.AssignedTo", {})
              .get("displayName", "Unassigned")
            or "Unassigned"
        )
        score = wi.get("analysis", {}).get("score", 0)
        reason = wi.get("analysis", {}).get("reason", "")

        user_map[assigned]["tasks"].append({
            "id": wi.get("id"),
            "title": wi.get("fields", {}).get("System.Title", "Untitled"),
            "score": score,
            "reason": reason
        })
        user_map[assigned]["total_score"] += score

    team_data = []
    for user, info in user_map.items():
        team_data.append({
            "name": user,
            "total_score": info["total_score"],
            "task_count": len(info["tasks"]),
            "tasks": info["tasks"]
        })

    summary_prompt = f"""
You are an AI assistant analyzing workload distribution in a development team.

You will receive JSON with each team member's:
- name
- total_score (sum of workload)
- task_count
- tasks (each has score and reason)

Your job:
Identify:
1. Overloaded members (high total_score or heavy tasks)
2. Underutilized members (low total_score or few light tasks)
3. Most efficient members (good output vs. effort or lower stress in reasoning)

Return JSON with EXACTLY this structure (no markdown, no extra keys):

{{
  "overloaded_members": [
    {{ "name": "...", "reason": "..." }},
    ...
  ],
  "underutilized_members": [
    {{ "name": "...", "reason": "..." }},
    ...
  ],
  "most_efficient_members": [
    {{ "name": "...", "reason": "..." }},
    ...
  ]
}}

Team Data:
{json.dumps(team_data, indent=2)}
"""

    try:
        response = model.generate_content(summary_prompt)
        raw_text = getattr(response, "text", "").strip()

        # ✅ Clean markdown formatting if present
        cleaned = raw_text
        # Remove ```json or ``` if present
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            # Also strip possible json/lang labels
            cleaned = re.sub(r"^json", "", cleaned, flags=re.IGNORECASE).strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            parsed = {
                "overloaded_members": [],
                "underutilized_members": [],
                "most_efficient_members": [],
                "raw": raw_text
            }

        return parsed

    except Exception as e:
        return {
            "overloaded_members": [],
            "underutilized_members": [],
            "most_efficient_members": [],
            "error": str(e)
        }


def analyze_workitems_with_gemini(workitems):
    """
    Analyze each work item individually, then summarize at team level.
    """
    analyzed_items = []
    for wi in workitems:
        analysis = analyze_single_workitem(wi)
        wi_copy = wi.copy()
        wi_copy["analysis"] = analysis
        analyzed_items.append(wi_copy)

    summary = summarize_team_analysis(analyzed_items)

    return {
        "analyzed_items": analyzed_items,
        "team_summary": summary
    }
