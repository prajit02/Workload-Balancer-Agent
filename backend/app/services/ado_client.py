import requests
from requests.auth import HTTPBasicAuth
import re
from datetime import datetime, timedelta

BASE_API_VERSION = "7.0"

def run_wiql(org: str, project: str, pat: str, wiql_query: str):
    """Run a WIQL query and return IDs"""
    wiql_url = f"https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version={BASE_API_VERSION}"
    response = requests.post(wiql_url, json={"query": wiql_query}, auth=HTTPBasicAuth("", pat))
    response.raise_for_status()
    return response.json().get("workItems", [])

def fetch_workitems(org: str, project: str, pat: str):
    """Fetch last week's work items with full details"""
    query = f"""
        SELECT [System.Id]
        FROM workitems
        WHERE 
            [System.CreatedDate] >= @Today - 7
            AND [System.WorkItemType] = 'Task'
            AND [System.TeamProject] = '{project}'
        ORDER BY [System.Id] DESC
    """
    work_items = run_wiql(org, project, pat, query)
    if not work_items:
        return {"workItems": []}

    ids = ",".join(str(item["id"]) for item in work_items)
    details_url = f"https://dev.azure.com/{org}/_apis/wit/workitems?ids={ids}&$expand=fields&api-version={BASE_API_VERSION}"
    details_response = requests.get(details_url, auth=HTTPBasicAuth("", pat))
    details_response.raise_for_status()
    details_data = details_response.json()

    enriched_items = []
    for wi in details_data.get("value", []):
        wi_id = wi["id"]
        comments = fetch_comments(org, project, pat, wi_id)
        wi["comments"] = comments
        
        if(len(comments) == 0):
            comments = [" No comments found "]

        # print("Comments:", comments[0])

        wi = {
            "id": wi.get("id"),
            "fields": {
                "System.Id": wi["fields"].get("System.Id"),
                "System.Title": wi["fields"].get("System.Title"),
                "System.TeamProject": wi["fields"].get("System.TeamProject"),
                "System.AssignedTo": {
                    "displayName": wi["fields"].get("System.AssignedTo", {}).get("displayName")
                } if wi["fields"].get("System.AssignedTo") else None,
                "System.CreatedDate": wi["fields"].get("System.CreatedDate")
            },
            "comments": re.sub(r'&.*?nbsp;', '', re.sub(r'<.*?>', '', comments[0]))
        }
        enriched_items.append(wi)

    pull_requests = fetch_pullrequests(org, project, pat)
    ado_items = fetch_ado_items(org, project, pat)

    return {"count": len(enriched_items), "workItems": enriched_items, "PR Data": pull_requests, "ADO Items": ado_items}

def fetch_comments(org: str, project: str, pat: str, work_item_id: int):
    """Fetch comments for a given work item"""
    url = f"https://dev.azure.com/{org}/{project}/_apis/wit/workItems/{work_item_id}/comments?api-version={BASE_API_VERSION}-preview.3"
    response = requests.get(url, auth=HTTPBasicAuth("", pat))
    if response.status_code != 200:
        return []
    data = response.json()
    return [c.get("text", "") for c in data.get("comments", [])]

