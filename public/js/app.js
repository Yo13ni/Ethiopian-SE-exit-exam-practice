const EXAM_HOURS_DEFAULT = 3;
const EXPLAIN_CACHE_VERSION = 11;
const EXPLAIN_CACHE_VERSION_KEY = "practice_explain_cache_version";
const CATALOG_VERSION = 23;
const SUBJECTS_VERSION = 4;

let catalog = null;
let currentExam = null;
let data = null;
let questions = [];

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

let subjectData = null;
let currentSubjectSlug = null;
let currentSubjectQuestions = [];
let subjectAnswers = {};

function sessionStorageId(id = currentExam?.id) {
  return id || "default";
}

function examStateKey(id = currentExam?.id) {
  return `practice_${id}_exam_state`;
}

function lastResultKey(id = currentExam?.id) {
  return `practice_${id}_last_result`;
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

function getExamState(sessionId) {
  try {
    return JSON.parse(localStorage.getItem(examStateKey(sessionId)));
  } catch {
    return null;
  }
}

function saveExamState(state) {
  localStorage.setItem(examStateKey(currentExam.id), JSON.stringify(state));
}

function getLastResult(sessionId) {
  try {
    return JSON.parse(localStorage.getItem(lastResultKey(sessionId)));
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
  localStorage.setItem(lastResultKey(examId), JSON.stringify(slim));
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

function getSessionMeta(sessionId) {
  return catalog?.exams?.find((e) => e.id === sessionId) || null;
}

function isStaleExamState(sessionId, state) {
  if (!state?.inProgress) return false;
  const meta = getSessionMeta(sessionId);
  if (!meta) return false;
  const current = examDataRevision(meta);
  return state.dataRevision == null || state.dataRevision !== current;
}

function cacheBust(url, version) {
  const sep = url.includes("?") ? "&" : "?";
  return `${url}${sep}v=${version}`;
}

// ── Hash routing (browser back/forward) ──

let routeSyncing = false;

function parseRoute() {
  const parts = (location.hash || "#/").replace(/^#/, "").split("/").filter(Boolean);
  if (!parts.length) return { screen: "home" };
  if (parts[0] === "subject" && parts[1]) {
    return { screen: "subject", slug: decodeURIComponent(parts[1]) };
  }
  if (parts[0] !== "exam" || !parts[1]) return { screen: "home" };
  const id = decodeURIComponent(parts[1]);
  if (parts[2] === "review") {
    return { screen: "review", id, missed: parts[3] === "missed" };
  }
  if (parts[2] === "results") return { screen: "results", id };
  if (!parts[2]) return { screen: "exam", id };
  return { screen: "home" };
}

function hashForDest(dest) {
  switch (dest.type) {
    case "home":
      return "#/";
    case "subject":
      return `#/subject/${encodeURIComponent(dest.slug)}`;
    case "exam":
      return `#/exam/${encodeURIComponent(dest.id)}`;
    case "review":
      return dest.missed
        ? `#/exam/${encodeURIComponent(dest.id)}/review/missed`
        : `#/exam/${encodeURIComponent(dest.id)}/review`;
    case "results":
      return `#/exam/${encodeURIComponent(dest.id)}/results`;
    default:
      return "#/";
  }
}

function destFromRoute(route) {
  if (route.screen === "home") return { type: "home" };
  if (route.screen === "subject") return { type: "subject", slug: route.slug };
  if (route.screen === "exam") {
    return { type: "exam", id: route.id, resume: true, confirmNew: false };
  }
  if (route.screen === "review") {
    return { type: "review", id: route.id, missed: route.missed };
  }
  if (route.screen === "results") return { type: "results", id: route.id };
  return { type: "home" };
}

function setRouteHash(hash, replace = false) {
  const path = hash || "#/";
  if (location.hash === path) return;
  routeSyncing = true;
  if (replace) {
    history.replaceState({ route: path }, "", path);
  } else {
    history.pushState({ route: path }, "", path);
  }
  routeSyncing = false;
}

async function navigate(dest, { replace = false, skipHash = false } = {}) {
  if (!skipHash) setRouteHash(hashForDest(dest), replace);

  if (dest.type === "home") {
    stopTimer();
    document.body.classList.remove("in-exam");
    showScreen("screen-home");
    return true;
  }

  if (dest.type === "exam") {
    const ok = await startExam(dest.id, dest.resume ?? false, {
      confirmNew: dest.confirmNew ?? false,
    });
    if (!ok && !skipHash) history.back();
    return ok;
  }

  if (dest.type === "review") {
    let filterIds = null;
    if (dest.missed) {
      const last = getLastResult(dest.id);
      if (!last?.sessionMissed?.length) {
        if (!skipHash) navigate({ type: "results", id: dest.id }, { replace: true });
        return false;
      }
      filterIds = last.sessionMissed.map((m) => m.id);
    }
    return startReviewMode(dest.id, filterIds);
  }

  if (dest.type === "results") {
    return openExamResults(dest.id);
  }

  if (dest.type === "subject") {
    return openSubject(dest.slug);
  }

  return false;
}

async function handleRouteChange() {
  if (routeSyncing || !catalog) return;
  await navigate(destFromRoute(parseRoute()), { skipHash: true });
}

function bindRouting() {
  window.addEventListener("popstate", () => {
    if (routeSyncing) return;
    handleRouteChange();
  });
}

async function init() {
  purgeStaleExplainCache();
  const catRes = await fetch(cacheBust("data/catalog.json", CATALOG_VERSION), { cache: "no-store" });
  catalog = await catRes.json();
  bindExamListEvents();
  bindSummaryEvents();
  bindSubjectNav();
  bindRouting();
  await ensureSubjectData();
  renderSubjectNav();
  if (!location.hash) setRouteHash("#/", true);
  await handleRouteChange();
  document.getElementById("exam-search")?.addEventListener("input", filterExamGrid);
  await checkExplainStatus();
}

function examSearchText(exam) {
  return [exam.title, exam.year, exam.source, exam.id].filter(Boolean).join(" ").toLowerCase();
}

function examTagLabel(exam) {
  if (exam.year) return exam.year;
  if (exam.source) return exam.source;
  return "Practice";
}

function examStatusLine(exam) {
  const state = getExamState(exam.id);
  const last = getLastResult(exam.id);
  if (state?.inProgress && !isStaleExamState(exam.id, state)) {
    const answered = Object.keys(state.answers || {}).length;
    const left = state.timeLeftMs ?? getExamTimeMs(exam);
    return `In progress · ${answered}/${exam.questionCount ?? "?"} answered · ${formatTime(left)} left`;
  }
  if (state?.inProgress && isStaleExamState(exam.id, state)) {
    return "Exam updated — start a new attempt";
  }
  if (last) {
    return `Last score: ${last.pct}% (${last.correct}/${last.total})`;
  }
  return "Not started yet";
}

function topicToSlug(topic) {
  return topic
    .toLowerCase()
    .replace(/\s*\/\s*/g, "-")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function setSubjectLoading(loading) {
  const html = loading
    ? '<p class="subject-loading">Loading subjects…</p>'
    : "";
  if (loading) {
    for (const id of ["subject-nav", "subject-nav-page"]) {
      const el = document.getElementById(id);
      if (el) el.innerHTML = html;
    }
  }
}

async function ensureSubjectData() {
  if (subjectData) return subjectData;
  if (!catalog?.exams?.length) return null;

  setSubjectLoading(true);
  try {
    const subRes = await fetch(cacheBust("data/subjects.json", SUBJECTS_VERSION), { cache: "no-store" });
    if (!subRes.ok) throw new Error("subjects.json not found — run scripts/build_subjects.py");
    const bundle = await subRes.json();

    const deepByExam = new Map();
    await Promise.all(
      catalog.exams.map(async (exam) => {
        const res = await fetch(cacheBust(exam.deepPath, examDataRevision(exam)), { cache: "no-store" });
        if (res.ok) deepByExam.set(exam.id, await res.json());
      })
    );

    const topics = (bundle.subjects || []).map((s) => ({
      name: s.name,
      slug: s.slug,
      count: s.count,
      guide: s.guide || "",
      questions: s.questions || [],
    }));
    const slugToTopic = new Map(topics.map((t) => [t.slug, t.name]));
    const questionsByTopic = new Map(topics.map((t) => [t.name, t.questions]));

    subjectData = {
      totalQuestions: bundle.totalQuestions ?? 0,
      examCount: bundle.examCount ?? catalog.exams.length,
      focusGuide: bundle.focusGuide || {},
      deepByExam,
      topics,
      slugToTopic,
      questionsByTopic,
    };

    const label = `${subjectData.totalQuestions} questions · ${subjectData.examCount} exams`;
    document.getElementById("subject-source-label")?.replaceChildren(document.createTextNode(label));
    document.getElementById("subject-source-label-page")?.replaceChildren(document.createTextNode(label));
    const lead = document.getElementById("home-lead");
    if (lead) {
      lead.textContent = `Study all ${subjectData.totalQuestions} questions by subject in the sidebar, or take a timed exam below.`;
    }
    return subjectData;
  } finally {
    setSubjectLoading(false);
  }
}

function renderSubjectNav(activeSlug = currentSubjectSlug) {
  if (!subjectData) return;
  for (const id of ["subject-nav", "subject-nav-page"]) {
    const el = document.getElementById(id);
    if (!el) continue;
    el.innerHTML = subjectData.topics
      .map((t) => {
        const active = t.slug === activeSlug;
        return `<button type="button" class="subject-nav-btn${active ? " is-active" : ""}" data-slug="${escAttr(t.slug)}">
          <span class="subject-nav-label">${esc(t.name)}</span>
          <span class="subject-nav-count">${t.count}</span>
        </button>`;
      })
      .join("");
  }
}

function bindSubjectNav() {
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".subject-nav-btn");
    if (!btn) return;
    e.preventDefault();
    navigate({ type: "subject", slug: btn.dataset.slug });
  });
}

function deepEntryForQuestion(q) {
  const num = String(q.examNumber ?? q.id ?? "");
  const deep = subjectData?.deepByExam?.get(q.examId);
  const entry = deep?.[num];
  if (entry) return entry;
  return {
    overview: q.concept || "No detailed explanation available for this question.",
    options: Object.fromEntries((q.options || []).map((o) => [o.key, o.text])),
    studyTip:
      subjectData?.focusGuide?.[q.topic] || subjectData?.focusGuide?.General || "",
  };
}

function subjectQuestionKey(q) {
  return `${q.examId}-${q.examNumber ?? q.id}`;
}

function buildExplanationHtml(q, correct, exp, picked = null) {
  const optionsHtml = (q.options || [])
    .map((opt) => {
      const text = (exp.options && exp.options[opt.key]) || opt.text;
      let itemCls = "exp-item";
      let label = `Option ${opt.key}`;
      let labelCls = "neutral";
      if (opt.key === correct) {
        itemCls += " is-answer";
        label = `Option ${opt.key} — Correct`;
        labelCls = "ok";
      } else if (picked && opt.key === picked) {
        itemCls += " is-wrong-pick";
        label = `Option ${opt.key} — Your choice`;
        labelCls = "bad";
      }
      return `<div class="${itemCls}"><div class="exp-label ${labelCls}">${label}</div><div class="exp-text">${formatText(text)}</div></div>`;
    })
    .join("");

  const tip = exp.studyTip || "";
  const tipHtml = tip ? `<p class="study-tip"><strong>Study tip:</strong> ${formatText(tip)}</p>` : "";

  return `<div class="concept">${formatText(exp.overview || q.concept || "")}</div>
    <div class="explanations">${optionsHtml}</div>
    ${tipHtml}`;
}

function renderSubjectChoicesHtml(q, cardId) {
  const picked = subjectAnswers[cardId];
  const correct = q.answer;
  return (q.options || [])
    .map((opt) => {
      if (!picked) {
        return `<button type="button" class="choice" data-card="${escAttr(cardId)}" data-key="${opt.key}">
          <span class="key">${opt.key}</span><span>${esc(opt.text)}</span>
        </button>`;
      }
      let cls = "choice";
      if (opt.key === correct) cls += " correct";
      else if (opt.key === picked) cls += " wrong selected";
      else cls += " dim";
      return `<div class="${cls}"><span class="key">${opt.key}</span><span>${esc(opt.text)}</span></div>`;
    })
    .join("");
}

function renderSubjectQuestionCard(q) {
  const cardId = subjectQuestionKey(q);
  const picked = subjectAnswers[cardId];
  const num = q.examNumber ?? q.id;
  const answered = Boolean(picked);
  const correct = q.answer;
  const isCorrect = picked === correct;
  const exp = answered ? deepEntryForQuestion(q) : null;

  let feedbackInner = "";
  if (answered && exp) {
    feedbackInner = `
      <div class="result-banner ${isCorrect ? "ok" : "no"}">${isCorrect ? "Correct" : `Incorrect — answer is ${correct}`}</div>
      ${buildExplanationHtml(q, correct, exp, picked)}`;
  }

  return `<article class="subject-q-card" id="subject-q-${escAttr(cardId)}">
    <div class="subject-q-head">
      <span class="badge">Q${num}</span>
      <span class="subject-q-meta">${esc(q.examTitle || q.examId)}</span>
    </div>
    <p class="q-text exam-q-text">${esc(q.text)}</p>
    <div class="choices" data-choices="${escAttr(cardId)}">${renderSubjectChoicesHtml(q, cardId)}</div>
    <div class="feedback subject-q-feedback${answered ? "" : " hidden"}" data-feedback="${escAttr(cardId)}">
      ${feedbackInner}
    </div>
  </article>`;
}

function pickSubjectAnswer(cardId, key) {
  if (subjectAnswers[cardId]) return;
  const q = currentSubjectQuestions.find((item) => subjectQuestionKey(item) === cardId);
  if (!q) return;

  subjectAnswers[cardId] = key;
  const correct = q.answer;
  const isCorrect = key === correct;
  const card = document.getElementById(`subject-q-${cardId}`);
  if (!card) return;

  const choicesEl = card.querySelector(`[data-choices="${cardId}"]`);
  if (choicesEl) choicesEl.innerHTML = renderSubjectChoicesHtml(q, cardId);

  const exp = deepEntryForQuestion(q);
  const feedbackEl = card.querySelector(`[data-feedback="${cardId}"]`);
  if (feedbackEl) {
    feedbackEl.classList.remove("hidden");
    feedbackEl.innerHTML = `
      <div class="result-banner ${isCorrect ? "ok" : "no"}">${isCorrect ? "Correct" : `Incorrect — answer is ${correct}`}</div>
      ${buildExplanationHtml(q, correct, exp, key)}`;
  }
}

function bindSubjectQuestionEvents() {
  const list = document.getElementById("subject-questions-list");
  if (!list || list.dataset.bound === "1") return;
  list.dataset.bound = "1";
  list.addEventListener("click", (e) => {
    const btn = e.target.closest(".choice[data-card][data-key]");
    if (!btn || btn.disabled) return;
    pickSubjectAnswer(btn.dataset.card, btn.dataset.key);
  });
}

function renderSubjectScrollPage(topic) {
  const qs = subjectData.questionsByTopic.get(topic) || [];
  currentSubjectQuestions = qs;
  subjectAnswers = {};

  const topicMeta = subjectData.topics.find((t) => t.name === topic);
  const guideText =
    topicMeta?.guide ||
    subjectData.focusGuide[topic] ||
    subjectData.focusGuide.General ||
    "";

  document.getElementById("subject-page-head").innerHTML = `
    <h1 class="studio-page-title subject-page-title">${esc(topic)}</h1>
    <p class="studio-page-lead">${qs.length} question${qs.length === 1 ? "" : "s"} · ${subjectData.examCount} exams · pick an answer to see the explanation</p>
    ${guideText ? `<p class="subject-guide">${esc(guideText)}</p>` : ""}`;

  document.getElementById("subject-questions-list").innerHTML = qs.map(renderSubjectQuestionCard).join("");
  bindSubjectQuestionEvents();
  const scrollEl = document.getElementById("subject-scroll");
  if (scrollEl) scrollEl.scrollTop = 0;
}

async function openSubject(slug) {
  if (!(await ensureSubjectData())) return false;
  const topic = subjectData.slugToTopic.get(slug);
  if (!topic) {
    navigate({ type: "home" }, { replace: true });
    return false;
  }

  currentSubjectSlug = slug;
  stopTimer();
  document.body.classList.remove("in-exam");
  showScreen("screen-subject");
  renderSubjectNav(slug);
  renderSubjectScrollPage(topic);
  return true;
}

function renderExamList() {
  const el = document.getElementById("exam-list");
  const countEl = document.getElementById("exam-count-label");
  if (!el || !catalog?.exams?.length) return;

  const exams = catalog.exams;
  const totalQuestions = exams.reduce((sum, e) => sum + (e.questionCount ?? 0), 0);
  if (countEl) {
    countEl.textContent = `${exams.length} exam${exams.length === 1 ? "" : "s"} · ${totalQuestions} playable questions`;
  }

  el.innerHTML = exams
    .map((exam) => {
      const state = getExamState(exam.id);
      const last = getLastResult(exam.id);
      const count = exam.questionCount ?? "?";
      const hours = exam.timeLimitHours ?? EXAM_HOURS_DEFAULT;
      const inProgress = state?.inProgress && !isStaleExamState(exam.id, state);
      const status = examStatusLine(exam);

      const actionPills = [
        inProgress
          ? `<button type="button" class="tag-pill tag-pill-action tag-pill-primary exam-resume" data-id="${escAttr(exam.id)}">Resume</button>`
          : `<button type="button" class="tag-pill tag-pill-action tag-pill-primary exam-start" data-id="${escAttr(exam.id)}">Exam Mode</button>`,
        `<button type="button" class="tag-pill tag-pill-action exam-review" data-id="${escAttr(exam.id)}">Feedback Mode</button>`,
        last
          ? `<button type="button" class="tag-pill tag-pill-action exam-results" data-id="${escAttr(exam.id)}">Results</button>`
          : "",
      ]
        .filter(Boolean)
        .join("");

      return `
      <article class="exam-grid-card" data-id="${escAttr(exam.id)}" data-search="${escAttr(examSearchText(exam))}">
        <div class="exam-grid-card-head">
          <h2 class="exam-grid-card-title">${esc(exam.title)}</h2>
          <span class="exam-grid-card-badge">${hours}h timed</span>
        </div>
        <p class="exam-grid-card-count">${count} playable questions</p>
        <p class="exam-grid-card-status${inProgress ? " is-active" : ""}${last && !inProgress ? " has-score" : ""}">${esc(status)}</p>
        <div class="exam-grid-card-tags">${actionPills}</div>
      </article>`;
    })
    .join("");

  filterExamGrid();
}

function filterExamGrid() {
  const query = (document.getElementById("exam-search")?.value || "").trim().toLowerCase();
  document.querySelectorAll(".exam-grid-card").forEach((card) => {
    const haystack = card.dataset.search || "";
    card.classList.toggle("is-hidden", Boolean(query) && !haystack.includes(query));
  });
  const visible = document.querySelectorAll(".exam-grid-card:not(.is-hidden)").length;
  const total = catalog?.exams?.length ?? 0;
  const countEl = document.getElementById("exam-count-label");
  if (countEl && query) {
    countEl.textContent = `${visible} of ${total} exams shown`;
  } else if (countEl && catalog?.exams) {
    const totalQuestions = catalog.exams.reduce((sum, e) => sum + (e.questionCount ?? 0), 0);
    countEl.textContent = `${total} exam${total === 1 ? "" : "s"} · ${totalQuestions} playable questions`;
  }
}

function bindExamListEvents() {
  const el = document.getElementById("exam-list");
  if (!el || el.dataset.bound === "1") return;
  el.dataset.bound = "1";
  el.addEventListener("click", (e) => {
    const start = e.target.closest(".exam-start");
    if (start) {
      e.preventDefault();
      navigate({ type: "exam", id: start.dataset.id, resume: false, confirmNew: true });
      return;
    }
    const resume = e.target.closest(".exam-resume");
    if (resume) {
      e.preventDefault();
      navigate({ type: "exam", id: resume.dataset.id, resume: true, confirmNew: false });
      return;
    }
    const review = e.target.closest(".exam-review");
    if (review) {
      e.preventDefault();
      navigate({ type: "review", id: review.dataset.id });
      return;
    }
    const results = e.target.closest(".exam-results");
    if (results) {
      e.preventDefault();
      navigate({ type: "results", id: results.dataset.id });
    }
  });
}

async function openExamResults(examId) {
  const last = getLastResult(examId);
  if (!last) return false;
  currentExam = getSessionMeta(examId);
  if (!(await loadSessionData(examId))) return false;
  lastResult = last;
  if (!lastResult.focusGuide || !Object.keys(lastResult.focusGuide).length) {
    lastResult.focusGuide = data?.focusGuide || {};
  }
  stopTimer();
  document.body.classList.remove("in-exam");
  renderSummary(lastResult);
  showScreen("screen-summary");
  window.scrollTo(0, 0);
  return true;
}

async function loadSessionData(sessionId) {
  const meta = getSessionMeta(sessionId);
  if (!meta) return false;
  currentExam = meta;
  const rev = examDataRevision(meta);
  const res = await fetch(cacheBust(meta.questionsPath, rev), { cache: "no-store" });
  data = await res.json();
  questions = data.questions || [];
  return true;
}

async function startExam(examId, resume, { confirmNew = true } = {}) {
  if (!(await loadSessionData(examId))) return false;

  if (resume) {
    const state = getExamState(examId);
    if (isStaleExamState(examId, state)) {
      localStorage.removeItem(examStateKey(examId));
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
      examSkipped = new Set((state.skipped || []).map(String));
      timeLeftMs = state.timeLeftMs ?? examMs;
    } else {
      resume = false;
    }
  }

  if (!resume) {
    const inProgress = getExamState(examId)?.inProgress;
    if (confirmNew && inProgress) {
      if (!confirm("Start a new 3-hour exam? Any in-progress attempt will be replaced.")) return false;
    } else if (confirmNew && !inProgress) {
      if (!confirm("Start a new 3-hour exam?")) return false;
    }
    examIndex = 0;
    examAnswers = {};
    examFlagged = new Set();
    examSkipped = new Set();
    timeLeftMs = getExamTimeMs(currentExam);
  }

  document.body.classList.add("in-exam");
  const titleBar = document.getElementById("exam-title-bar");
  const subBar = document.getElementById("exam-subtitle-bar");
  const displayTitle = data.title || currentExam.title;
  if (titleBar) titleBar.textContent = displayTitle;
  if (subBar) {
    subBar.textContent = `Exam Mode · ${questions.length} questions · ${currentExam.timeLimitHours ?? EXAM_HOURS_DEFAULT}h`;
  }

  showScreen("screen-exam");
  startTimer();
  updateExamNav();
  renderExamQuestion();
  return true;
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
  const navKey = `${currentExam?.id || "default"}-${questionList.length}`;
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
    startedAt: getExamState(currentExam.id)?.startedAt || Date.now(),
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
      scrollQuestionViewToTop();
    });
    container.appendChild(btn);
  });

  document.getElementById("btn-prev").disabled = examIndex === 0;
  document.getElementById("btn-next-exam").textContent =
    examIndex === questions.length - 1 ? "Finish" : "Next";
  document.getElementById("btn-flag").classList.toggle("flagged", examFlagged.has(questionKey(q)));
  updateExamNav();
  persistExamState();
  scrollQuestionViewToTop(true);
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

  const sessionTitle = data.title || currentExam.title;

  return {
    date: new Date().toISOString(),
    examId: currentExam.id,
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

  let saveOk = true;
  try {
    saveLastResult(currentExam.id, lastResult);
    saveExamState({ inProgress: false, examId: currentExam.id });
  } catch (e) {
    saveOk = false;
    console.warn("Could not save exam result to browser storage:", e);
  }

  navigate({ type: "results", id: currentExam.id }, { replace: true });
  window.scrollTo(0, 0);

  const warnEl = document.getElementById("summary-save-warn");
  if (warnEl) {
    warnEl.classList.toggle("hidden", saveOk);
    if (!saveOk) {
      warnEl.textContent =
        "Results shown below but could not be saved (browser storage full). Screenshot this page or review now.";
    }
  }
}

