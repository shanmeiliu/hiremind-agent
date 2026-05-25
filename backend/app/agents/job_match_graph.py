from typing import TypedDict, List
import json
from langgraph.graph import StateGraph, END
from app.agents.llm_provider import get_llm
from app.schemas.job import JobAnalyzeRequest, JobAnalyzeResponse


class JobMatchState(TypedDict):
    request: JobAnalyzeRequest
    job_keywords: List[str]
    resume_keywords: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    match_score: int
    recommendation: str
    decision: str
    decision_reason: str
    application_notes: List[str]


TRACKED_SKILLS = [
    "python",
    "fastapi",
    "langchain",
    "langgraph",
    "rag",
    "postgres",
    "pgvector",
    "aws",
    "docker",
    "react",
    "typescript",
    "redis",
    "kubernetes",
    "llm",
    "openai",
]


def parse_job(state: JobMatchState) -> JobMatchState:
    request = state["request"]
    job_text = request.job_description.lower()

    job_keywords = [skill for skill in TRACKED_SKILLS if skill in job_text]

    return {
        **state,
        "job_keywords": job_keywords,
    }


def compare_resume(state: JobMatchState) -> JobMatchState:
    request = state["request"]
    resume_text = request.resume_text.lower()

    resume_keywords = [skill for skill in TRACKED_SKILLS if skill in resume_text]
    matched_skills = [
        skill for skill in state["job_keywords"] if skill in resume_keywords
    ]
    missing_skills = [
        skill for skill in state["job_keywords"] if skill not in resume_keywords
    ]

    return {
        **state,
        "resume_keywords": resume_keywords,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


def score_match(state: JobMatchState) -> JobMatchState:
    matched_count = len(state["matched_skills"])
    missing_count = len(state["missing_skills"])
    job_keyword_count = max(len(state["job_keywords"]), 1)

    coverage_score = int((matched_count / job_keyword_count) * 100)
    penalty = missing_count * 3
    score = max(0, min(95, coverage_score - penalty))

    if score >= 80:
        recommendation = "Strong Match"
        decision = "apply"
        decision_reason = "The role has strong alignment with the candidate's existing skills and experience."
    elif score >= 60:
        recommendation = "Potential Match"
        decision = "maybe"
        decision_reason = "The role has some relevant overlap, but there are missing skills to review before applying."
    else:
        recommendation = "Weak Match"
        decision = "skip"
        decision_reason = "The role does not currently show enough alignment with the candidate's resume."

    return {
        **state,
        "match_score": score,
        "recommendation": recommendation,
        "decision": decision,
        "decision_reason": decision_reason,
    }


def generate_notes(state: JobMatchState) -> JobMatchState:
    request = state["request"]
    matched = state["matched_skills"]
    missing = state["missing_skills"]

    fallback_notes = [
        "Highlight the strongest matching skills near the top of the resume.",
        "Use the job posting language when describing relevant project experience.",
        "Mention production experience with APIs, databases, and LLM workflows.",
    ]

    try:
        llm = get_llm()

        prompt = f"""
You are an AI job application assistant.

Generate application notes for this job match.

Return ONLY valid JSON with this exact schema:
{{
  "application_notes": [
    "note 1",
    "note 2",
    "note 3"
  ]
}}

Rules:
- Return 3 to 5 notes.
- Each note must be one sentence.
- Do not use markdown.
- Do not exaggerate experience.
- Do not invent skills.
- Focus on how the candidate should position their experience.

Job title:
{request.job_title}

Company:
{request.company or "Unknown"}

Matched skills:
{", ".join(matched) if matched else "None"}

Missing skills:
{", ".join(missing) if missing else "None"}

Job description:
{request.job_description}

Resume text:
{request.resume_text}
"""

        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)

        parsed = json.loads(content)
        notes = parsed.get("application_notes", [])

        if not isinstance(notes, list) or not notes:
            notes = fallback_notes

        notes = [str(note).strip() for note in notes if str(note).strip()]

    except Exception as exc:
        notes = fallback_notes + [
            f"LLM note generation failed, using fallback notes. Error: {str(exc)}"
        ]

    return {
        **state,
        "application_notes": notes[:5],
    }

def build_job_match_graph():
    graph = StateGraph(JobMatchState)

    graph.add_node("parse_job", parse_job)
    graph.add_node("compare_resume", compare_resume)
    graph.add_node("score_match", score_match)
    graph.add_node("generate_notes", generate_notes)

    graph.set_entry_point("parse_job")

    graph.add_edge("parse_job", "compare_resume")
    graph.add_edge("compare_resume", "score_match")
    graph.add_edge("score_match", "generate_notes")
    graph.add_edge("generate_notes", END)

    return graph.compile()


job_match_graph = build_job_match_graph()


def analyze_job_match(request: JobAnalyzeRequest) -> JobAnalyzeResponse:
    initial_state: JobMatchState = {
    "request": request,
    "job_keywords": [],
    "resume_keywords": [],
    "matched_skills": [],
    "missing_skills": [],
    "match_score": 0,
    "recommendation": "",
    "decision": "",
    "decision_reason": "",
    "application_notes": [],
}

    final_state = job_match_graph.invoke(initial_state)

    return JobAnalyzeResponse(
        match_score=final_state["match_score"],
        recommendation=final_state["recommendation"],
        decision=final_state["decision"],
        decision_reason=final_state["decision_reason"],
        job_skills=final_state["job_keywords"],
        resume_skills=final_state["resume_keywords"],
        strengths=[
            f"Experience matches job requirement: {skill}"
            for skill in final_state["matched_skills"]
        ],
        missing_skills=[
            f"Job mentions {skill}, but it was not found in resume text"
            for skill in final_state["missing_skills"]
        ],
        application_notes=final_state["application_notes"],
    )