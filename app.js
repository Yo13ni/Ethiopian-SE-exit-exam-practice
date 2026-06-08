const SETTINGS_KEY = "practice_settings";
const EXAM_HOURS_DEFAULT = 3;
const EXPLAIN_CACHE_VERSION = 5;
const EXPLAIN_CACHE_VERSION_KEY = "practice_explain_cache_version";
const CATALOG_VERSION = 17;
const COURSES_VERSION = 1;

let catalog = null;
let coursesCatalog = null;
let sessionType = "exam"; // "exam" | "course"
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
let examSkipped = new Set(); // left without answering when navigating away
let timeLeftMs = EXAM_HOURS_DEFAULT * 60 * 60 * 1000;
let timerInterval = null;

// Review mode state
let reviewIndex = 0;
let reviewFilter = null; // null = all, or array of question ids
let reviewQuestions = [];
let reviewAnswers = {}; // question id -> picked key
let reviewAnswered = false;
let lastResult = null;

function sessionStorageId(id = currentExam?.id) {
  if (!id) return "default";
  return sessionType === "course" ? `course_${id}` : id;
}

function examStateKey(id = currentExam?.id, type = sessionType) {
  const sid = type === "course" ? `course_${id}` : id;
  return `practice_${sid}_exam_state`;
}

function lastResultKey(id = currentExam?.id, type = sessionType) {
  const sid = type === "course" ? `course_${id}` : id;
  return `practice_${sid}_last_result`;
}

