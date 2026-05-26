import json
from fastapi import APIRouter, Depends, HTTPException
from app.db.repositories import create_job_analysis, list_job_analyses, get_job_analysis_by_id
from app.schemas.job import (
    JobAnalyzeRequest,
    JobAnalyzeResponse,
    JobAnalysisListItem,
    JobAnalysisDetail,
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
    db: Session = Depends(get_db),
):
    analyses = list_job_analyses(db=db, limit=limit)

    return [
        JobAnalysisListItem(
            id=item.id,
            job_title=item.job_title,
            company=item.company,
            recommendation=item.recommendation,
            decision=item.decision,
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
    )