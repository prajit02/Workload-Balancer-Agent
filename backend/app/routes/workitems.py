from fastapi import APIRouter, Query
from app.services import ado_client, workload_service

router = APIRouter(prefix="/workitems", tags=["workitems"])

@router.get("/")
def get_workitems(org: str, project: str, pat: str, analyze: bool = False, days: int = 15):
    result = ado_client.fetch_workitems(org, project, pat, days)
    if analyze and "workItems" in result:
        result["workItems"] = workload_service.analyze_workitems_with_gemini(result["workItems"])
    return result