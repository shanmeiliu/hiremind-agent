from pydantic import BaseModel
from typing import List


class JobAnalyzeRequest(BaseModel):
    job_title: str
    company: str | None = None
    job_description: str
    resume_text: str


class JobAnalyzeResponse(BaseModel):
    match_score: int
    recommendation: str
    decision: str
    decision_reason: str
    semantic_score: int
    semantic_strengths: List[str]
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
    match_score: int

class JobAnalysisDetail(BaseModel):
    id: int
    job_title: str
    company: str | None = None
    recommendation: str
    decision: str
    status: str
    decision_reason: str | None = None
    match_score: int
    semantic_score: int | None = None
    semantic_strengths: List[str]
    transferable_skills: List[str]
    job_description: str
    resume_text: str
    strengths: List[str]
    missing_skills: List[str]
    application_notes: List[str]

class JobDecisionUpdateRequest(BaseModel):
    decision: str
    decision_reason: str | None = None