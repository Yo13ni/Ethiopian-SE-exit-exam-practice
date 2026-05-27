const SETTINGS_KEY = "practice_settings";
const EXAM_HOURS_DEFAULT = 3;
const EXPLAIN_CACHE_VERSION = 5;
const EXPLAIN_CACHE_VERSION_KEY = "practice_explain_cache_version";
const CATALOG_VERSION = 11;

let catalog = null;
let currentExam = null;
let data = null;
let questions = [];
let settings = loadSettings();

function getExamTimeMs(exam) {
  const hours = exam?.timeLimitHours ?? EXAM_HOURS_DEFAULT;
  return hours * 60 * 60 * 1000;
}

// Exam mode state
let examIndex = 0;
let examAnswers = {}; // question id -> selected key
let examFlagged = new Set();
let timeLeftMs = EXAM_HOURS_DEFAULT * 60 * 60 * 1000;
let timerInterval = null;

// Review mode state
let reviewIndex = 0;
let reviewFilter = null; // null = all, or array of question ids
let reviewQuestions = [];
let reviewAnswered = false;
let lastResult = null;

function storeKey(name) {
  return `practice_${currentExam?.id || "default"}_${name}`;
}

function purgeStaleExplainCache() {
  try {
    const stored = parseInt(localStorage.getItem(EXPLAIN_CACHE_VERSION_KEY) || "0", 10);
    if (stored >= EXPLAIN_CACHE_VERSION) return;
    for (let i = localStorage.length - 1; i >= 0; i--) {
      const key = localStorage.key(i);
      if (key && key.includes("_explain_cache")) localStorage.removeItem(key);
    }
    localStorage.setItem(EXPLAIN_CACHE_VERSION_KEY, String(EXPLAIN_CACHE_VERSION));
  } catch { /* ignore */ }
}

function loadSettings() {
  try {
    return JSON.parse(localStorage.getItem(SETTINGS_KEY)) || {
      apiKey: "",
      baseUrl: "https://api.openai.com/v1",
      model: "gpt-4o-mini",
      useAi: true,
    };
  } catch {
    return { apiKey: "", baseUrl: "https://api.openai.com/v1", model: "gpt-4o-mini", useAi: true };
  }
}

function saveSettings(s) {
  settings = s;
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(s));
}

function getExamState(examId) {
  try {
    return JSON.parse(localStorage.getItem(`practice_${examId}_exam_state`));
  } catch {
    return null;
  }
}

function saveExamState(state) {
  localStorage.setItem(`practice_${currentExam.id}_exam_state`, JSON.stringify(state));
}

function getLastResult(examId) {
  try {
    return JSON.parse(localStorage.getItem(`practice_${examId}_last_result`));
  } catch {
    return null;
  }
}

function saveLastResult(examId, result) {
  // Slim payload — full question text + examAnswers can exceed localStorage quota
  const slim = {
    date: result.date,
    examId: result.examId,
    examTitle: result.examTitle,
    pct: result.pct,
    correct: result.correct,
    total: result.total,
    answered: result.answered,
    unanswered: result.unanswered,
    topicBreakdown: result.topicBreakdown,
    weakTopics: result.weakTopics,
    sessionMissed: (result.sessionMissed || []).map((m) => ({
      id: m.id,
      topic: m.topic,
      picked: m.picked,
      answer: m.answer,
      text: String(m.text || "").slice(0, 180),
      reason: m.reason,
    })),
    focusGuide: result.focusGuide,
    timeUsedMs: result.timeUsedMs,
  };
  localStorage.setItem(`practice_${examId}_last_result`, JSON.stringify(slim));
}

function formatTime(ms) {
  if (ms <= 0) return "0:00:00";
  const s = Math.floor(ms / 1000);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
}

function examDataRevision(exam) {
  return exam?.dataRevision ?? 1;
}

function isStaleExamState(examId, state) {
  if (!state?.inProgress) return false;
  const exam = catalog?.exams?.find((e) => e.id === examId);
  if (!exam) return false;
  const current = examDataRevision(exam);
  return state.dataRevision == null || state.dataRevision !== current;
}