async function startReviewMode(sessionId, filterIds) {
  if (!(await loadSessionData(sessionId))) return false;
  reviewFilter = filterIds;
  if (filterIds) {
    reviewQuestions = questions.filter((q) => filterIds.includes(q.id));
  } else {
    reviewQuestions = [...questions];
  }
  if (!reviewQuestions.length) {
    alert("No questions to review.");
    return false;
  }
  reviewIndex = 0;
  reviewAnswers = {};
  stopTimer();
  document.body.classList.add("in-exam");
  const reviewTitle = document.getElementById("review-exam-title");
  if (reviewTitle) {
    reviewTitle.textContent = data.title || currentExam.title;
  }
  showScreen("screen-review");
  updateReviewNav();
  renderReviewQuestion();
  return true;
}

function renderReviewQuestion() {
  const q = reviewQuestions[reviewIndex];
  const picked = reviewAnswers[questionKey(q)];
  reviewAnswered = Boolean(picked);
  const pct = ((reviewIndex + 1) / reviewQuestions.length) * 100;

  document.getElementById("review-bar").style.width = `${pct}%`;
  document.getElementById("review-counter").textContent = `Q ${reviewIndex + 1} / ${reviewQuestions.length}`;
  const topicLabel = `${currentExam.title} · ${q.topic}`;
  document.getElementById("review-topic-badge").textContent = topicLabel;
  document.getElementById("review-q-text").textContent = q.text;

  document.getElementById("feedback").classList.add("hidden");
  document.getElementById("explain-loading").classList.add("hidden");
  document.getElementById("explain-body").classList.add("hidden");

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
      else if (opt.key === picked) btn.classList.add("wrong", "selected");
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
  setReviewNextButton(reviewAnswered);
  scrollQuestionViewToTop(true);
}

