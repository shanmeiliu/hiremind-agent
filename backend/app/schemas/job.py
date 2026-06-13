from pydantic import BaseModel
from typing import List


class JobAnalyzeRequest(BaseModel):
    job_title: str
    company: str | None = None
    job_url: str | None = None
    source: str | None = None
    job_description: str
    resume_text: str


class JobAnalyzeResponse(BaseModel):
    analysis_id: int | None = None
    match_score: int
    recommendation: str
    decision: str
    decision_reason: str
    semantic_score: int
    semantic_strengths: List[str]
    # JobAnalyzeResponse
    status: str | None = None
    transferable_skills: List[str]
    job_skills: List[str]
    resume_skills: List[str]
    strengths: List[str]
    missing_skills: List[str]
    application_notes: List[str]
    

class JobAnalysisListItem(BaseModel):
    id: int
    job_title: str
    company: str | None = None
    recommendation: str
    decision: str
    status: str
    job_url: str | None = None
    source: str | None = None
    match_score: int

class JobAnalysisDetail(BaseModel):
    id: int
    job_title: str
    company: str | None = None
    recommendation: str
    decision: str
    job_url: str | None = None
    source: str | None = None
    job_key: str | None = None
    status: str
    decision_reason: str | None = None
    match_score: int
    semantic_score: int | None = None
    semantic_strengths: List[str]
    transferable_skills: List[str]
    job_description: str | None = None
    resume_text: str | None = None
    strengths: List[str]
    missing_skills: List[str]
    application_notes: List[str]

class JobDecisionUpdateRequest(BaseModel):
    decision: str
    decision_reason: str | None = None


class JobStatusUpdateRequest(BaseModel):
    status: str

class JobStatusStatsResponse(BaseModel):
    total: int
    saved: int
    applied: int
    interview: int
    final_round: int
    offer: int
    rejected: int
    withdrawn: int
    ghosted: int
    interview_rate: float
    offer_rate: float