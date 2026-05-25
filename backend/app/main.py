from fastapi import FastAPI
from app.api.jobs import router as jobs_router

app = FastAPI(
    title="HireMind Agent",
    description="AI-powered job matching and application copilot.",
    version="0.1.0",
)

app.include_router(jobs_router, prefix="/api/jobs", tags=["jobs"])


@app.get("/")
def root():
    return {"message": "HireMind Agent API is running"}