function cacheBust(url, version) {
  const sep = url.includes("?") ? "&" : "?";
  return `${url}${sep}v=${version}`;
}

async function init() {
  purgeStaleExplainCache();
  const catRes = await fetch(cacheBust("data/catalog.json", CATALOG_VERSION), { cache: "no-store" });
  catalog = await catRes.json();
  renderExamList();
  await checkAiStatus();
}

function renderExamList() {
  const el = document.getElementById("exam-list");
  el.innerHTML = catalog.exams
    .map((exam) => {
      const state = getExamState(exam.id);
      const last = getLastResult(exam.id);
      let status = "Not started";
      if (state?.inProgress && !isStaleExamState(exam.id, state)) {
        const examMs = getExamTimeMs(exam);
        const left = state.timeLeftMs ?? examMs;
        const answered = Object.keys(state.answers || {}).length;
        status = `In progress · Q${(state.index || 0) + 1} · ${answered} answered · ${formatTime(left)} left`;
      } else if (state?.inProgress && isStaleExamState(exam.id, state)) {
        status = "Exam updated — start a new attempt";
      } else if (last) {
        status = `Last score: ${last.pct}% (${last.correct}/${last.total})`;
      }
      return `
      <div class="exam-card-wrap">
        <div class="exam-card-title">${esc(exam.title)}</div>
        <div class="exam-card-meta">${status}</div>
        <div class="exam-card-actions">
          ${state?.inProgress && !isStaleExamState(exam.id, state)
            ? `<button type="button" class="btn primary exam-resume" data-id="${escAttr(exam.id)}">Resume Exam</button>`
            : `<button type="button" class="btn primary exam-start" data-id="${escAttr(exam.id)}">Start Exam (3h)</button>`}
          <button type="button" class="btn ghost exam-review" data-id="${escAttr(exam.id)}">Review Mode</button>
          ${last ? `<button type="button" class="btn ghost exam-results" data-id="${escAttr(exam.id)}">View Results</button>` : ""}
        </div>
      </div>`;
    })
    .join("");

  el.querySelectorAll(".exam-start").forEach((b) =>
    b.addEventListener("click", () => startExam(b.dataset.id, false))
  );
  el.querySelectorAll(".exam-resume").forEach((b) =>
    b.addEventListener("click", () => startExam(b.dataset.id, true))
  );
  el.querySelectorAll(".exam-review").forEach((b) =>
    b.addEventListener("click", () => startReviewMode(b.dataset.id, null))
  );
  el.querySelectorAll(".exam-results").forEach((b) => {
    b.addEventListener("click", async () => {
      const last = getLastResult(b.dataset.id);
      if (last) {
        currentExam = catalog.exams.find((e) => e.id === b.dataset.id);
        await loadExamData(b.dataset.id);
        lastResult = last;
        if (!lastResult.focusGuide || !Object.keys(lastResult.focusGuide).length) {
          lastResult.focusGuide = data?.focusGuide || {};
        }
        renderSummary(lastResult);
        show("screen-summary");
        window.scrollTo(0, 0);
      }
    });
  });
}

async function loadExamData(examId) {
  const meta = catalog.exams.find((e) => e.id === examId);
  if (!meta) return false;
  currentExam = meta;
  const rev = examDataRevision(meta);
  const res = await fetch(cacheBust(meta.questionsPath, rev), { cache: "no-store" });
  data = await res.json();
  questions = data.questions;
  return true;
}

async function startExam(examId, resume) {
  if (!(await loadExamData(examId))) return;

  if (resume) {
    const state = getExamState(examId);
    if (isStaleExamState(examId, state)) {
      localStorage.removeItem(`practice_${examId}_exam_state`);
      resume = false;
    }
  }

  if (resume) {
    const state = getExamState(examId);
    const examMs = getExamTimeMs(currentExam);
    if (state?.inProgress) {
      examIndex = state.index || 0;
      examAnswers = {};
      for (const [k, v] of Object.entries(state.answers || {})) {
        examAnswers[String(k)] = v;
      }
      examFlagged = new Set((state.flagged || []).map(String));
      timeLeftMs = state.timeLeftMs ?? examMs;
    }
  } else {
    if (!confirm("Start a new 3-hour exam? Any in-progress attempt will be replaced.")) return;
    examIndex = 0;
    examAnswers = {};
    examFlagged = new Set();
    timeLeftMs = getExamTimeMs(currentExam);
  }

  show("screen-exam");
  startTimer();
  renderExamQuestion();
}

