from fastapi import APIRouter
from app.schemas.job import JobAnalyzeRequest, JobAnalyzeResponse
from app.agents.job_match_graph import analyze_job_match

router = APIRouter()


@router.post("/analyze", response_model=JobAnalyzeResponse)
async def analyze_job(request: JobAnalyzeRequest):
    return analyze_job_match(request)