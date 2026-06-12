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
        status="saved",
        match_score=response.match_score,
        job_description=request.job_description,
        resume_text=request.resume_text,
        strengths=json.dumps(response.strengths),
        missing_skills=json.dumps(response.missing_skills),
        application_notes=json.dumps(response.application_notes),
        decision_reason=response.decision_reason,
        semantic_score=response.semantic_score,
        semantic_strengths=json.dumps(response.semantic_strengths),
        transferable_skills=json.dumps(response.transferable_skills),
        )

    db.add(job_analysis)
    db.commit()
    db.refresh(job_analysis)

    return job_analysis

def list_job_analyses(
    db: Session,
    limit: int = 20,
    decision: str | None = None,
) -> list[JobAnalysis]:
    query = db.query(JobAnalysis)

    if decision is not None:
        query = query.filter(JobAnalysis.decision == decision)

    return (
        query
        .order_by(JobAnalysis.created_at.desc())
        .limit(limit)
        .all()
    )

def update_job_analysis_decision(
    db: Session,
    analysis_id: int,
    decision: str,
    decision_reason: str | None = None,
) -> JobAnalysis | None:
    job_analysis = get_job_analysis_by_id(db=db, analysis_id=analysis_id)

    if job_analysis is None:
        return None

    job_analysis.decision = decision

    if decision_reason is not None:
        job_analysis.decision_reason = decision_reason

    db.commit()
    db.refresh(job_analysis)

    return job_analysis

def get_job_analysis_by_id(db: Session, analysis_id: int) -> JobAnalysis | None:
    return db.query(JobAnalysis).filter(JobAnalysis.id == analysis_id).first()