function startTimer() {
  stopTimer();
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    timeLeftMs -= 1000;
    if (timeLeftMs <= 0) {
      timeLeftMs = 0;
      stopTimer();
      submitExam(true);
      return;
    }
    updateTimerDisplay();
    persistExamState();
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function updateTimerDisplay() {
  const el = document.getElementById("timer");
  el.textContent = formatTime(timeLeftMs);
  el.classList.toggle("timer-warn", timeLeftMs < 15 * 60 * 1000);
  el.classList.toggle("timer-critical", timeLeftMs < 5 * 60 * 1000);
}

function questionKey(q) {
  return String(q.id ?? q.examNumber);
}

function getExamAnswer(q) {
  return examAnswers[questionKey(q)];
}

function setExamAnswer(q, key) {
  examAnswers[questionKey(q)] = key;
}

function persistExamState() {
  saveExamState({
    inProgress: true,
    examId: currentExam.id,
    index: examIndex,
    answers: examAnswers,
    flagged: [...examFlagged],
    timeLeftMs,
    dataRevision: examDataRevision(currentExam),
    startedAt: getExamState(currentExam.id)?.startedAt || Date.now(),
  });
}

function renderExamQuestion() {
  const q = questions[examIndex];
  const pct = ((examIndex + 1) / questions.length) * 100;
  document.getElementById("bar").style.width = `${pct}%`;
  document.getElementById("counter").textContent = `${examIndex + 1} / ${questions.length}`;
  document.getElementById("topic-badge").textContent = q.topic;
  document.getElementById("q-text").textContent = q.text;

  const selected = getExamAnswer(q);
  const container = document.getElementById("choices");
  container.innerHTML = "";
  q.options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.type = "button";
    const isSelected = selected === opt.key;
    btn.className = "choice" + (isSelected ? " selected" : "");
    btn.setAttribute("aria-pressed", isSelected ? "true" : "false");
    btn.innerHTML = `<span class="key">${opt.key}</span><span>${esc(opt.text)}</span>`;
    btn.addEventListener("click", () => {
      setExamAnswer(q, opt.key);
      renderExamQuestion();
      persistExamState();
    });
    container.appendChild(btn);
  });

  document.getElementById("btn-prev").disabled = examIndex === 0;
  document.getElementById("btn-next-exam").textContent =
    examIndex === questions.length - 1 ? "Finish" : "Next";
  document.getElementById("btn-flag").classList.toggle("flagged", examFlagged.has(questionKey(q)));
  persistExamState();
}

function buildExamResult() {
  let correct = 0;
  let unansweredCount = 0;
  const topicStats = {};
  const sessionMissed = [];

  questions.forEach((q) => {
    const picked = getExamAnswer(q);
    if (!topicStats[q.topic]) {
      topicStats[q.topic] = { correct: 0, total: 0, wrong: 0, unanswered: 0 };
    }
    const ts = topicStats[q.topic];
    ts.total++;

    if (!picked) {
      ts.unanswered++;
      unansweredCount++;
      sessionMissed.push({
        id: q.id,
        examNumber: q.examNumber,
        text: q.text,
        topic: q.topic,
        picked: null,
        answer: q.answer,
        reason: "unanswered",
      });
    } else if (picked === q.answer) {
      correct++;
      ts.correct++;
    } else {
      ts.wrong++;
      sessionMissed.push({
        id: q.id,
        examNumber: q.examNumber,
        text: q.text,
        topic: q.topic,
        picked,
        answer: q.answer,
        reason: "wrong",
      });
    }
  });

  const total = questions.length;
  const answered = total - unansweredCount;
  const pct = total ? Math.round((correct / total) * 100) : 0;

  const topicBreakdown = Object.entries(topicStats)
    .map(([topic, s]) => ({
      topic,
      correct: s.correct,
      wrong: s.wrong,
      unanswered: s.unanswered,
      total: s.total,
      missed: s.wrong + s.unanswered,
      pct: Math.round((s.correct / s.total) * 100),
    }))
    .sort((a, b) => a.pct - b.pct || b.missed - a.missed);

  const weakTopics = topicBreakdown.filter((t) => t.missed > 0);

  return {
    date: new Date().toISOString(),
    examId: currentExam.id,
    examTitle: data.title || currentExam.title,
    pct,
    correct,
    total,
    answered,
    unanswered: unansweredCount,
    topicBreakdown,
    weakTopics,
    sessionMissed,
    focusGuide: data?.focusGuide || {},
    timeUsedMs: getExamTimeMs(currentExam) - timeLeftMs,
  };
}

