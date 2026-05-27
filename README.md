# Ethiopian Software Engineering Exit Exam — Practice App

A web-based MCQ simulator for Ethiopian university **Software Engineering exit exam** preparation. Practice under real exam conditions with a **3-hour timer**, then review every question with **deep explanations for all four choices** (why the correct answer fits and why each distractor fails).

Built for students preparing for the national MoE exit exam and related model papers (2015, 2016, AAU, BDU, ASTU, MoEE).

---

## Features

- **Exam mode** — timed 3-hour sessions, answers hidden until submit (like the real test)
- **Review mode** — step through questions with instant feedback and detailed breakdowns
- **Deep explanations** — overview, per-option analysis (A–D), and study tips for every question
- **Score summary** — percentage score, **score by topic**, and **focus areas** for weak concepts
- **Resume exam** — continue an in-progress attempt (saved in your browser)
- **Optional live AI** — connect an OpenAI API key in Settings for extra explanations (offline deep explanations work without a key)
- **Mobile-friendly** — responsive layout for phone and desktop

---

## Exams included

| Exam | Questions | Deep explanations |
|------|-----------|-------------------|
| Exit Exam 2015 | 93 | Yes |
| 2016 Software Engineering Exit Exam | 100 | Yes |
| AAU Model Exit Exam | 100 | Yes |
| BDU Model Exit Exam | 99 | Yes |
| ASTU Software Engineering MCQs | 60 | Yes |
| MoEE Model Exam 1 | 100 | Yes |
| 2025 MoEE Exit Exam | 100 | Yes |

Topics covered across exams include: programming fundamentals, data structures, OOP/Java, web development, Android, databases, operating systems, software engineering, project management, networking, security, AI, and machine learning.

---

## Quick start (local)

**Requirements:** Python 3.10+ (stdlib only — no pip packages required to run the server)

```bash
cd Ethiopian-SE-exit-exam-practice
python server.py
```

Open **http://localhost:8081** in your browser.

Default port is `8081`. Override with:

```bash
set PORT=3000
python server.py
```

---

## How to use

1. **Home** — pick an exam from the list
2. **Start Exam (3h)** — timed attempt; flag questions and navigate freely before submitting
3. **Review Mode** — learn at your own pace; explanations load after you pick an answer
4. **View Results** — see your last score, topic breakdown, and questions you missed
5. **Settings (⚙)** — optional OpenAI API key for live AI explanations

Progress and results are stored in **localStorage** in your browser (no account required).

---

## Optional: live AI explanations

By default, the app uses **offline deep explanations** bundled with each exam.

To enable live AI explanations:

1. Open **Settings** in the app, or
2. Set an environment variable before starting the server:

```bash
set OPENAI_API_KEY=sk-your-key-here
python server.py
```

The server proxies requests to the OpenAI API so your key is not embedded in the frontend code when using the env var.

---

## Deploy to Render (free tier)

This repo includes a [Render Blueprint](https://render.com/docs/blueprint-spec) (`render.yaml`):

1. Push this folder to GitHub
2. In Render: **New → Blueprint** → connect the repo
3. Render runs `python server.py` and health-checks `/api/health`

Set `OPENAI_API_KEY` in Render environment variables if you want server-side AI.

---

## Project structure

```
practice-app/
├── index.html          # App shell
├── app.js              # Exam/review UI, timer, results
├── styles.css          # Layout and theme
├── server.py           # Static file server + /api/explain + /api/health
├── render.yaml         # Render deployment config
├── data/
│   ├── catalog.json    # Exam list (ids, paths, titles)
│   └── exams/
│       ├── 2015/
│       ├── 2016/
│       ├── aau/
│       ├── bdu/
│       ├── astu/
│       ├── model1/
│       └── moe2025/
│           ├── questions.json
│           └── deep_explanations.json
└── build_*.py          # Scripts to regenerate exam data (developers)
```

Each exam folder contains:

- `questions.json` — MCQs, options, answers, topics, focus guide
- `deep_explanations.json` — offline teaching content keyed by question number

---

## Adding or updating an exam (developers)

1. Add question data under `data/exams/<exam-id>/`
2. Register the exam in `data/catalog.json`
3. Bump `CATALOG_VERSION` in `app.js` and the script cache query in `index.html` so browsers fetch fresh JSON

Example build scripts in this repo:

```bash
python build_2016_practice.py   # questions.json from source + OCR fixes
python build_2016_deep.py       # deep_explanations.json
python build_moe2025_practice.py
```

---

## Push to GitHub

From the `practice-app` directory:

```bash
git init
git add .
git commit -m "Add Ethiopian SE exit exam practice app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

> **Tip:** Initialize git inside `practice-app/` if you only want the exam website on GitHub, not the entire parent `research` folder.

---

## Disclaimer

This project is for **educational practice only**. Exam content is derived from publicly shared past papers and model exams. It is **not affiliated with** or endorsed by the Ethiopian Ministry of Education or any university. Verify answers and wording against your official course materials.

---

## License

MIT — see [LICENSE](LICENSE) if present, or add one before publishing.
