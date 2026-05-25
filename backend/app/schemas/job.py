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
    strengths: List[str]
    missing_skills: List[str]
    application_notes: List[str]