function submitExam(auto = false) {
  const unanswered = questions.filter((q) => !getExamAnswer(q)).length;
  if (!auto && unanswered > 0) {
    if (!confirm(`${unanswered} question(s) unanswered. Submit anyway?`)) return;
  }
  stopTimer();

  lastResult = buildExamResult();

  // Always show results first — storage failures must not block the summary screen
  renderSummary(lastResult);
  show("screen-summary");
  window.scrollTo(0, 0);

  let saveOk = true;
  try {
    saveLastResult(currentExam.id, lastResult);
    saveExamState({ inProgress: false, examId: currentExam.id });
  } catch (e) {
    saveOk = false;
    console.warn("Could not save exam result to browser storage:", e);
  }
  const warnEl = document.getElementById("summary-save-warn");
  if (warnEl) {
    warnEl.classList.toggle("hidden", saveOk);
    if (!saveOk) {
      warnEl.textContent =
        "Results shown below but could not be saved (browser storage full). Screenshot this page or review now.";
    }
  }
}

async function startReviewMode(examId, filterIds) {
  if (!(await loadExamData(examId))) return;
  reviewFilter = filterIds;
  if (filterIds) {
    reviewQuestions = questions.filter((q) => filterIds.includes(q.id));
  } else {
    reviewQuestions = [...questions];
  }
  if (!reviewQuestions.length) {
    alert("No questions to review.");
    return;
  }
  reviewIndex = 0;
  show("screen-review");
  renderReviewQuestion();
}

function renderReviewQuestion() {
  reviewAnswered = false;
  const q = reviewQuestions[reviewIndex];
  const pct = ((reviewIndex + 1) / reviewQuestions.length) * 100;

  document.getElementById("review-bar").style.width = `${pct}%`;
  document.getElementById("review-counter").textContent = `${reviewIndex + 1} / ${reviewQuestions.length}`;
  document.getElementById("review-topic-badge").textContent = `${currentExam.title} · ${q.topic}`;
  document.getElementById("review-q-text").textContent = q.text;

  document.getElementById("feedback").classList.add("hidden");
  document.getElementById("explain-loading").classList.add("hidden");
  document.getElementById("explain-body").classList.add("hidden");
  document.getElementById("btn-next-review").disabled = true;

  const container = document.getElementById("review-choices");
  container.innerHTML = "";
  q.options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "choice";
    btn.innerHTML = `<span class="key">${opt.key}</span><span>${esc(opt.text)}</span>`;
    btn.addEventListener("click", () => pickReview(opt.key));
    container.appendChild(btn);
  });

  document.getElementById("btn-prev-review").disabled = reviewIndex === 0;
  document.getElementById("btn-next-review-footer").textContent =
    reviewIndex === reviewQuestions.length - 1 ? "Done" : "Next";
}

