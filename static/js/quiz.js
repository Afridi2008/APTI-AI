/* ───────────────────────────────────────────
   Aptitude AI  ·  Quiz & Result JS
─────────────────────────────────────────── */

// ── Timer ──────────────────────────────────
let timerInterval = null;

function startTimer(seconds) {
  const display = document.getElementById("timer");
  if (!display) return;

  function tick() {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    display.textContent = `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
    display.style.color = seconds <= 30 ? "var(--danger)" : "var(--accent)";

    if (seconds <= 0) {
      clearInterval(timerInterval);
      display.textContent = "00:00";
      submitQuiz(true);  // auto-submit on timeout
    }
    seconds--;
  }

  tick();
  timerInterval = setInterval(tick, 1000);
}

// ── Option Selection ───────────────────────
document.addEventListener("click", function (e) {
  const opt = e.target.closest(".option-btn");
  if (!opt) return;

  const group = opt.closest(".options-group");
  group.querySelectorAll(".option-btn").forEach(b => {
    b.classList.remove("selected");
    b.setAttribute("aria-checked", "false");
  });
  opt.classList.add("selected");
  opt.setAttribute("aria-checked", "true");

  // progress bar update
  updateProgress();
});

function updateProgress() {
  const total    = document.querySelectorAll(".question-card").length;
  const answered = document.querySelectorAll(".option-btn.selected").length;
  const bar = document.getElementById("progress-bar");
  const label = document.getElementById("progress-label");
  if (bar) bar.style.width = `${(answered / total) * 100}%`;
  if (label) label.textContent = `${answered} / ${total} answered`;
}

// ── Submit ────────────────────────────────
async function submitQuiz(timedOut = false) {
  clearInterval(timerInterval);

  const submitBtn = document.getElementById("submit-btn");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Submitting…';
  }

  const answers = {};
  document.querySelectorAll(".question-card").forEach(card => {
    const qId = card.dataset.qid;
    const sel  = card.querySelector(".option-btn.selected");
    if (sel) answers[qId] = sel.dataset.value;
  });

  try {
    const res  = await fetch("/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers })
    });
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert("Something went wrong. Please try again.");
    if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Submit Answers"; }
  }
}

// ── Result Rendering ──────────────────────
function renderResults(data) {
  const quizSection   = document.getElementById("quiz-section");
  const resultSection = document.getElementById("result-section");

  quizSection.style.display   = "none";
  resultSection.style.display = "block";
  resultSection.scrollIntoView({ behavior: "smooth" });

  const pct = Math.round((data.score / data.total) * 100);

  document.getElementById("score-display").textContent  = `${data.score} / ${data.total}`;
  document.getElementById("score-percent").textContent  = `${pct}%`;
  document.getElementById("score-ring").style.setProperty("--pct", pct);

  const msg = pct >= 80 ? "🎉 Excellent work!" :
              pct >= 50 ? "👍 Good effort — keep practising!" :
              "💪 Don't worry — review the explanations below!";
  document.getElementById("score-msg").textContent = msg;

  const breakdown = document.getElementById("breakdown");
  breakdown.innerHTML = "";

  data.details.forEach((item, i) => {
    const card = document.createElement("div");
    card.className = "result-card card mt-2";
    card.innerHTML = `
      <div class="result-header">
        <span class="badge ${item.is_correct ? "badge-green" : "badge-red"}">
          ${item.is_correct ? "✓ Correct" : "✗ Wrong"}
        </span>
        <span class="badge badge-blue">${item.topic}</span>
      </div>
      <p class="result-question mt-1"><strong>Q${i+1}.</strong> ${item.question}</p>
      <div class="result-options mt-1">
        ${item.options.map((opt, idx) => {
          const key = `option${idx+1}`;
          const isCorrect = key === item.correct_answer;
          const isUser    = key === item.user_answer;
          let cls = "result-opt";
          if (isCorrect) cls += " opt-correct";
          else if (isUser && !isCorrect) cls += " opt-wrong";
          return `<div class="${cls}">${isUser ? "▶ " : ""}${opt}${isCorrect ? " ✓" : ""}</div>`;
        }).join("")}
      </div>
      ${!item.is_correct ? `
        <div class="explain-wrap mt-2">
          <button class="btn btn-outline explain-btn" onclick="loadExplanation(this, \`${esc(item.question)}\`, \`${esc(item.correct_answer)}\`)">
            💡 Get AI Explanation
          </button>
          <div class="explanation-box" style="display:none;"></div>
        </div>
      ` : ""}
    `;
    breakdown.appendChild(card);
  });
}

function esc(str) {
  return (str || "").replace(/`/g, "\\`").replace(/\$/g, "\\$");
}

// ── AI Explanation ────────────────────────
async function loadExplanation(btn, question, correctAnswer) {
  const wrap = btn.closest(".explain-wrap");
  const box  = wrap.querySelector(".explanation-box");

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Loading…';

  try {
    const res  = await fetch("/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, correct_answer: correctAnswer })
    });
    const data = await res.json();
    box.innerHTML = `<div class="ai-explanation">${data.explanation.replace(/\n/g, "<br>")}</div>`;
    box.style.display = "block";
    btn.style.display = "none";
  } catch {
    btn.textContent = "Retry explanation";
    btn.disabled = false;
  }
}