function setReviewNextButton(enabled) {
  const nextBtn = document.getElementById("btn-next-review-footer");
  if (!nextBtn) return;
  nextBtn.disabled = !enabled;
  nextBtn.textContent = reviewIndex === reviewQuestions.length - 1 ? "Done" : "Next →";
}

function showReviewFeedback(q, picked) {
  const correct = q.answer;
  const isCorrect = picked === correct;

  document.getElementById("result-banner").className = "result-banner " + (isCorrect ? "ok" : "no");
  document.getElementById("result-banner").textContent = isCorrect
    ? "Correct"
    : `Incorrect — answer is ${correct}`;

  document.getElementById("feedback").classList.remove("hidden");
  setReviewNextButton(true);
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
    else if (k === key) btn.classList.add("wrong", "selected");
    else btn.classList.add("dim");
  });

  document.getElementById("result-banner").className = "result-banner " + (isCorrect ? "ok" : "no");
  document.getElementById("result-banner").textContent = isCorrect
    ? "Correct — loading explanation…"
    : `Incorrect — correct answer is ${correct}`;

  document.getElementById("feedback").classList.remove("hidden");
  document.getElementById("explain-loading").classList.remove("hidden");
  document.getElementById("explain-body").classList.add("hidden");
  setReviewNextButton(true);
  scrollToReviewFeedback();

  updateReviewNav();

  const exp = await fetchExplanation(q, key);
  renderExplanation(q, key, correct, isCorrect, exp);
}