async function pickReview(key) {
  if (reviewAnswered) return;
  reviewAnswered = true;
  const q = reviewQuestions[reviewIndex];
  const correct = q.answer;
  const isCorrect = key === correct;

  document.querySelectorAll("#review-choices .choice").forEach((btn) => {
    btn.disabled = true;
    const k = btn.querySelector(".key").textContent;
    if (k === correct) btn.classList.add("correct");
    else if (k === key) btn.classList.add("wrong");
    else btn.classList.add("dim");
  });

  document.getElementById("result-banner").className = "result-banner " + (isCorrect ? "ok" : "no");
  document.getElementById("result-banner").textContent = isCorrect
    ? "Correct — loading explanation…"
    : `Incorrect — correct answer is ${correct}`;

  document.getElementById("feedback").classList.remove("hidden");
  document.getElementById("explain-loading").classList.remove("hidden");
  document.getElementById("explain-body").classList.add("hidden");

  const exp = await fetchExplanation(q, key);
  renderExplanation(q, key, correct, isCorrect, exp);
}

function cacheKey(q, picked) {
  return `v${EXPLAIN_CACHE_VERSION}_${currentExam.id}_${q.examNumber}_${picked}_${settings.useAi ? "ai" : "off"}`;
}

async function fetchExplanation(q, userPick) {
  const ck = cacheKey(q, userPick);
  try {
    const cache = JSON.parse(localStorage.getItem(storeKey("explain_cache")) || "{}");
    if (cache[ck]) return cache[ck];
  } catch { /* ignore */ }

  try {
    const res = await fetch("/api/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        examId: currentExam.id,
        examTitle: data.title || currentExam.title,
        examNumber: q.examNumber,
        question: q.text,
        options: q.options.map((o) => ({ key: o.key, text: o.text })),
        answer: q.answer,
        userPick,
        topic: q.topic,
        apiKey: settings.apiKey,
        baseUrl: settings.baseUrl,
        model: settings.model,
        useAi: settings.useAi,
      }),
    });
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || res.statusText);
    const result = await res.json();
    // Only cache live AI responses; offline guides are always fetched fresh.
    if (result.source === "ai-live") {
      try {
        const cache = JSON.parse(localStorage.getItem(storeKey("explain_cache")) || "{}");
        cache[ck] = result;
        localStorage.setItem(storeKey("explain_cache"), JSON.stringify(cache));
      } catch { /* ignore */ }
    }
    return result;
  } catch (e) {
    return {
      overview: q.concept || "Could not load explanation.",
      options: Object.fromEntries(q.options.map((o) => [o.key, o.text])),
      studyTip: "Check server is running.",
      source: "error-fallback",
    };
  }
}

function renderExplanation(q, picked, correct, isCorrect, exp) {
  document.getElementById("explain-loading").classList.add("hidden");
  document.getElementById("explain-body").classList.remove("hidden");
  document.getElementById("btn-next-review").disabled = false;
  document.getElementById("btn-next-review").textContent =
    reviewIndex === reviewQuestions.length - 1 ? "Finish Review" : "Next Question";

  document.getElementById("result-banner").className = "result-banner " + (isCorrect ? "ok" : "no");
  document.getElementById("result-banner").textContent = isCorrect
    ? "Correct — read the breakdown below"
    : `Incorrect — correct answer is ${correct}`;

  document.getElementById("concept").innerHTML = formatText(exp.overview || "");
  const labels = {
    "ai-live": "Live AI tutor",
    "offline-deep": "Detailed curated explanation",
    "offline-fallback": "Basic explanation",
  };
  document.getElementById("explain-source").textContent = labels[exp.source] || exp.source || "";

  document.getElementById("explanations").innerHTML = q.options
    .map((opt) => {
      const text = (exp.options && exp.options[opt.key]) || opt.text;
      let cls = "neutral";
      let label = `Option ${opt.key}`;
      if (opt.key === correct) {
        cls = "ok";
        label = `Option ${opt.key} — Correct`;
      } else if (opt.key === picked) {
        cls = "bad";
        label = `Option ${opt.key} — Your choice`;
      }
      const itemCls =
        opt.key === correct ? "exp-item is-answer" : opt.key === picked ? "exp-item is-wrong-pick" : "exp-item";
      return `<div class="${itemCls}"><div class="exp-label ${cls}">${label}</div><div class="exp-text">${formatText(text)}</div><div class="exp-option-ref">${esc(opt.text)}</div></div>`;
    })
    .join("");

  const tip = exp.studyTip || "";
  document.getElementById("study-tip").innerHTML = tip ? `<strong>Study tip:</strong> ${formatText(tip)}` : "";
}

