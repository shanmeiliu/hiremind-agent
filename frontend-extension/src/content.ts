const SIDEBAR_ID = "hiremind-agent-sidebar";
const RESUME_STORAGE_KEY = "hiremind_resume_text";
const FONT_SIZE_KEY = "hiremind_font_size";

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

function applyFontSize(size: number) {
  const sidebar = document.getElementById(SIDEBAR_ID);

  if (!sidebar) {
    return;
  }

  sidebar.style.fontSize = `${size}px`;
}

function updateFontSize(delta: number) {
  chrome.storage.local.get([FONT_SIZE_KEY], (result) => {
    let size =
      typeof result[FONT_SIZE_KEY] === "number"
        ? result[FONT_SIZE_KEY]
        : 14;

    size += delta;
    size = Math.max(10, Math.min(24, size));

    chrome.storage.local.set({
      [FONT_SIZE_KEY]: size,
    });

    applyFontSize(size);
  });
}

function resetFontSize() {
  chrome.storage.local.set({
    [FONT_SIZE_KEY]: 14,
  });

  applyFontSize(14);
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
      line-height: 1.5;
    ">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;">HireMind Agent</h2>
        <button id="hiremind-close" style="
          font-size:18px;
          border:1px solid #9ca3af;
          background:white;
          border-radius:4px;
          cursor:pointer;
        ">×</button>
      </div>

      <p style="color:#666; margin-bottom:8px;">Analyze this job page with AI.</p>

      <div style="
        display:flex;
        gap:8px;
        align-items:center;
        margin:8px 0 12px;
      ">
        <span style="font-weight:bold;">Text size:</span>
        <button id="hiremind-font-down" style="
          padding:4px 8px;
          border:1px solid #d1d5db;
          background:#f9fafb;
          border-radius:6px;
          cursor:pointer;
        ">A-</button>
        <button id="hiremind-font-reset" style="
          padding:4px 8px;
          border:1px solid #d1d5db;
          background:#f9fafb;
          border-radius:6px;
          cursor:pointer;
        ">A</button>
        <button id="hiremind-font-up" style="
          padding:4px 8px;
          border:1px solid #d1d5db;
          background:#f9fafb;
          border-radius:6px;
          cursor:pointer;
        ">A+</button>
      </div>

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
      <textarea id="hiremind-resume" style="
        width:100%;
        height:160px;
        margin-top:6px;
        box-sizing:border-box;
        font: inherit;
        padding:8px;
        border:1px solid #9ca3af;
        border-radius:6px;
      "></textarea>

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
        font: inherit;
      ">
        Analyze Current Page
      </button>

      <div id="hiremind-result" style="margin-top:16px;"></div>
    </div>
  `;

  document.body.appendChild(sidebar);

  chrome.storage.local.get([FONT_SIZE_KEY], (result) => {
    const size =
      typeof result[FONT_SIZE_KEY] === "number"
        ? result[FONT_SIZE_KEY]
        : 14;

    applyFontSize(size);
  });

  const resumeTextarea = document.getElementById(
    "hiremind-resume"
  ) as HTMLTextAreaElement | null;

  chrome.storage.local.get([RESUME_STORAGE_KEY], (result) => {
    const savedResumeText = result[RESUME_STORAGE_KEY];

    if (resumeTextarea && typeof savedResumeText === "string") {
      resumeTextarea.value = savedResumeText;
    }
  });

  resumeTextarea?.addEventListener("input", () => {
    chrome.storage.local.set({
      [RESUME_STORAGE_KEY]: resumeTextarea.value,
    });
  });

  document.getElementById("hiremind-font-up")?.addEventListener("click", () => {
    updateFontSize(1);
  });

  document.getElementById("hiremind-font-down")?.addEventListener("click", () => {
    updateFontSize(-1);
  });

  document.getElementById("hiremind-font-reset")?.addEventListener("click", () => {
    resetFontSize();
  });

  document.getElementById("hiremind-close")?.addEventListener("click", () => {
    sidebar.remove();
  });

  document.getElementById("hiremind-analyze")?.addEventListener("click", async () => {
    const resultBox = document.getElementById("hiremind-result");
    const resumeText = resumeTextarea?.value || "";

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
          job_url: window.location.href,
          source: latestJob.source,
          job_description: latestJob.jobDescription,
          resume_text: resumeText
        })
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();

      resultBox.innerHTML = `
        <h3 style="margin-bottom:4px;">${data.match_score}% — ${escapeHtml(data.recommendation)}</h3>
        <p style="margin:4px 0;"><strong>Decision:</strong> ${escapeHtml(data.decision)}</p>
        <p style="margin-top:4px;">${escapeHtml(data.decision_reason)}</p>

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