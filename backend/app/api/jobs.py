from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.job_match_graph import analyze_job_match
from app.db.database import SessionLocal
from app.db.repositories import create_job_analysis
from app.schemas.job import JobAnalyzeRequest, JobAnalyzeResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/analyze", response_model=JobAnalyzeResponse)
async def analyze_job(
    request: JobAnalyzeRequest,
    db: Session = Depends(get_db),
):
    response = analyze_job_match(request)

    create_job_analysis(
        db=db,
        request=request,
        response=response,
    )

    return response