function explainExamId(q) {
  return q.sourceExamId || currentExam.id;
}

async function fetchExplanation(q, userPick) {
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
      }),
    });
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || res.statusText);
    return await res.json();
  } catch (e) {
    return {
      overview: q.concept || "Could not load explanation.",
      options: Object.fromEntries(q.options.map((o) => [o.key, o.text])),
      studyTip: "Run server/server.py to load offline explanations.",
      source: "error-fallback",
    };
  }
}

function renderExplanation(q, picked, correct, isCorrect, exp) {
  document.getElementById("explain-loading").classList.add("hidden");
  document.getElementById("explain-body").classList.remove("hidden");
  setReviewNextButton(true);

  document.getElementById("result-banner").className = "result-banner " + (isCorrect ? "ok" : "no");
  document.getElementById("result-banner").textContent = isCorrect
    ? "Correct"
    : `Incorrect — answer is ${correct}`;

  document.getElementById("concept").innerHTML = formatText(exp.overview || "");

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
      return `<div class="${itemCls}"><div class="exp-label ${cls}">${label}</div><div class="exp-text">${formatText(text)}</div></div>`;
    })
    .join("");

  const tip = exp.studyTip || "";
  document.getElementById("study-tip").innerHTML = tip ? `<strong>Study tip:</strong> ${formatText(tip)}` : "";
  requestAnimationFrame(() => {
    requestAnimationFrame(() => scrollToReviewFeedback());
  });
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
    navigate({ type: "home" });
  }
}

