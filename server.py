"""Practice app server: static files + live AI explanations."""

import json
import os
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingTCPServer

ROOT = Path(__file__).parent
CATALOG = ROOT / "data" / "catalog.json"
PORT = int(os.environ.get("PORT", "8081"))

_deep_cache: dict[str, tuple[float, dict]] = {}


def load_catalog() -> dict:
    if CATALOG.exists():
        return json.loads(CATALOG.read_text(encoding="utf-8"))
    return {"exams": []}


def _read_deep_file(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    mtime = path.stat().st_mtime
    return mtime, data


def load_deep(exam_id: str = "2015") -> dict:
    for exam in load_catalog().get("exams", []):
        if exam["id"] == exam_id:
            path = ROOT / exam["deepPath"]
            if path.exists():
                mtime, data = _read_deep_file(path)
                cached = _deep_cache.get(exam_id)
                if cached and cached[0] == mtime:
                    return cached[1]
                _deep_cache[exam_id] = (mtime, data)
                return data
    legacy = ROOT / "data" / "deep_explanations.json"
    if legacy.exists():
        mtime, data = _read_deep_file(legacy)
        cached = _deep_cache.get(exam_id)
        if cached and cached[0] == mtime:
            return cached[1]
        _deep_cache[exam_id] = (mtime, data)
        return data
    return {}


def ai_explain(payload: dict) -> dict:
    api_key = payload.get("apiKey") or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("No API key. Add one in Settings or set OPENAI_API_KEY.")

    base_url = payload.get("baseUrl", "https://api.openai.com/v1").rstrip("/")
    model = payload.get("model", "gpt-4o-mini")

    q = payload["question"]
    opts = payload["options"]
    answer = payload["answer"]
    picked = payload.get("userPick", "")
    topic = payload.get("topic", "General")
    exam_title = payload.get("examTitle", "Software Engineering Exit Exam")

    opt_lines = "\n".join(f"{o['key']}. {o['text']}" for o in opts)

    system = (
        "You are an expert Software Engineering tutor helping Ethiopian university students "
        "prepare for exit exams. Write like a patient teacher: clear, detailed, accurate. "
        "Use examples, definitions, and exam tips. Never be vague."
    )
    user = f"""Exam: {exam_title}
Topic: {topic}
Question: {q}

Options:
{opt_lines}

Correct answer: {answer}
Student picked: {picked or "not answered"}

Return JSON only:
{{
  "overview": "4-6 sentences: define the core concept, explain the rule/principle, and why {answer} is correct",
  "options": {{
    "A": "5-8 sentences for option A — state if correct/wrong, explain the underlying idea, give a concrete example, note common mistakes",
    "B": "...",
    "C": "...",
    "D": "..."
  }},
  "studyTip": "2-3 sentences with specific topics/keywords to review for the exam"
}}"""

    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.35,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def offline_explain(payload: dict, deep: dict) -> dict:
    exam_num = str(payload.get("examNumber", ""))
    if exam_num in deep:
        entry = deep[exam_num]
        return {
            "overview": entry.get("overview", ""),
            "options": entry.get("options", {}),
            "studyTip": entry.get("studyTip", ""),
            "source": "offline-deep",
        }

    q = payload["question"]
    answer = payload["answer"]
    opts = {o["key"]: o["text"] for o in payload["options"]}
    topic = payload.get("topic", "General")

    options_out = {}
    for key, text in opts.items():
        if key == answer:
            options_out[key] = (
                f"CORRECT — {text}\n\n"
                f"This matches what the question asks in {topic}. "
                f"It is the standard answer taught in software engineering exit exam preparation."
            )
        else:
            options_out[key] = (
                f"INCORRECT — {text}\n\n"
                f"This is a distractor. It may relate to {topic} but does not satisfy this question. "
                f"Compare with option {answer}."
            )

    return {
        "overview": (
            f"This {topic} question tests a specific definition or rule. "
            f"The correct answer is {answer}: {opts.get(answer, '')}."
        ),
        "options": options_out,
        "studyTip": f"Review {topic} notes and practice similar MCQs.",
        "source": "offline-fallback",
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        if self.path.endswith(".json"):
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/explain":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))

        try:
            use_ai = payload.get("useAi", True)
            exam_id = payload.get("examId", "2015")
            deep = load_deep(exam_id)
            if use_ai and (payload.get("apiKey") or os.environ.get("OPENAI_API_KEY")):
                result = ai_explain(payload)
                result["source"] = "ai-live"
            else:
                result = offline_explain(payload, deep)
            body = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            self._json_error(502, f"AI API error: {err[:500]}")
        except Exception as e:
            self._json_error(500, str(e))

    def do_GET(self):
        if self.path == "/api/health":
            catalog = load_catalog()
            deep_counts = {e["id"]: len(load_deep(e["id"])) for e in catalog.get("exams", [])}
            body = json.dumps({
                "ok": True,
                "exams": catalog.get("exams", []),
                "deepCounts": deep_counts,
                "hasEnvKey": bool(os.environ.get("OPENAI_API_KEY")),
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def _json_error(self, code, message):
        body = json.dumps({"error": message}).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)


def main():
    catalog = load_catalog()
    with ThreadingTCPServer(("", PORT), Handler) as httpd:
        print(f"Practice app: http://localhost:{PORT}")
        for e in catalog.get("exams", []):
            print(f"  - {e['id']}: {e['title']} ({len(load_deep(e['id']))} deep explanations)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