function storeKey(name) {
  return `practice_${sessionStorageId()}_${name}`;
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

function getExamState(sessionId, type = "exam") {
  try {
    return JSON.parse(localStorage.getItem(examStateKey(sessionId, type)));
  } catch {
    return null;
  }
}

function saveExamState(state) {
  localStorage.setItem(examStateKey(currentExam.id, sessionType), JSON.stringify(state));
}

function getLastResult(sessionId, type = "exam") {
  try {
    return JSON.parse(localStorage.getItem(lastResultKey(sessionId, type)));
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
    sessionType: result.sessionType || sessionType,
  };
  localStorage.setItem(lastResultKey(examId, sessionType), JSON.stringify(slim));
}

function getSummarySessionType() {
  return lastResult?.sessionType || sessionType;
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

function getSessionMeta(sessionId, type = "exam") {
  if (type === "course") {
    return coursesCatalog?.courses?.find((c) => c.id === sessionId) || null;
  }
  return catalog?.exams?.find((e) => e.id === sessionId) || null;
}

function isStaleExamState(sessionId, state, type = "exam") {
  if (!state?.inProgress) return false;
  const meta = getSessionMeta(sessionId, type);
  if (!meta) return false;
  const current = examDataRevision(meta);
  return state.dataRevision == null || state.dataRevision !== current;
}

function cacheBust(url, version) {
  const sep = url.includes("?") ? "&" : "?";
  return `${url}${sep}v=${version}`;
}

async function init() {
  purgeStaleExplainCache();
  const [catRes, coursesRes] = await Promise.all([
    fetch(cacheBust("data/catalog.json", CATALOG_VERSION), { cache: "no-store" }),
    fetch(cacheBust("data/courses.json", COURSES_VERSION), { cache: "no-store" }),
  ]);
  catalog = await catRes.json();
  coursesCatalog = await coursesRes.json();
  renderCourseList();
  renderExamList();
  await checkAiStatus();
}

function renderCourseList() {
  const el = document.getElementById("course-grid");
  if (!el || !coursesCatalog?.courses?.length) return;

  el.innerHTML = coursesCatalog.courses
    .filter((course) => (course.questionCount ?? 0) > 0)
    .map((course) => {
      const state = getExamState(course.id, "course");
      const last = getLastResult(course.id, "course");
      const count = course.questionCount ?? 0;
      const displayTitle = course.shortTitle || course.title;
      let status = "";
      if (state?.inProgress && !isStaleExamState(course.id, state, "course")) {
        const courseMs = getExamTimeMs(course);
        const left = state.timeLeftMs ?? courseMs;
        const answered = Object.keys(state.answers || {}).length;
        status = `In progress · ${answered}/${count} · ${formatTime(left)}`;
      } else if (last) {
        status = `Last: ${last.pct}%`;
      }

      const accent = course.color || "#6366f1";
      return `
      <div class="course-card-wrap" style="--course-accent:${escAttr(accent)}">
        <button type="button" class="course-card" data-course="${escAttr(course.id)}" style="--course-accent:${escAttr(accent)}">
          <span class="course-card-icon" aria-hidden="true">${course.icon || "📘"}</span>
          <span class="course-card-title">${esc(displayTitle)}</span>
          <span class="course-card-count">${count} question${count === 1 ? "" : "s"}</span>
          ${status ? `<span class="course-card-status">${esc(status)}</span>` : ""}
        </button>
        <div class="course-card-actions">
          ${state?.inProgress && !isStaleExamState(course.id, state, "course")
            ? `<button type="button" class="btn primary course-resume" data-id="${escAttr(course.id)}">Resume</button>`
            : `<button type="button" class="btn primary course-start" data-id="${escAttr(course.id)}">Start Practice</button>`}
          <button type="button" class="btn ghost course-review" data-id="${escAttr(course.id)}">Review</button>
          ${last ? `<button type="button" class="btn ghost course-results" data-id="${escAttr(course.id)}">Results</button>` : ""}
        </div>
      </div>`;
    })
    .join("");

  el.querySelectorAll(".course-card").forEach((card) => {
    card.addEventListener("click", (e) => {
      if (e.target.closest(".course-card-actions")) return;
      const id = card.dataset.course;
      const state = getExamState(id, "course");
      if (state?.inProgress && !isStaleExamState(id, state, "course")) {
        startCourse(id, true);
      } else {
        startCourse(id, false);
      }
    });
  });
  el.querySelectorAll(".course-start").forEach((b) =>
    b.addEventListener("click", (e) => {
      e.stopPropagation();
      startCourse(b.dataset.id, false);
    })
  );
  el.querySelectorAll(".course-resume").forEach((b) =>
    b.addEventListener("click", (e) => {
      e.stopPropagation();
      startCourse(b.dataset.id, true);
    })
  );
  el.querySelectorAll(".course-review").forEach((b) =>
    b.addEventListener("click", (e) => {
      e.stopPropagation();
      startReviewMode(b.dataset.id, null, "course");
    })
  );
  el.querySelectorAll(".course-results").forEach((b) => {
    b.addEventListener("click", async (e) => {
      e.stopPropagation();
      const last = getLastResult(b.dataset.id, "course");
      if (last) {
        sessionType = "course";
        currentExam = getSessionMeta(b.dataset.id, "course");
        await loadSessionData(b.dataset.id, "course");
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

function renderExamList() {
  const el = document.getElementById("exam-list");
  el.innerHTML = catalog.exams
    .map((exam) => {
      const state = getExamState(exam.id, "exam");
      const last = getLastResult(exam.id, "exam");
      let status = "Not started";
      if (state?.inProgress && !isStaleExamState(exam.id, state, "exam")) {
        const examMs = getExamTimeMs(exam);
        const left = state.timeLeftMs ?? examMs;
        const answered = Object.keys(state.answers || {}).length;
        status = `In progress · Q${(state.index || 0) + 1} · ${answered} answered · ${formatTime(left)} left`;
      } else if (state?.inProgress && isStaleExamState(exam.id, state, "exam")) {
        status = "Exam updated — start a new attempt";
      } else if (last) {
        status = `Last score: ${last.pct}% (${last.correct}/${last.total})`;
      }
      return `
      <div class="exam-card-wrap">
        <div class="exam-card-title">${esc(exam.title)}</div>
        <div class="exam-card-meta">${status}</div>
        <div class="exam-card-actions">
          ${state?.inProgress && !isStaleExamState(exam.id, state, "exam")
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
      const last = getLastResult(b.dataset.id, "exam");
      if (last) {
        sessionType = "exam";
        currentExam = getSessionMeta(b.dataset.id, "exam");
        await loadSessionData(b.dataset.id, "exam");
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

async function loadSessionData(sessionId, type = sessionType) {
  const meta = getSessionMeta(sessionId, type);
  if (!meta) return false;
  currentExam = meta;
  sessionType = type;
  const rev = examDataRevision(meta);
  const res = await fetch(cacheBust(meta.questionsPath, rev), { cache: "no-store" });
  data = await res.json();
  questions = data.questions || [];
  return true;
}

async function loadExamData(examId) {
  return loadSessionData(examId, "exam");
}

async function startSession(sessionId, resume, type) {
  if (!(await loadSessionData(sessionId, type))) return;

  const label = type === "course" ? "course practice" : "3-hour exam";

  if (resume) {
    const state = getExamState(sessionId, type);
    if (isStaleExamState(sessionId, state, type)) {
      localStorage.removeItem(examStateKey(sessionId, type));
      resume = false;
    }
  }

  if (resume) {
    const state = getExamState(sessionId, type);
    const examMs = getExamTimeMs(currentExam);
    if (state?.inProgress) {
      examIndex = state.index || 0;
      examAnswers = {};
      for (const [k, v] of Object.entries(state.answers || {})) {
        examAnswers[String(k)] = v;
      }
      examFlagged = new Set((state.flagged || []).map(String));
      examSkipped = new Set((state.skipped || []).map(String));
      timeLeftMs = state.timeLeftMs ?? examMs;
    }
  } else {
    const msg =
      type === "course"
        ? `Start ${currentExam.title} practice (${questions.length} questions)? Any in-progress attempt will be replaced.`
        : "Start a new 3-hour exam? Any in-progress attempt will be replaced.";
    if (!confirm(msg)) return;
    examIndex = 0;
    examAnswers = {};
    examFlagged = new Set();
    examSkipped = new Set();
    timeLeftMs = getExamTimeMs(currentExam);
  }

  document.body.classList.add("in-exam");
  const titleBar = document.getElementById("exam-title-bar");
  const subBar = document.getElementById("exam-subtitle-bar");
  const displayTitle =
    type === "course"
      ? `${currentExam.shortTitle || currentExam.title} Practice`
      : data.title || currentExam.title;
  if (titleBar) titleBar.textContent = displayTitle;
  if (subBar) {
    subBar.textContent =
      type === "course"
        ? `${questions.length} Questions · ${label} · ${currentExam.timeLimitHours ?? EXAM_HOURS_DEFAULT}h Timer`
        : `${questions.length} Questions · ${currentExam.timeLimitHours ?? EXAM_HOURS_DEFAULT}h Timer`;
  }

  show("screen-exam");
  startTimer();
  updateExamNav();
  renderExamQuestion();
}

async function startExam(examId, resume) {
  return startSession(examId, resume, "exam");
}

async function startCourse(courseId, resume) {
  return startSession(courseId, resume, "course");
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
  examSkipped.delete(questionKey(q));
}

function markExamSkippedAtIndex(index) {
  const q = questions[index];
  if (!q || getExamAnswer(q)) return;
  examSkipped.add(questionKey(q));
}

function navigateExamQuestion(newIndex) {
  if (newIndex === examIndex) return;
  markExamSkippedAtIndex(examIndex);
  examIndex = newIndex;
  renderExamQuestion();
}

function examLivePillStatus(q) {
  if (getExamAnswer(q)) return "answered";
  if (examSkipped.has(questionKey(q))) return "skipped";
  return "pending";
}

function getExamLiveStats() {
  let skipped = 0;
  let answered = 0;
  questions.forEach((q) => {
    if (getExamAnswer(q)) answered++;
    else if (examSkipped.has(questionKey(q))) skipped++;
  });
  return { skipped, answered, total: questions.length };
}

function computeSessionStats(questionList, getPicked) {
  let correct = 0;
  let attempted = 0;
  questionList.forEach((q) => {
    const picked = getPicked(q);
    if (!picked) return;
    attempted++;
    if (isAnswerCorrect(picked, q.answer)) correct++;
  });
  const total = questionList.length;
  const incorrect = attempted - correct;
  const skipped = total - attempted;
  return { correct, incorrect, attempted, skipped, total };
}

function getReviewStats() {
  return computeSessionStats(reviewQuestions, (q) => reviewAnswers[questionKey(q)]);
}

function normalizeAnswerKey(key) {
  return String(key ?? "").trim().toUpperCase();
}

function isAnswerCorrect(picked, correctAnswer) {
  if (!picked || !correctAnswer) return false;
  return normalizeAnswerKey(picked) === normalizeAnswerKey(correctAnswer);
}

function pillStatus(picked, correctAnswer) {
  if (!picked) return "pending";
  return isAnswerCorrect(picked, correctAnswer) ? "correct" : "wrong";
}

const navDelegates = new Set();

function renderProgressPanel(statsId, stats, mode = "final") {
  const el = document.getElementById(statsId);
  if (!el) return;

  if (mode === "live") {
    const pct = stats.total ? Math.round((stats.answered / stats.total) * 100) : 0;
    el.innerHTML = `
      <p class="progress-headline"><strong>${stats.skipped}</strong> question${stats.skipped === 1 ? "" : "s"} skipped</p>
      <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:${pct}%"></div></div>
      <p class="progress-sub">${stats.answered} of ${stats.total} answered · results hidden until submit</p>`;
    return;
  }

  const pct = stats.total ? Math.round((stats.attempted / stats.total) * 100) : 0;
  const headline =
    stats.attempted > 0
      ? `<strong>${stats.correct}</strong> correct out of <strong>${stats.attempted}</strong> attempted`
      : "Exam submitted";
  el.innerHTML = `
    <p class="progress-headline">${headline}</p>
    <div class="progress-grid">
      <div class="stat-card stat-ok"><span class="stat-val">${stats.correct}</span><span class="stat-lbl">Correct</span></div>
      <div class="stat-card stat-bad"><span class="stat-val">${stats.incorrect}</span><span class="stat-lbl">Incorrect</span></div>
      <div class="stat-card"><span class="stat-val">${stats.skipped}</span><span class="stat-lbl">Skipped</span></div>
      <div class="stat-card"><span class="stat-val">${stats.attempted}</span><span class="stat-lbl">Attempted</span></div>
    </div>
    <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:${pct}%"></div></div>
    <p class="progress-sub">${stats.correct} correct · ${stats.incorrect} incorrect · ${stats.skipped} skipped</p>`;
}

function refreshExamQuestionNav() {
  const nav = document.getElementById("exam-question-nav");
  if (!nav) return;
  questions.forEach((q, i) => {
    const pill = nav.querySelector(`[data-index="${i}"]`);
    if (!pill) return;
    pill.dataset.status = examLivePillStatus(q);
    pill.classList.toggle("is-active", i === examIndex);
    pill.classList.toggle("flagged", examFlagged.has(questionKey(q)));
    const label =
      pill.dataset.status === "answered"
        ? ", answered"
        : pill.dataset.status === "skipped"
          ? ", skipped"
          : "";
    pill.setAttribute("aria-label", `Question ${i + 1}${label}`);
  });
  const active = nav.querySelector(".q-pill.is-active");
  if (active) active.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function updateExamNavLegend() {
  const legend = document.getElementById("exam-nav-legend");
  if (!legend) return;
  legend.innerHTML = `
    <span><i class="dot dot-answered"></i> Answered</span>
    <span><i class="dot dot-skipped"></i> Skipped</span>
    <span><i class="dot dot-pending"></i> Not visited</span>`;
}

function ensureQuestionNav(navId, questionList, onNavigate) {
  const nav = document.getElementById(navId);
  if (!nav) return;
  const navKey = `${sessionType}-${currentExam?.id || "default"}-${questionList.length}`;
  if (nav.dataset.key !== navKey) {
    nav.innerHTML = questionList
      .map(
        (_, i) =>
          `<button type="button" class="q-pill" data-status="pending" data-index="${i}" aria-label="Question ${i + 1}">${i + 1}</button>`
      )
      .join("");
    nav.dataset.key = navKey;
  }
  if (!navDelegates.has(navId)) {
    nav.addEventListener("click", (e) => {
      const btn = e.target.closest(".q-pill");
      if (!btn) return;
      onNavigate(parseInt(btn.dataset.index, 10));
    });
    navDelegates.add(navId);
  }
}

function refreshQuestionNav(navId, questionList, activeIndex, getPicked, flaggedSet = null) {
  const nav = document.getElementById(navId);
  if (!nav) return;
  questionList.forEach((q, i) => {
    const pill = nav.querySelector(`[data-index="${i}"]`);
    if (!pill) return;
    const picked = getPicked(q);
    pill.dataset.status = pillStatus(picked, q.answer);
    pill.classList.toggle("is-active", i === activeIndex);
    pill.classList.toggle("flagged", Boolean(flaggedSet?.has(questionKey(q))));
    const status =
      pill.dataset.status === "correct"
        ? ", correct"
        : pill.dataset.status === "wrong"
          ? ", incorrect"
          : "";
    pill.setAttribute("aria-label", `Question ${i + 1}${status}`);
  });
  const active = nav.querySelector(".q-pill.is-active");
  if (active) active.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function updateExamNav() {
  renderProgressPanel("exam-progress-stats", getExamLiveStats(), "live");
  updateExamNavLegend();
  ensureQuestionNav("exam-question-nav", questions, (idx) => {
    closeSidebar("exam");
    navigateExamQuestion(idx);
  });
  refreshExamQuestionNav();
  const totalEl = document.getElementById("exam-nav-total");
  if (totalEl) totalEl.textContent = `${questions.length} Questions`;
}

function updateReviewNav() {
  const stats = getReviewStats();
  renderProgressPanel("review-progress-stats", stats);
  ensureQuestionNav("review-question-nav", reviewQuestions, (idx) => {
    reviewIndex = idx;
    closeSidebar("review");
    renderReviewQuestion();
  });
  refreshQuestionNav("review-question-nav", reviewQuestions, reviewIndex, (q) =>
    reviewAnswers[questionKey(q)]
  );
  const totalEl = document.getElementById("review-nav-total");
  if (totalEl) totalEl.textContent = `${reviewQuestions.length} Questions`;
}

function closeSidebar(mode) {
  const sidebar = document.getElementById(mode === "exam" ? "exam-sidebar" : "review-sidebar");
  const backdrop = document.getElementById(
    mode === "exam" ? "exam-sidebar-backdrop" : "review-sidebar-backdrop"
  );
  sidebar?.classList.remove("open");
  backdrop?.classList.remove("open");
}

function toggleSidebar(mode) {
  const sidebar = document.getElementById(mode === "exam" ? "exam-sidebar" : "review-sidebar");
  const backdrop = document.getElementById(
    mode === "exam" ? "exam-sidebar-backdrop" : "review-sidebar-backdrop"
  );
  const open = sidebar?.classList.toggle("open");
  backdrop?.classList.toggle("open", open);
}

function persistExamState() {
  saveExamState({
    inProgress: true,
    examId: currentExam.id,
    index: examIndex,
    answers: examAnswers,
    flagged: [...examFlagged],
    skipped: [...examSkipped],
    timeLeftMs,
    dataRevision: examDataRevision(currentExam),
    startedAt: getExamState(currentExam.id, sessionType)?.startedAt || Date.now(),
  });
}

function renderExamQuestion() {
  const q = questions[examIndex];
  const pct = ((examIndex + 1) / questions.length) * 100;
  document.getElementById("bar").style.width = `${pct}%`;
  document.getElementById("counter").textContent = `Q ${examIndex + 1} / ${questions.length}`;
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
      updateExamNav();
      renderExamQuestion();
      persistExamState();
    });
    container.appendChild(btn);
  });

  document.getElementById("btn-prev").disabled = examIndex === 0;
  document.getElementById("btn-next-exam").textContent =
    examIndex === questions.length - 1 ? "Finish" : "Next";
  document.getElementById("btn-flag").classList.toggle("flagged", examFlagged.has(questionKey(q)));
  updateExamNav();
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
    } else if (isAnswerCorrect(picked, q.answer)) {
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

  const sessionTitle =
    sessionType === "course"
      ? `${currentExam.shortTitle || currentExam.title} Practice`
      : data.title || currentExam.title;

  return {
    date: new Date().toISOString(),
    examId: currentExam.id,
    sessionType,
    examTitle: sessionTitle,
    pct,
    correct,
    incorrect: answered - correct,
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
  markExamSkippedAtIndex(examIndex);
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

async function startReviewMode(sessionId, filterIds, type = "exam") {
  if (!(await loadSessionData(sessionId, type))) return;
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
  reviewAnswers = {};
  document.body.classList.add("in-exam");
  const reviewTitle = document.getElementById("review-exam-title");
  if (reviewTitle) {
    reviewTitle.textContent =
      type === "course"
        ? `${currentExam.shortTitle || currentExam.title} · Review`
        : data.title || currentExam.title;
  }
  show("screen-review");
  updateReviewNav();
  renderReviewQuestion();
}

function renderReviewQuestion() {
  const q = reviewQuestions[reviewIndex];
  const picked = reviewAnswers[questionKey(q)];
  reviewAnswered = Boolean(picked);
  const pct = ((reviewIndex + 1) / reviewQuestions.length) * 100;

  document.getElementById("review-bar").style.width = `${pct}%`;
  document.getElementById("review-counter").textContent = `Q ${reviewIndex + 1} / ${reviewQuestions.length}`;
  const topicLabel =
    sessionType === "course" && q.sourceExamTitle
      ? `${q.sourceExamTitle} · ${q.topic}`
      : `${currentExam.title} · ${q.topic}`;
  document.getElementById("review-topic-badge").textContent = topicLabel;
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
    if (picked) {
      btn.disabled = true;
      if (opt.key === q.answer) btn.classList.add("correct");
      else if (opt.key === picked) btn.classList.add("wrong");
      else btn.classList.add("dim");
    } else {
      btn.addEventListener("click", () => pickReview(opt.key));
    }
    container.appendChild(btn);
  });

  if (picked) {
    const isCorrect = picked === q.answer;
    showReviewFeedback(q, picked);
    document.getElementById("explain-loading").classList.remove("hidden");
    fetchExplanation(q, picked).then((exp) => {
      if (reviewQuestions[reviewIndex] !== q) return;
      renderExplanation(q, picked, q.answer, isCorrect, exp);
    });
  }

  updateReviewNav();

  document.getElementById("btn-prev-review").disabled = reviewIndex === 0;
  document.getElementById("btn-next-review-footer").textContent =
    reviewIndex === reviewQuestions.length - 1 ? "Done" : "Next";
}

function showReviewFeedback(q, picked) {
  const correct = q.answer;
  const isCorrect = picked === correct;

  document.getElementById("result-banner").className = "result-banner " + (isCorrect ? "ok" : "no");
  document.getElementById("result-banner").textContent = isCorrect
    ? "Correct — explanation below"
    : `Incorrect — correct answer is ${correct}`;

  document.getElementById("feedback").classList.remove("hidden");
  document.getElementById("btn-next-review").disabled = false;
  document.getElementById("btn-next-review").textContent =
    reviewIndex === reviewQuestions.length - 1 ? "Finish Review" : "Next Question";
}

async function pickReview(key) {
  if (reviewAnswered) return;
  reviewAnswered = true;
  const q = reviewQuestions[reviewIndex];
  reviewAnswers[questionKey(q)] = key;
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

  updateReviewNav();

  const exp = await fetchExplanation(q, key);
  renderExplanation(q, key, correct, isCorrect, exp);
}

function explainExamId(q) {
  return q.sourceExamId || currentExam.id;
}

function cacheKey(q, picked) {
  return `v${EXPLAIN_CACHE_VERSION}_${explainExamId(q)}_${q.examNumber}_${picked}_${settings.useAi ? "ai" : "off"}`;
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
        examId: explainExamId(q),
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

function renderSummaryQuestionStrip(result) {
  const strip = document.getElementById("summary-question-nav");
  if (!strip || !questions.length) return;

  strip.innerHTML = questions
    .map((q, i) => {
      const key = questionKey(q);
      const missed = (result.sessionMissed || []).find((m) => String(m.id) === key);
      let status = "correct";
      if (missed) {
        status = missed.reason === "unanswered" || missed.picked == null ? "skipped" : "wrong";
      }
      return `<span class="q-pill" data-status="${status}" title="Q${i + 1}">${i + 1}</span>`;
    })
    .join("");
}

function renderSummary(result) {
  const scoreEl = document.getElementById("final-score");
  scoreEl.textContent = `${result.pct}%`;
  scoreEl.className = "big-score" + (result.pct >= 70 ? " score-pass" : result.pct >= 50 ? " score-mid" : " score-low");

  const answeredCount = result.answered ?? result.total - (result.unanswered ?? 0);
  const incorrect = result.incorrect ?? answeredCount - result.correct;
  const skipped = result.unanswered ?? result.total - answeredCount;

  renderProgressPanel("summary-progress-stats", {
    correct: result.correct,
    incorrect,
    attempted: answeredCount,
    skipped,
    total: result.total,
  });

  document.getElementById("final-text").textContent =
    `${result.examTitle} — Final score ${result.pct}%`;

  renderSummaryQuestionStrip(result);
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
  document.body.classList.toggle("in-exam", id === "screen-exam" || id === "screen-review");
  if (id === "screen-home") {
    renderCourseList();
    renderExamList();
  }
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
  if (examIndex > 0) navigateExamQuestion(examIndex - 1);
});
document.getElementById("btn-next-exam").addEventListener("click", () => {
  if (examIndex < questions.length - 1) navigateExamQuestion(examIndex + 1);
  else submitExam(false);
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
  if (currentExam) startReviewMode(currentExam.id, null, getSummarySessionType());
});
document.getElementById("btn-review-missed-only").addEventListener("click", () => {
  if (lastResult?.sessionMissed?.length) {
    startReviewMode(
      currentExam.id,
      lastResult.sessionMissed.map((m) => m.id),
      getSummarySessionType()
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

document.getElementById("btn-toggle-exam-nav")?.addEventListener("click", () => toggleSidebar("exam"));
document.getElementById("btn-toggle-review-nav")?.addEventListener("click", () => toggleSidebar("review"));
document.getElementById("exam-sidebar-backdrop")?.addEventListener("click", () => closeSidebar("exam"));
document.getElementById("review-sidebar-backdrop")?.addEventListener("click", () => closeSidebar("review"));

init();