function prevReview() {
  if (reviewIndex > 0) {
    reviewIndex--;
    renderReviewQuestion();
  }
}

function findQuestionIndexById(id, examNumber) {
  const key = String(id);
  let idx = questions.findIndex((q) => questionKey(q) === key);
  if (idx >= 0) return idx;
  if (examNumber != null) {
    idx = questions.findIndex((q) => String(q.examNumber) === String(examNumber));
  }
  return idx;
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
      const num = q.examNumber ?? i + 1;
      if (missed) {
        return `<button type="button" class="q-pill q-pill-missed" data-status="${status}" data-qidx="${i}" data-missed="1" title="View Q${num} explanation">${
          num
        }</button>`;
      }
      return `<span class="q-pill" data-status="${status}" title="Q${num} — correct">${num}</span>`;
    })
    .join("");
}

function renderSummaryMissedChoices(q, picked) {
  const container = document.getElementById("summary-missed-choices");
  if (!container) return;
  const correct = q.answer;
  container.innerHTML = "";
  q.options.forEach((opt) => {
    const btn = document.createElement("div");
    btn.className = "choice";
    if (opt.key === correct) btn.classList.add("correct");
    else if (picked && opt.key === picked) btn.classList.add("wrong", "selected");
    else if (!picked) btn.classList.add("dim");
    else btn.classList.add("dim");
    btn.innerHTML = `<span class="key">${opt.key}</span><span>${esc(opt.text)}</span>`;
    container.appendChild(btn);
  });
}

