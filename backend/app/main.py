from fastapi import FastAPI
from app.api.jobs import router as jobs_router
from app.db.database import Base, engine
from app.db import models
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="HireMind Agent",
    description="AI-powered job matching and application copilot.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://www.linkedin.com",
        "https://www.indeed.com",
        "https://ca.indeed.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobs_router, prefix="/api/jobs", tags=["jobs"])


@app.get("/")
def root():
    return {"message": "HireMind Agent API is running"}