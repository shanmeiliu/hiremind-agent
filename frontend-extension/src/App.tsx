import { useState } from "react";
import "./App.css";
import { analyzeJob } from "./api";
import type { JobAnalyzeResponse } from "./api";

function App() {
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [result, setResult] = useState<JobAnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeJob({
        job_title: jobTitle,
        company: company || undefined,
        job_description: jobDescription,
        resume_text: resumeText,
      });

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyze job");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <h1>HireMind Agent</h1>
      <p className="subtitle">AI job matching copilot</p>

      <label>
        Job title
        <input
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          placeholder="Senior Backend Engineer"
        />
      </label>

      <label>
        Company
        <input
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="FutureFit AI"
        />
      </label>

      <label>
        Job description
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste job description here..."
        />
      </label>

      <label>
        Resume text
        <textarea
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          placeholder="Paste resume text here..."
        />
      </label>

      <button
        onClick={handleAnalyze}
        disabled={loading || !jobTitle || !jobDescription || !resumeText}
      >
        {loading ? "Analyzing..." : "Analyze Job"}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <section className="result">
          <h2>{result.match_score}% — {result.recommendation}</h2>
          <p><strong>Decision:</strong> {result.decision}</p>
          <p>{result.decision_reason}</p>

          <h3>Application Notes</h3>
          <ul>
            {result.application_notes.map((note, index) => (
              <li key={index}>{note}</li>
            ))}
          </ul>

          <h3>Transferable Skills</h3>
          <ul>
            {result.transferable_skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>

          <h3>Missing Skills</h3>
          <ul>
            {result.missing_skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}

export default App;