def fetch_pullrequests(org: str, project: str, pat: str):
    """Fetch pull requests for a project"""
    # TODO: comment count

    today = datetime.today()
    one_month_ago = today - timedelta(days=30)

    start_date = one_month_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
    # end_date = today.strftime('%Y-%m-%dT%H:%M:%SZ')

    url = f"https://dev.azure.com/{org}/{project}/_apis/git/pullrequests?status=completed&minTime={start_date}"
    response = requests.get(url, auth=HTTPBasicAuth("", pat))

    if response.status_code != 200:
        print(response)
        return {}
    data = response.json()

    name_counts = {}
    result = []

    for pr in data.get("value", []):
        created_by = pr.get("createdBy", {})
        display_name = created_by.get("displayName")

        # Handle created_by displayName
        if display_name:
            if display_name in name_counts:
                name_counts[display_name]["created_count"] += 1
            else:
                name_counts[display_name] = {
                    "created_count": 1,
                    "reviewed_count": 0
                }

        # Handle reviewers
        for reviewer in pr.get("reviewers", []):
            reviewer_display_name = reviewer.get("displayName")
            if reviewer_display_name:
                if reviewer_display_name in name_counts:
                    if "reviewed_count" in name_counts[reviewer_display_name]:
                        name_counts[reviewer_display_name]["reviewed_count"] += 1
                    else:
                        name_counts[reviewer_display_name]["reviewed_count"] = 1
                else:
                    name_counts[reviewer_display_name] = {
                        "created_count": 0,
                        "reviewed_count": 1
                    }

        # Add PR details to result list
        result.append({
            "repository": {
                "name": pr.get("repository", {}).get("name"),
                "id": pr.get("repository", {}).get("id")
            },
            "pullRequestId": pr.get("pullRequestId"),
            "status": pr.get("status"),
            "createdBy": {
                "displayName": pr.get("createdBy", {}).get("displayName"),
                "id": pr.get("createdBy", {}).get("id"),
                "uniqueName": pr.get("createdBy", {}).get("uniqueName")
            },
            "creationDate": pr.get("creationDate"),
            "closedDate": pr.get("closedDate"),
            "title": pr.get("title"),
            "reviewers": [{
                "displayName": reviewer.get("displayName"),
                "id": reviewer.get("id"),
                "uniqueName": reviewer.get("uniqueName"),
                "vote": reviewer.get("vote")
            } for reviewer in pr.get("reviewers", [])]
        })

    finalresult = {
        "pullRequests": {"count": len(result), "requestsInfo": result},
        "metricsInfo": name_counts
    }

    return finalresult

def fetch_ado_items(org: str, project: str, pat: str):
    """"Fetch ado items"""
    #TODO count by user of items

    query = f"""
        SELECT [System.Id]
        FROM workitems
        WHERE 
            [System.CreatedDate] >= @Today - 15
            AND [System.TeamProject] = '{project}'
        ORDER BY [System.Id] DESC
    """

    ado_items = run_wiql(org, project, pat, query)

    ids = ",".join(str(item["id"]) for item in ado_items)
    details_url = f"https://dev.azure.com/{org}/_apis/wit/workitems?ids={ids}&$expand=fields&api-version={BASE_API_VERSION}"
    details_response = requests.get(details_url, auth=HTTPBasicAuth("", pat))
    details_response.raise_for_status()
    details_response = details_response.json()

    enriched_items = []
    for wi in details_response.get("value", []):
        # if wi["fields"].get("System.WorkItemType") == "Task":
        #     continue
        wi = {
            "id": wi.get("id"),
            "fields": {
                # "System.Id": wi["fields"].get("System.Id"),
                "System.Title": wi["fields"].get("System.Title"),
                # "System.TeamProject": wi["fields"].get("System.TeamProject"),
                "System.WorkItemType": wi["fields"].get("System.WorkItemType"),
                "System.CreatedBy": {
                    "displayName": wi["fields"].get("System.CreatedBy", {}).get("displayName")
                },
                "System.CreatedDate": wi["fields"].get("System.CreatedDate")
            }
        }
        enriched_items.append(wi)

    name_counts = {}
    for item in enriched_items:
        created_by = item["fields"].get("System.CreatedBy", {})
        display_name = created_by.get("displayName")
        work_item_type = item["fields"].get("System.WorkItemType")
        if display_name:
            if display_name not in name_counts:
                name_counts[display_name] = {}
            if work_item_type in name_counts[display_name]:
                name_counts[display_name][work_item_type] += 1
            else:
                name_counts[display_name][work_item_type] = 1

    return {"count": len(enriched_items), "adoItems": enriched_items, "metricsInfo": name_counts}

    # print(type(enriched_items[0]))
    # print(enriched_items[0].keys())
    # di = {"id": enriched_items[0]["id"], 
    #       "fields": {
    #           "System.Id":enriched_items[0]["fields"]["System.Id"],
    #           "System.TeamProject":enriched_items[0]["fields"]["System.TeamProject"],
    #           "System.AssignedTo":{"displayName":enriched_items[0]["fields"]["System.AssignedTo"]["displayName"]},
    #           "System.CreatedDate":enriched_items[0]["fields"]["System.CreatedDate"]
    #         }, 
    #       "comments": enriched_items[0]["comments"]
    #       }
    # print(di)