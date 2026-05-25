import json

from sqlalchemy.orm import Session

from app.db.models import JobAnalysis
from app.schemas.job import JobAnalyzeRequest, JobAnalyzeResponse


def create_job_analysis(
    db: Session,
    request: JobAnalyzeRequest,
    response: JobAnalyzeResponse,
) -> JobAnalysis:
    job_analysis = JobAnalysis(
        job_title=request.job_title,
        company=request.company,
        recommendation=response.recommendation,
        decision=response.decision,
        match_score=response.match_score,
        job_description=request.job_description,
        resume_text=request.resume_text,
        strengths=json.dumps(response.strengths),
        missing_skills=json.dumps(response.missing_skills),
        application_notes=json.dumps(response.application_notes),
    )

    db.add(job_analysis)
    db.commit()
    db.refresh(job_analysis)

    return job_analysis

def list_job_analyses(db: Session, limit: int = 20) -> list[JobAnalysis]:
    return (
        db.query(JobAnalysis)
        .order_by(JobAnalysis.created_at.desc())
        .limit(limit)
        .all()
    )