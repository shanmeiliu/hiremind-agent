# HireMind Agent

AI-powered job matching and application copilot built with LangGraph, FastAPI, React, and pgvector.

---

## Overview

HireMind Agent is an AI-assisted recruiting copilot designed to help users analyze job postings, evaluate job fit, and streamline the application workflow using LLM-powered agent pipelines.

The system combines:

* Browser-based job ingestion
* LangGraph workflow orchestration
* LangChain LLM integrations
* Resume-aware matching
* Vector search and semantic retrieval
* Human-in-the-loop review

Instead of blindly automating job applications, HireMind Agent focuses on intelligent filtering, ranking, and application preparation.

---

## Goals

* Extract job information from LinkedIn and other job platforms
* Compare jobs against user experience and preferences
* Rank jobs using LLM-based reasoning
* Generate tailored application notes
* Prepare answers for application questions
* Assist with resume optimization
* Provide an extensible multi-agent architecture

---

## Architecture

```text
Chrome Extension / Gmail Ingestion
                ↓
          FastAPI Backend
                ↓
         LangGraph Workflow
                ↓
     LangChain + LLM Providers
                ↓
      PostgreSQL + pgvector
                ↓
       Human Review Interface
```

---

## Planned Features

### Job Ingestion

* LinkedIn job page extraction
* Gmail job notification parsing
* Indeed and company career page support
* Saved job tracking

### AI Matching

* Resume-to-job semantic matching
* Skill gap analysis
* Experience relevance scoring
* Remote/hybrid preference filtering
* Salary and seniority analysis

### Agent Workflows

* Structured job extraction
* Resume analysis
* Match scoring
* Tailored application generation
* Interview preparation workflows

### Human-in-the-Loop

* Manual approval before apply
* Editable AI-generated responses
* Resume version selection
* Application history tracking

---

## Tech Stack

### Frontend

* React
* TypeScript
* Chrome Extension APIs
* Plasmo or Vite

### Backend

* FastAPI
* LangChain
* LangGraph
* PostgreSQL
* pgvector
* Redis (planned)

### AI/LLM

* OpenAI
* Anthropic
* Ollama (local models)
* Embedding models
* Reranker models

### Infrastructure

* Docker
* Docker Compose
* Nginx
* GitHub Actions

---

## Example Workflow

```text
1. User opens a LinkedIn job page
2. Chrome extension extracts the job description
3. Backend receives structured content
4. LangGraph workflow processes the job
5. AI agents:
   - extract skills
   - compare resume
   - calculate fit score
   - generate insights
6. Results appear in the extension sidebar
7. User decides whether to apply
```

---

## Example Match Output

```json
{
  "match_score": 87,
  "strengths": [
    "FastAPI experience",
    "RAG systems",
    "PostgreSQL + pgvector",
    "AWS backend architecture"
  ],
  "missing_skills": [
    "Production Kubernetes experience"
  ],
  "recommendation": "Strong Match",
  "generated_notes": [
    "Highlight LangGraph workflow experience",
    "Emphasize AI infrastructure projects"
  ]
}
```

---

## Planned LangGraph Workflow

```text
JobParserNode
        ↓
ResumeMatcherNode
        ↓
SkillGapAnalyzerNode
        ↓
FitScoringNode
        ↓
ApplicationGeneratorNode
        ↓
HumanReviewNode
```

---

## Repository Structure

```text
hiremind-agent/
├── frontend-extension/
├── backend/
├── agents/
├── shared/
├── docs/
├── docker-compose.yml
└── README.md
```

---

## MVP Roadmap

### Phase 1

* LinkedIn job extraction
* FastAPI backend
* LangGraph scoring workflow
* Sidebar UI

### Phase 2

* Resume ingestion
* pgvector semantic matching
* Gmail job parsing
* Saved jobs database

### Phase 3

* Resume tailoring
* AI-generated application responses
* Interview preparation assistant
* Multi-agent orchestration

---

## Future Ideas

* WhatsApp/Telegram notifications
* Interview question prediction
* AI-powered networking suggestions
* Company research agent
* Salary benchmarking
* Application analytics dashboard
* Multi-user/team support

---

## Development Status

Early-stage prototype and architecture exploration.

---

## License

MIT License
