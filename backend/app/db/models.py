from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, index=True)

    job_title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    job_url = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    job_key = Column(String, nullable=True, unique=True, index=True)

    recommendation = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    status = Column(String, nullable=False, default="saved")
    match_score = Column(Integer, nullable=False)

    semantic_score = Column(Integer, nullable=True)
    semantic_strengths = Column(Text, nullable=True)
    transferable_skills = Column(Text, nullable=True)
    decision_reason = Column(Text, nullable=True)

    job_description = Column(Text, nullable=False)
    resume_text = Column(Text, nullable=False)

    strengths = Column(Text, nullable=True)
    missing_skills = Column(Text, nullable=True)
    application_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())