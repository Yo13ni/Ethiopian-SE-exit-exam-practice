"""Practice app server: static files + offline explanations API."""

import json
import os
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingTCPServer

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
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
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def translate_path(self, path: str) -> str:
        clean = path.split("?", 1)[0]
        if clean.startswith("/data/"):
            rel = clean[len("/data/") :]
            return str((ROOT / "data" / rel).resolve())
        return super().translate_path(path)

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
            exam_id = payload.get("examId", "2015")
            deep = load_deep(exam_id)
            result = offline_explain(payload, deep)
            body = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
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
        first = args[0] if args else ""
        if isinstance(first, str) and "/api/" in first:
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
