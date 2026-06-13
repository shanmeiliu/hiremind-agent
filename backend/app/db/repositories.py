from datetime import datetime
import json
import hashlib
from sqlalchemy.orm import Session

from app.db.models import JobAnalysis
from app.schemas.job import JobAnalyzeRequest, JobAnalyzeResponse


def build_job_key(
    job_title: str,
    company: str | None = None,
    job_url: str | None = None,
    source: str | None = None,
) -> str:
    if job_url:
        raw_key = f"{source or 'unknown'}:{job_url.strip().lower()}"
    else:
        raw_key = f"{source or 'manual'}:{company or ''}:{job_title}".strip().lower()

    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def create_job_analysis(
    db: Session,
    request: JobAnalyzeRequest,
    response: JobAnalyzeResponse,
) -> JobAnalysis:
    job_key = build_job_key(
        job_title=request.job_title,
        company=request.company,
        job_url=request.job_url,
        source=request.source,
    )

    job_analysis = (
        db.query(JobAnalysis)
        .filter(JobAnalysis.job_key == job_key)
        .first()
    )

    if job_analysis is None:
        job_analysis = JobAnalysis(
            job_title=request.job_title,
            company=request.company,
            job_url=request.job_url,
            source=request.source,
            job_key=job_key,
            status="saved",
        )
        db.add(job_analysis)

    job_analysis.recommendation = response.recommendation
    job_analysis.decision = response.decision
    job_analysis.decision_reason = response.decision_reason
    job_analysis.match_score = response.match_score
    job_analysis.semantic_score = response.semantic_score

    job_analysis.job_description = None
    job_analysis.resume_text = None

    job_analysis.strengths = json.dumps(response.strengths)
    job_analysis.missing_skills = json.dumps(response.missing_skills)
    job_analysis.application_notes = json.dumps(response.application_notes)
    job_analysis.semantic_strengths = json.dumps(response.semantic_strengths)
    job_analysis.transferable_skills = json.dumps(response.transferable_skills)

    db.commit()
    db.refresh(job_analysis)

    return job_analysis

def list_job_analyses(
    db: Session,
    limit: int = 20,
    decision: str | None = None,
    status: str | None = None,
    source: str | None = None,
    search: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[JobAnalysis]:
    query = db.query(JobAnalysis)

    if decision is not None:
        query = query.filter(JobAnalysis.decision == decision)

    if status is not None:
        query = query.filter(JobAnalysis.status == status)

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

def update_job_analysis_status(
    db: Session,
    analysis_id: int,
    status: str,
) -> JobAnalysis | None:
    job_analysis = get_job_analysis_by_id(db=db, analysis_id=analysis_id)

    if job_analysis is None:
        return None

    job_analysis.status = status

    db.commit()
    db.refresh(job_analysis)

    return job_analysis


def get_job_status_stats(db: Session) -> dict[str, int | float]:
    statuses = [
        "saved",
        "applied",
        "interview",
        "final_round",
        "offer",
        "rejected",
        "withdrawn",
        "ghosted",
    ]

    total = db.query(JobAnalysis).count()

    result: dict[str, int | float] = {"total": total}

    for status in statuses:
        result[status] = (
            db.query(JobAnalysis)
            .filter(JobAnalysis.status == status)
            .count()
        )

    applied_count = int(result["applied"])
    interview_count = int(result["interview"]) + int(result["final_round"]) + int(result["offer"])
    offer_count = int(result["offer"])

    result["interview_rate"] = round(
        interview_count / applied_count,
        4,
    ) if applied_count else 0.0

    result["offer_rate"] = round(
        offer_count / applied_count,
        4,
    ) if applied_count else 0.0

    return result