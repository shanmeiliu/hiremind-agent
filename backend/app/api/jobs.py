import json
from fastapi import APIRouter, Depends, HTTPException
from app.db.repositories import (
    create_job_analysis,
    list_job_analyses,
    get_job_analysis_by_id,
    update_job_analysis_decision,
    update_job_analysis_status
)
from app.schemas.job import (
    JobAnalyzeRequest,
    JobAnalyzeResponse,
    JobAnalysisListItem,
    JobAnalysisDetail,
    JobDecisionUpdateRequest,
    JobStatusUpdateRequest
)
from sqlalchemy.orm import Session
from typing import List
from app.agents.job_match_graph import analyze_job_match
from app.db.database import SessionLocal


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

@router.get("/analyses", response_model=List[JobAnalysisListItem])
async def get_job_analyses(
    limit: int = 20,
    decision: str | None = None,
    db: Session = Depends(get_db),
):
    allowed_decisions = {"apply", "maybe", "skip"}

    if decision is not None and decision not in allowed_decisions:
        raise HTTPException(
            status_code=400,
            detail="Decision must be one of: apply, maybe, skip",
        )

    analyses = list_job_analyses(
        db=db,
        limit=limit,
        decision=decision,
    )

    return [
        JobAnalysisListItem(
            id=item.id,
            job_title=item.job_title,
            company=item.company,
            job_url=item.job_url,
            source=item.source,
            recommendation=item.recommendation,
            decision=item.decision,
            status=item.status,
            match_score=item.match_score,
        )
        for item in analyses
    ]

@router.get("/analyses/{analysis_id}", response_model=JobAnalysisDetail)
async def get_job_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    item = get_job_analysis_by_id(db=db, analysis_id=analysis_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    return JobAnalysisDetail(
        id=item.id,
        job_title=item.job_title,
        company=item.company,
        recommendation=item.recommendation,
        decision=item.decision,
        decision_reason=item.decision_reason,
        match_score=item.match_score,
        semantic_score=item.semantic_score,
        semantic_strengths=json.loads(item.semantic_strengths or "[]"),
        transferable_skills=json.loads(item.transferable_skills or "[]"),
        job_description=item.job_description,
        resume_text=item.resume_text,
        strengths=json.loads(item.strengths or "[]"),
        missing_skills=json.loads(item.missing_skills or "[]"),
        application_notes=json.loads(item.application_notes or "[]"),
        job_url=item.job_url,
        source=item.source,
        job_key=item.job_key,
        status=item.status,
    )

@router.patch("/analyses/{analysis_id}/decision", response_model=JobAnalysisDetail)
async def update_job_decision(
    analysis_id: int,
    request: JobDecisionUpdateRequest,
    db: Session = Depends(get_db),
):
    allowed_decisions = {"apply", "maybe", "skip"}

    if request.decision not in allowed_decisions:
        raise HTTPException(
            status_code=400,
            detail="Decision must be one of: apply, maybe, skip",
        )

    item = update_job_analysis_decision(
        db=db,
        analysis_id=analysis_id,
        decision=request.decision,
        decision_reason=request.decision_reason,
    )

    if item is None:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    return JobAnalysisDetail(
        id=item.id,
        job_title=item.job_title,
        company=item.company,
        recommendation=item.recommendation,
        decision=item.decision,
        decision_reason=item.decision_reason,
        match_score=item.match_score,
        semantic_score=item.semantic_score,
        semantic_strengths=json.loads(item.semantic_strengths or "[]"),
        transferable_skills=json.loads(item.transferable_skills or "[]"),
        job_description=item.job_description,
        resume_text=item.resume_text,
        strengths=json.loads(item.strengths or "[]"),
        missing_skills=json.loads(item.missing_skills or "[]"),
        application_notes=json.loads(item.application_notes or "[]"),
        job_url=item.job_url,
        source=item.source,
        job_key=item.job_key,
        status=item.status,
    )

@router.patch("/analyses/{analysis_id}/status", response_model=JobAnalysisDetail)
async def update_job_status(
    analysis_id: int,
    request: JobStatusUpdateRequest,
    db: Session = Depends(get_db),
):
    allowed_statuses = {
        "saved",
        "applied",
        "interview",
        "final_round",
        "offer",
        "rejected",
        "withdrawn",
        "ghosted",
    }

    if request.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be one of: saved, applied, interview, final_round, offer, rejected, withdrawn, ghosted",
        )

    item = update_job_analysis_status(
        db=db,
        analysis_id=analysis_id,
        status=request.status,
    )

    if item is None:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    return JobAnalysisDetail(
        id=item.id,
        job_title=item.job_title,
        company=item.company,
        job_url=item.job_url,
        source=item.source,
        job_key=item.job_key,
        recommendation=item.recommendation,
        decision=item.decision,
        status=item.status,
        decision_reason=item.decision_reason,
        match_score=item.match_score,
        semantic_score=item.semantic_score,
        semantic_strengths=json.loads(item.semantic_strengths or "[]"),
        transferable_skills=json.loads(item.transferable_skills or "[]"),
        job_description=item.job_description,
        resume_text=item.resume_text,
        strengths=json.loads(item.strengths or "[]"),
        missing_skills=json.loads(item.missing_skills or "[]"),
        application_notes=json.loads(item.application_notes or "[]"),
    )