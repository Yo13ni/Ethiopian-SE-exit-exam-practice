"""Generate detailed offline explanations via OpenAI (optional) or write curated batch."""

import json
import os
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
QUESTIONS = ROOT / "data" / "exams" / "2015" / "questions.json"
OUT = ROOT / "data" / "exams" / "2015" / "deep_explanations.json"


def ai_one(q: dict, api_key: str, base_url: str, model: str) -> dict:
    opt_lines = "\n".join(f"{o['key']}. {o['text']}" for o in q["options"])
    prompt = f"""You are tutoring Software Engineering exit exam students.

Topic: {q['topic']}
Question: {q['text']}
Options:
{opt_lines}
Correct: {q['answer']}

Write detailed JSON:
{{
  "overview": "3-4 sentences teaching the core concept",
  "options": {{
    "A": "4-6 sentences on A — definition, why wrong/right, mini example",
    "B": "...",
    "C": "...",
    "D": "..."
  }},
  "studyTip": "2 sentences on how to remember this for the exam"
}}"""

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return json.loads(data["choices"][0]["message"]["content"])


def main():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("Set OPENAI_API_KEY to generate via AI.")
        print("Example: set OPENAI_API_KEY=sk-... && python generate_deep_explanations.py")
        return

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    data = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    existing = {}
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8"))

    for q in data["questions"]:
        num = str(q["examNumber"])
        if num in existing:
            print(f"Skip {num}")
            continue
        print(f"Generating {num}...", flush=True)
        try:
            existing[num] = ai_one(q, api_key, base_url, model)
            OUT.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
            time.sleep(0.5)
        except Exception as e:
            print(f"  Error: {e}")

    print(f"Done -> {OUT} ({len(existing)} entries)")


if __name__ == "__main__":
    main()
