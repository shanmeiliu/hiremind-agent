const SIDEBAR_ID = "hiremind-agent-sidebar";

function getPageText() {
  return document.body.innerText.slice(0, 12000);
}

function getPageTitle() {
  return document.title || "Unknown Job";
}

function createSidebar() {
  if (document.getElementById(SIDEBAR_ID)) {
    return;
  }

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
    ">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;">HireMind Agent</h2>
        <button id="hiremind-close" style="font-size:18px;">×</button>
      </div>

      <p style="color:#666;">Analyze this job page with AI.</p>

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

  document.getElementById("hiremind-close")?.addEventListener("click", () => {
    sidebar.remove();
  });

  document.getElementById("hiremind-analyze")?.addEventListener("click", async () => {
    const resultBox = document.getElementById("hiremind-result");
    const resumeText = (document.getElementById("hiremind-resume") as HTMLTextAreaElement).value;

    if (!resumeText.trim()) {
      resultBox!.innerHTML = `<p style="color:#b91c1c;">Please paste your resume text first.</p>`;
      return;
    }

    resultBox!.innerHTML = `<p>Analyzing...</p>`;

    try {
      const response = await fetch("http://127.0.0.1:8000/api/jobs/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          job_title: getPageTitle(),
          company: "",
          job_description: getPageText(),
          resume_text: resumeText
        })
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();

      resultBox!.innerHTML = `
        <h3>${data.match_score}% — ${data.recommendation}</h3>
        <p><strong>Decision:</strong> ${data.decision}</p>
        <p>${data.decision_reason}</p>

        <h4>Application Notes</h4>
        <ul>
          ${data.application_notes.map((note: string) => `<li>${note}</li>`).join("")}
        </ul>

        <h4>Missing Skills</h4>
        <ul>
          ${data.missing_skills.map((skill: string) => `<li>${skill}</li>`).join("")}
        </ul>
      `;
    } catch (error) {
      resultBox!.innerHTML = `<p style="color:#b91c1c;">${error instanceof Error ? error.message : "Failed to analyze page"}</p>`;
    }
  });
}

createSidebar();