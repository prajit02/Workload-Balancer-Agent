import requests
from requests.auth import HTTPBasicAuth
import re

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
            [System.CreatedDate] >= @Today - 2
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
        
        wi = {
            "id": wi["id"],
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

    return {"count": len(enriched_items), "workItems": enriched_items}

def fetch_comments(org: str, project: str, pat: str, work_item_id: int):
    """Fetch comments for a given work item"""
    url = f"https://dev.azure.com/{org}/{project}/_apis/wit/workItems/{work_item_id}/comments?api-version={BASE_API_VERSION}-preview.3"
    response = requests.get(url, auth=HTTPBasicAuth("", pat))
    if response.status_code != 200:
        return []
    data = response.json()
    return [c.get("text", "") for c in data.get("comments", [])]






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