function renderSummaryMissedExplanation(q, picked, exp) {
  const correct = q.answer;
  const isCorrect = picked && isAnswerCorrect(picked, correct);
  const banner = document.getElementById("summary-missed-banner");
  if (banner) {
    banner.className = "result-banner " + (isCorrect ? "ok" : "no");
    banner.textContent = isCorrect
      ? "Correct"
      : picked
        ? `Incorrect — you picked ${picked}, answer is ${correct}`
        : `Skipped — answer is ${correct}`;
  }

  document.getElementById("summary-missed-loading")?.classList.add("hidden");
  document.getElementById("summary-missed-explain-body")?.classList.remove("hidden");

  const concept = document.getElementById("summary-missed-concept");
  if (concept) concept.innerHTML = formatText(exp.overview || "");

  const explanations = document.getElementById("summary-missed-explanations");
  if (explanations) {
    explanations.innerHTML = q.options
      .map((opt) => {
        const text = (exp.options && exp.options[opt.key]) || opt.text;
        let cls = "neutral";
        let label = `Option ${opt.key}`;
        if (opt.key === correct) {
          cls = "ok";
          label = `Option ${opt.key} — Correct`;
        } else if (picked && opt.key === picked) {
          cls = "bad";
          label = `Option ${opt.key} — Your choice`;
        }
        const itemCls =
          opt.key === correct ? "exp-item is-answer" : picked && opt.key === picked ? "exp-item is-wrong-pick" : "exp-item";
        return `<div class="${itemCls}"><div class="exp-label ${cls}">${label}</div><div class="exp-text">${formatText(text)}</div></div>`;
      })
      .join("");
  }

  const tip = exp.studyTip || "";
  const tipEl = document.getElementById("summary-missed-study-tip");
  if (tipEl) tipEl.innerHTML = tip ? `<strong>Study tip:</strong> ${formatText(tip)}` : "";
}