function formatText(text) {
  return esc(String(text))
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>")
    .replace(/^/, "<p>")
    .replace(/$/, "</p>");
}

function nextReview() {
  if (reviewIndex < reviewQuestions.length - 1) {
    reviewIndex++;
    renderReviewQuestion();
  } else {
    show("screen-home");
  }
}

function prevReview() {
  if (reviewIndex > 0) {
    reviewIndex--;
    renderReviewQuestion();
  }
}

function renderSummary(result) {
  const scoreEl = document.getElementById("final-score");
  scoreEl.textContent = `${result.pct}%`;
  scoreEl.className = "big-score" + (result.pct >= 70 ? " score-pass" : result.pct >= 50 ? " score-mid" : " score-low");

  const unanswered = result.unanswered ?? result.total - (result.answered ?? result.total);
  document.getElementById("final-text").textContent =
    `${result.examTitle}: ${result.correct} / ${result.total} correct · ${result.answered ?? result.total - unanswered} answered · ${unanswered} skipped`;
  document.getElementById("summary-date").textContent = result.date
    ? `Completed: ${new Date(result.date).toLocaleString()} · Time used: ${formatTime(result.timeUsedMs || 0)}`
    : "";

  const guides = result.focusGuide || {};
  let breakdown = result.topicBreakdown;
  if (!breakdown?.length && result.weakTopics?.length) {
    breakdown = result.weakTopics.map((t) => ({
      topic: t.topic,
      pct: t.pct ?? 0,
      correct: Math.max(0, (t.total ?? t.missed ?? 0) - (t.missed ?? 0)),
      wrong: t.missed ?? 0,
      unanswered: 0,
      total: t.total ?? t.missed ?? 0,
      missed: t.missed ?? 0,
    }));
  }
  breakdown = breakdown || [];
  const weak = breakdown.filter((t) => (t.missed ?? t.total - t.correct) > 0);

  document.getElementById("topic-breakdown").innerHTML = !breakdown.length
    ? '<p class="empty">No topic data.</p>'
    : breakdown
        .map((t) => {
          const missed = t.missed ?? (t.wrong || 0) + (t.unanswered || 0);
          const barClass = t.pct >= 70 ? "bar-ok" : t.pct >= 50 ? "bar-mid" : "bar-low";
          const parts = [];
          if (t.wrong) parts.push(`${t.wrong} wrong`);
          if (t.unanswered) parts.push(`${t.unanswered} skipped`);
          return `<div class="topic-row">
            <div class="topic-row-head">
              <span class="topic-name">${esc(t.topic)}</span>
              <span class="topic-pct ${barClass}">${t.pct}%</span>
            </div>
            <div class="topic-bar-track"><div class="topic-bar-fill ${barClass}" style="width:${t.pct}%"></div></div>
            <div class="topic-meta">${t.correct}/${t.total} correct${parts.length ? " · " + parts.join(" · ") : ""}</div>
          </div>`;
        })
        .join("");

  document.getElementById("focus-areas").innerHTML = !weak.length
    ? `<p class="empty">${result.pct === 100 ? "Perfect score — no weak areas!" : "Review skipped questions below."}</p>`
    : weak
        .slice(0, 8)
        .map((t) => {
          const missed = t.missed ?? (t.wrong || 0) + (t.unanswered || 0);
          const guide = guides[t.topic] || guides.General || "Review lecture notes and practice similar MCQs for this topic.";
          return `<div class="focus-row">
            <div class="focus-name">${esc(t.topic)} — ${t.pct}% (${missed} to improve)</div>
            <div class="focus-detail">${esc(guide)}</div>
          </div>`;
        })
        .join("");

  const missed = result.sessionMissed || [];
  document.getElementById("review-list").innerHTML = !missed.length
    ? '<p class="empty">Perfect score — no missed questions!</p>'
    : missed
        .map((m, i) => {
          const label =
            m.reason === "unanswered" || m.picked == null
              ? "Skipped"
              : `You: ${m.picked} → Correct: ${m.answer}`;
          return `<div class="review-item">${i + 1}. ${esc(String(m.text || "").slice(0, 120))}${String(m.text || "").length > 120 ? "…" : ""}<br><small style="color:var(--muted)">${label} · ${esc(m.topic)}</small></div>`;
        })
        .join("");

  document.getElementById("btn-review-missed-only").style.display =
    missed.length > 0 ? "inline-flex" : "none";
}

