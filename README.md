# Ethiopian Software Engineering Exit Exam — Practice App

A web-based MCQ simulator for Ethiopian university **Software Engineering exit exam** preparation. Practice under real exam conditions with a **3-hour timer**, then review every question with **deep explanations for all four choices** (why the correct answer fits and why each distractor fails).

Built for students preparing for the national MoE exit exam and related model papers (2015–2017, AAU, BDU, ASTU, MoEE).

---

## Features

- **Exam mode** — timed 3-hour sessions, answers hidden until submit (like the real test)
- **Review mode** — step through questions with instant feedback and detailed breakdowns
- **Deep explanations** — overview, per-option analysis (A–D), and study tips for every question
- **Score summary** — percentage score, **score by topic**, and **focus areas** for weak concepts
- **Resume exam** — continue an in-progress attempt (saved in your browser)
- **Mobile-friendly** — responsive layout for phone and desktop

---

## Exams included

| Exam | Questions | Deep explanations |
|------|-----------|-------------------|
| Exit Exam 2015 | 93 | Yes |
| 2016 Software Engineering Exit Exam | 100 | Yes |
| 2017 Software Engineering Exit Exam | 96 | Yes |
| AAU Model Exit Exam | 100 | Yes |
| BDU Model Exit Exam | 99 | Yes |
| ASTU Software Engineering MCQs | 60 | Yes |
| MoEE Model Exam 1 | 100 | Yes |
| 2025 MoEE Exit Exam | 100 | Yes |

Topics covered across exams include: programming fundamentals, data structures, OOP/Java, C++, web development, Android, databases, operating systems, software engineering, software architecture, project management, software testing, networking, security, AI/ML, and general SE concepts.

> **Note:** The 2017 exam has 96 of 100 questions. Four items (Q11, Q22, Q23, Q81) are missing from the source screenshots and could not be recovered from OCR.

---

## Quick start (local)

**Requirements:** Python 3.10+ (stdlib only — no pip packages required to run the server)

```bash
cd practice-app
python server/server.py
```

Open **http://localhost:8081** in your browser.

Default port is `8081`. Override with:

**Windows (PowerShell):**
```powershell
$env:PORT=3000
python server/server.py
```

**Linux / macOS:**
```bash
PORT=3000 python server/server.py
```

---

## How to use

1. **Home** — pick an exam from the list
2. **Start Exam (3h)** — timed attempt; flag questions and navigate freely before submitting
3. **Review Mode** — learn at your own pace; explanations load after you pick an answer
4. **View Results** — see your last score, topic breakdown, and questions you missed

Progress and results are stored in **localStorage** in your browser (no account required). Explanations come from **offline deep explanation** files bundled with each exam.

After updating exam data locally, do a **hard refresh** (Ctrl+Shift+R) so the browser loads new JSON.

---

## Deploy to Render (free tier)