async function openSummaryMissedQuestion(qIndex) {
  const q = questions[qIndex];
  if (!q || !lastResult) return;

  const missed = (lastResult.sessionMissed || []).find((m) => String(m.id) === questionKey(q));
  if (!missed) return;

  const picked = missed.picked || "";
  const panel = document.getElementById("summary-missed-detail");
  const label = document.getElementById("summary-missed-label");
  const qText = document.getElementById("summary-missed-q-text");

  if (label) label.textContent = `Question ${q.examNumber ?? qIndex + 1} · ${q.topic}`;
  if (qText) qText.textContent = q.text;

  renderSummaryMissedChoices(q, picked);

  document.getElementById("summary-missed-explain-body")?.classList.add("hidden");
  document.getElementById("summary-missed-loading")?.classList.remove("hidden");
  if (panel) {
    panel.classList.remove("hidden");
    panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  document.querySelectorAll("#summary-question-nav .q-pill-missed").forEach((pill) => {
    pill.classList.toggle("is-active", parseInt(pill.dataset.qidx, 10) === qIndex);
  });

  const exp = await fetchExplanation(q, picked);
  if (questions[qIndex] !== q) return;
  renderSummaryMissedExplanation(q, picked, exp);
}

function closeSummaryMissedDetail() {
  document.getElementById("summary-missed-detail")?.classList.add("hidden");
  document.querySelectorAll("#summary-question-nav .q-pill-missed").forEach((pill) => {
    pill.classList.remove("is-active");
  });
}

function bindSummaryEvents() {
  const strip = document.getElementById("summary-question-nav");
  if (strip && strip.dataset.bound !== "1") {
    strip.dataset.bound = "1";
    strip.addEventListener("click", (e) => {
      const pill = e.target.closest(".q-pill-missed[data-qidx]");
      if (!pill) return;
      openSummaryMissedQuestion(parseInt(pill.dataset.qidx, 10));
    });
  }

  const list = document.getElementById("review-list");
  if (list && list.dataset.bound !== "1") {
    list.dataset.bound = "1";
    list.addEventListener("click", (e) => {
      const item = e.target.closest("[data-missed-qidx]");
      if (!item) return;
      openSummaryMissedQuestion(parseInt(item.dataset.missedQidx, 10));
    });
  }

  document.getElementById("btn-close-summary-detail")?.addEventListener("click", closeSummaryMissedDetail);
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

  closeSummaryMissedDetail();

  const missed = result.sessionMissed || [];
  document.getElementById("review-list").innerHTML = !missed.length
    ? '<p class="empty">Perfect score — no missed questions!</p>'
    : missed
        .map((m, i) => {
          const qIdx = findQuestionIndexById(m.id, m.examNumber);
          const label =
            m.reason === "unanswered" || m.picked == null
              ? "Skipped"
              : `You: ${m.picked} → Correct: ${m.answer}`;
          const qNum = m.examNumber ?? i + 1;
          return `<button type="button" class="review-item review-item-clickable" data-missed-qidx="${qIdx}" title="View explanation">
            <strong>Q${qNum}.</strong> ${esc(String(m.text || "").slice(0, 120))}${String(m.text || "").length > 120 ? "…" : ""}
            <br><small>${label} · ${esc(m.topic)}</small>
          </button>`;
        })
        .join("");

  document.getElementById("btn-review-missed-only").style.display =
    missed.length > 0 ? "inline-flex" : "none";
}

function scrollQuestionViewToTop(smooth = false) {
  const behavior = smooth ? "smooth" : "auto";
  const active = document.querySelector(".screen.active.exam-screen") || document.querySelector(".screen.active");
  const main = active?.querySelector(".national-main");

  window.scrollTo({ top: 0, left: 0, behavior });
  document.documentElement.scrollTo({ top: 0, left: 0, behavior });
  document.body.scrollTo({ top: 0, left: 0, behavior });

  if (main) {
    main.scrollTop = 0;
    main.scrollTo({ top: 0, left: 0, behavior });
  }
}

function scrollToReviewFeedback(smooth = false) {
  scrollQuestionViewToTop(smooth);
}

function showScreen(id) {
  document.querySelectorAll(".screen").forEach((s) => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  document.body.classList.toggle("in-exam", id === "screen-exam" || id === "screen-review");
  document.body.classList.toggle("on-home", id === "screen-home");
  document.body.classList.toggle("on-subject", id === "screen-subject");
  document.body.classList.toggle("on-summary", id === "screen-summary");
  if (id === "screen-home") {
    currentSubjectSlug = null;
    renderSubjectNav();
    renderExamList();
  }
}

async function checkExplainStatus() {
  const el = document.getElementById("explain-status");
  try {
    const h = await (await fetch("/api/health")).json();
    const total = Object.values(h.deepCounts || {}).reduce((a, b) => a + b, 0);
    el.textContent = `${total} offline explanations · study by subject (sidebar) or timed exams`;
  } catch {
    el.textContent = "Run server/server.py to enable explanations";
  }
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
document.getElementById("btn-next-review-footer").addEventListener("click", () => {
  if (reviewAnswered) nextReview();
});

document.getElementById("btn-review-answers").addEventListener("click", () => {
  if (currentExam) navigate({ type: "review", id: currentExam.id });
});
document.getElementById("btn-review-missed-only").addEventListener("click", () => {
  if (lastResult?.sessionMissed?.length && currentExam) {
    navigate({ type: "review", id: currentExam.id, missed: true });
  }
});
document.getElementById("btn-back-home").addEventListener("click", () => navigate({ type: "home" }));
document.getElementById("btn-subject-home")?.addEventListener("click", () => navigate({ type: "home" }));

document.getElementById("btn-toggle-exam-nav")?.addEventListener("click", () => toggleSidebar("exam"));
document.getElementById("btn-toggle-review-nav")?.addEventListener("click", () => toggleSidebar("review"));
document.getElementById("exam-sidebar-backdrop")?.addEventListener("click", () => closeSidebar("exam"));
document.getElementById("review-sidebar-backdrop")?.addEventListener("click", () => closeSidebar("review"));

init();