function show(id) {
  document.querySelectorAll(".screen").forEach((s) => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  if (id === "screen-home") renderExamList();
}

async function checkAiStatus() {
  const el = document.getElementById("ai-status");
  try {
    const h = await (await fetch("/api/health")).json();
    const total = Object.values(h.deepCounts || {}).reduce((a, b) => a + b, 0);
    el.textContent = settings.apiKey || h.hasEnvKey
      ? `AI tutor ready · ${total} offline guides`
      : `${total} detailed offline explanations in Review mode`;
  } catch {
    el.textContent = "Run server.py to enable explanations";
  }
}

function openSettings() {
  document.getElementById("api-key").value = settings.apiKey || "";
  document.getElementById("api-base").value = settings.baseUrl || "https://api.openai.com/v1";
  document.getElementById("api-model").value = settings.model || "gpt-4o-mini";
  document.getElementById("use-ai").checked = settings.useAi !== false;
  document.getElementById("settings-dialog").showModal();
}

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function escAttr(s) {
  return String(s).replace(/"/g, "&quot;");
}

// Event listeners
document.getElementById("btn-prev").addEventListener("click", () => {
  if (examIndex > 0) {
    examIndex--;
    renderExamQuestion();
  }
});
document.getElementById("btn-next-exam").addEventListener("click", () => {
  if (examIndex < questions.length - 1) {
    examIndex++;
    renderExamQuestion();
  } else {
    submitExam(false);
  }
});
document.getElementById("btn-submit-exam").addEventListener("click", () => submitExam(false));
document.getElementById("btn-flag").addEventListener("click", () => {
  const q = questions[examIndex];
  const id = questionKey(q);
  if (examFlagged.has(id)) examFlagged.delete(id);
  else examFlagged.add(id);
  renderExamQuestion();
});

document.getElementById("btn-prev-review").addEventListener("click", prevReview);
document.getElementById("btn-next-review").addEventListener("click", nextReview);
document.getElementById("btn-next-review-footer").addEventListener("click", () => {
  if (reviewAnswered) nextReview();
  else alert("Select an answer first to see the explanation.");
});

document.getElementById("btn-review-answers").addEventListener("click", () => {
  if (currentExam) startReviewMode(currentExam.id, null);
});
document.getElementById("btn-review-missed-only").addEventListener("click", () => {
  if (lastResult?.sessionMissed?.length) {
    startReviewMode(
      currentExam.id,
      lastResult.sessionMissed.map((m) => m.id)
    );
  }
});
document.getElementById("btn-back-home").addEventListener("click", () => show("screen-home"));

document.getElementById("btn-settings").addEventListener("click", openSettings);
document.getElementById("btn-settings-review").addEventListener("click", openSettings);
document.getElementById("settings-form").addEventListener("submit", (e) => {
  e.preventDefault();
  saveSettings({
    apiKey: document.getElementById("api-key").value.trim(),
    baseUrl: document.getElementById("api-base").value.trim() || "https://api.openai.com/v1",
    model: document.getElementById("api-model").value.trim() || "gpt-4o-mini",
    useAi: document.getElementById("use-ai").checked,
  });
  document.getElementById("settings-dialog").close();
  checkAiStatus();
});
document.getElementById("btn-clear-key").addEventListener("click", () => {
  document.getElementById("api-key").value = "";
});

init();