This repo includes a [Render Blueprint](https://render.com/docs/blueprint-spec) (`render.yaml`):

1. Push this folder to GitHub
2. In Render: **New → Blueprint** → connect the repo
3. Render runs `python server/server.py` and health-checks `/api/health`

---

## Project structure

```
practice-app/
├── public/                 # Static website (served to browsers)
│   ├── index.html          # App shell
│   ├── css/styles.css      # Layout and theme
│   └── js/app.js           # Exam/review UI, timer, results
├── server/
│   └── server.py           # Static file server + /api/explain + /api/health
├── data/
│   ├── catalog.json        # Exam list (ids, paths, titles)
│   └── exams/
│       ├── 2015/
│       ├── 2016/
│       ├── 2017/           # OCR-built from Moodle screenshots
│       ├── aau/
│       ├── bdu/
│       ├── astu/
│       ├── model1/
│       └── moe2025/
│           ├── questions.json
│           └── deep_explanations.json
├── scripts/                # Build/dev tools (regenerate exam data)
├── render.yaml             # Render deployment config
└── requirements.txt
```

Each exam folder typically contains:

- `questions.json` — MCQs, options, answers, topics, focus guide
- `deep_explanations.json` — offline teaching content keyed by question number

The 2017 exam also includes OCR pipeline artifacts:

- `raw_ocr.json` — raw text from Moodle screenshots
- `number_map.json` — screenshot order → exam question number
- `curated_questions.json` — manual transcriptions for bad OCR
- `matched_answers.json` — cross-exam answer matching log

---

## Adding or updating an exam (developers)

### 1. Add question data

Place files under `data/exams/<exam-id>/` and register the exam in `data/catalog.json`:

```json
{
  "id": "2017",
  "title": "2017 Software Engineering Exit Exam",
  "questionsPath": "data/exams/2017/questions.json",
  "deepPath": "data/exams/2017/deep_explanations.json",
  "timeLimitHours": 3,
  "questionCount": 96,
  "year": "2017"
}
```

### 2. Generate deep explanations

Use the unified deep builder (cross-exam matching + concept engine):

```bash
python scripts/build_all_deep.py
```

Or rebuild a single exam:

```bash
python scripts/build_2016_practice.py
python scripts/build_2016_deep.py
python scripts/build_2017_practice.py
python scripts/build_moe2025_practice.py
```

For 2017 deep explanations only:

```powershell
$env:PYTHONIOENCODING="utf-8"
python -c "
import json, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
from unified_deep_builder import build_deep_entry

data = json.loads(Path('data/exams/2017/questions.json').read_text(encoding='utf-8'))
out = {str(q['examNumber']): build_deep_entry(q, '2017') for q in data['questions']}
Path('data/exams/2017/deep_explanations.json').write_text(
    json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
print(len(out), 'explanations written')
"
```

### 3. Bump browser cache versions

After changing JSON data, bump versions so clients fetch fresh files:

| File | Constant | Purpose |
|------|----------|---------|
| `public/js/app.js` | `CATALOG_VERSION` | `data/catalog.json` and exam question JSON |
| `public/js/app.js` | `EXPLAIN_CACHE_VERSION` | deep explanation JSON + localStorage cache |
| `public/index.html` | `?v=` on `app.js` / `styles.css` | static asset cache bust |

### Key build scripts

| Script | Purpose |
|--------|---------|
| `build_2016_practice.py` | Build 2016 `questions.json` |
| `build_2016_deep.py` | Build 2016 deep explanations |
| `build_2017_practice.py` | Build 2017 `questions.json` from OCR + curated fixes |
| `extract_2017_ocr.py` | Run Windows OCR on Moodle screenshots |
| `exam2017_parser.py` | Parse OCR text into question stems/options |
| `match_2017_answers.py` | Match answers via cross-exam stem similarity |
| `unified_deep_builder.py` | Deep explanations for all exams (concept engine + cross-match) |
| `unified_topic_enricher.py` | Rich per-option rules (Android, OSI, crypto, etc.) |
| `build_moe2025_practice.py` | Build 2025 MoEE exam data |
| `build_all_deep.py` | Regenerate deep explanations across catalog |

Manual curation for 2017 lives in `scripts/exam2017_data.py` (`MANUAL_ANSWERS`, `QUESTION_FIXES`, `FOCUS_GUIDE`).

---

## API endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check (used by Render) |
| `/api/explain` | POST | Return deep explanation for a question (`examId`, `examNumber`) |

The app loads explanations from bundled JSON first; the API is a fallback for the same offline content.

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

> **Tip:** Initialize git inside `practice-app/` if you only want the exam website on GitHub, not a parent folder.

---

## Disclaimer

This project is for **educational practice only**. Exam content is derived from publicly shared past papers and model exams. It is **not affiliated with** or endorsed by the Ethiopian Ministry of Education or any university. Verify answers and wording against your official course materials.

---

## License

MIT — see [LICENSE](LICENSE).
