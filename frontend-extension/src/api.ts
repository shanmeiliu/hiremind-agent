export type JobAnalyzeRequest = {
  job_title: string;
  company?: string;
  job_description: string;
  resume_text: string;
};

export type JobAnalyzeResponse = {
  match_score: number;
  recommendation: string;
  decision: string;
  decision_reason: string;
  semantic_score: number | null;
  semantic_strengths: string[];
  transferable_skills: string[];
  job_skills: string[];
  resume_skills: string[];
  strengths: string[];
  missing_skills: string[];
  application_notes: string[];
};

const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeJob(
  payload: JobAnalyzeRequest
): Promise<JobAnalyzeResponse> {
  const response = await fetch(`${API_BASE_URL}/api/jobs/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Analyze request failed: ${response.status}`);
  }

  return response.json();
}