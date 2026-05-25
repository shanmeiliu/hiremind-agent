from app.schemas.job import JobAnalyzeRequest, JobAnalyzeResponse


def analyze_job_match(request: JobAnalyzeRequest) -> JobAnalyzeResponse:
    """
    Placeholder workflow.

    Later this will become a LangGraph pipeline:
    1. Parse job description
    2. Extract skills
    3. Compare with resume
    4. Score fit
    5. Generate application notes
    """

    job_text = request.job_description.lower()
    resume_text = request.resume_text.lower()

    keywords = [
        "python",
        "fastapi",
        "langchain",
        "langgraph",
        "rag",
        "postgres",
        "aws",
        "docker",
        "react",
        "typescript",
    ]

    matched = [kw for kw in keywords if kw in job_text and kw in resume_text]
    missing = [kw for kw in keywords if kw in job_text and kw not in resume_text]

    score = min(95, 40 + len(matched) * 8 - len(missing) * 3)

    if score >= 80:
        recommendation = "Strong Match"
    elif score >= 60:
        recommendation = "Potential Match"
    else:
        recommendation = "Weak Match"

    return JobAnalyzeResponse(
        match_score=max(score, 0),
        recommendation=recommendation,
        strengths=[f"Experience matches job requirement: {kw}" for kw in matched],
        missing_skills=[f"Job mentions {kw}, but it was not found in resume text" for kw in missing],
        application_notes=[
            "Highlight relevant backend and AI experience.",
            "Mention production experience with APIs, databases, and LLM workflows.",
            "Customize resume bullets around the strongest matched skills.",
        ],
    )