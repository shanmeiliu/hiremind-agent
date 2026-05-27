const SIDEBAR_ID = "hiremind-agent-sidebar";

type ExtractedJobPage = {
  jobTitle: string;
  company: string;
  jobDescription: string;
  source: "linkedin" | "indeed" | "fallback";
};

function getText(selector: string): string {
  const element = document.querySelector(selector);
  return element?.textContent?.trim() || "";
}

function getLinkedInJobPage(): ExtractedJobPage {
  const jobTitle =
    getText(".job-details-jobs-unified-top-card__job-title") ||
    getText(".job-details-jobs-unified-top-card__job-title h1") ||
    getText("h1") ||
    document.title;

  const company =
    getText(".job-details-jobs-unified-top-card__company-name") ||
    getText(".job-details-jobs-unified-top-card__primary-description-container a") ||
    "";

  const jobDescription =
    getText(".jobs-description-content__text") ||
    getText(".jobs-box__html-content") ||
    getText("#job-details") ||
    getText(".jobs-description") ||
    getText('[class*="jobs-description"]') ||
    document.body.innerText.slice(0, 12000);

  return {
    jobTitle,
    company,
    jobDescription,
    source: "linkedin",
  };
}

function getIndeedJobPage(): ExtractedJobPage {
  const jobTitle =
    getText('[data-testid="jobsearch-JobInfoHeader-title"]') ||
    getText("h1") ||
    document.title;

  const company =
    getText('[data-testid="inlineHeader-companyName"]') ||
    getText('[data-company-name="true"]') ||
    "";

  const jobDescription =
    getText("#jobDescriptionText") ||
    getText('[data-testid="jobsearch-JobComponent-description"]') ||
    document.body.innerText.slice(0, 12000);

  return {
    jobTitle,
    company,
    jobDescription,
    source: "indeed",
  };
}

function getFallbackJobPage(): ExtractedJobPage {
  return {
    jobTitle: document.title || "Unknown Job",
    company: "",
    jobDescription: document.body.innerText.slice(0, 12000),
    source: "fallback",
  };
}

function extractJobPage(): ExtractedJobPage {
  const hostname = window.location.hostname;

  if (hostname.includes("linkedin.com")) {
    return getLinkedInJobPage();
  }

  if (hostname.includes("indeed.com")) {
    return getIndeedJobPage();
  }

  return getFallbackJobPage();
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function createSidebar() {
  if (document.getElementById(SIDEBAR_ID)) {
    return;
  }

  const extractedJob = extractJobPage();

  const sidebar = document.createElement("div");
  sidebar.id = SIDEBAR_ID;

  sidebar.innerHTML = `
    <div style="
      position: fixed;
      top: 0;
      right: 0;
      width: 420px;
      height: 100vh;
      z-index: 999999;
      background: white;
      border-left: 1px solid #ddd;
      box-shadow: -4px 0 16px rgba(0,0,0,0.15);
      font-family: Arial, sans-serif;
      padding: 16px;
      overflow-y: auto;
      color: #111827;
    ">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;">HireMind Agent</h2>
        <button id="hiremind-close" style="font-size:18px;">×</button>
      </div>

      <p style="color:#666;">Analyze this job page with AI.</p>

      <div style="
        margin-top: 12px;
        padding: 10px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
      ">
        <div><strong>Detected:</strong> ${escapeHtml(extractedJob.source)}</div>
        <div><strong>Title:</strong> ${escapeHtml(extractedJob.jobTitle)}</div>
        <div><strong>Company:</strong> ${escapeHtml(extractedJob.company || "Unknown")}</div>
        <div><strong>Description chars:</strong> ${extractedJob.jobDescription.length}</div>
      </div>

      <label style="display:block; margin-top:12px; font-weight:bold;">
        Resume Text
      </label>
      <textarea id="hiremind-resume" style="width:100%; height:160px; margin-top:6px;"></textarea>

      <button id="hiremind-analyze" style="
        width:100%;
        margin-top:12px;
        padding:10px;
        background:#111827;
        color:white;
        border:none;
        border-radius:8px;
        font-weight:bold;
        cursor:pointer;
      ">
        Analyze Current Page
      </button>

      <div id="hiremind-result" style="margin-top:16px;"></div>
    </div>
  `;

  document.body.appendChild(sidebar);

  const resumeTextarea = document.getElementById(
  "hiremind-resume"
    ) as HTMLTextAreaElement | null;

  chrome.storage.local.get(["hiremind_resume_text"], (result) => {
  const savedResumeText = result.hiremind_resume_text;

if (resumeTextarea && typeof savedResumeText === "string") {
  resumeTextarea.value = savedResumeText;
}
});

resumeTextarea?.addEventListener("input", () => {
  chrome.storage.local.set({
    hiremind_resume_text: resumeTextarea.value,
  });
});

  document.getElementById("hiremind-close")?.addEventListener("click", () => {
    sidebar.remove();
  });

  document.getElementById("hiremind-analyze")?.addEventListener("click", async () => {
    const resultBox = document.getElementById("hiremind-result");
    const resumeText = (document.getElementById("hiremind-resume") as HTMLTextAreaElement).value;

    if (!resultBox) return;

    if (!resumeText.trim()) {
      resultBox.innerHTML = `<p style="color:#b91c1c;">Please paste your resume text first.</p>`;
      return;
    }

    resultBox.innerHTML = `<p>Analyzing...</p>`;

    try {
      const latestJob = extractJobPage();

      const response = await fetch("http://127.0.0.1:8000/api/jobs/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          job_title: latestJob.jobTitle,
          company: latestJob.company,
          job_description: latestJob.jobDescription,
          resume_text: resumeText
        })
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();

      resultBox.innerHTML = `
        <h3>${data.match_score}% — ${escapeHtml(data.recommendation)}</h3>
        <p><strong>Decision:</strong> ${escapeHtml(data.decision)}</p>
        <p>${escapeHtml(data.decision_reason)}</p>

        <h4>Semantic Score</h4>
        <p>${data.semantic_score ?? "N/A"}</p>

        <h4>Application Notes</h4>
        <ul>
          ${data.application_notes.map((note: string) => `<li>${escapeHtml(note)}</li>`).join("")}
        </ul>

        <h4>Transferable Skills</h4>
        <ul>
          ${data.transferable_skills.map((skill: string) => `<li>${escapeHtml(skill)}</li>`).join("")}
        </ul>

        <h4>Missing Skills</h4>
        <ul>
          ${data.missing_skills.map((skill: string) => `<li>${escapeHtml(skill)}</li>`).join("")}
        </ul>
      `;
    } catch (error) {
      resultBox.innerHTML = `<p style="color:#b91c1c;">${escapeHtml(
        error instanceof Error ? error.message : "Failed to analyze page"
      )}</p>`;
    }
  });
}

createSidebar();