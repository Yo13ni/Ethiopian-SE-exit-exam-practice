"""Generate BDU deep explanations via OpenAI — full concept explanation per option."""

import json
import os
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
QUESTIONS = ROOT / "data" / "exams" / "bdu" / "questions.json"
OUT = ROOT / "data" / "exams" / "bdu" / "deep_explanations.json"


def ai_one(q: dict, api_key: str, base_url: str, model: str) -> dict:
    opt_lines = "\n".join(f"{o['key']}. {o['text']}" for o in q["options"])
    prompt = f"""You are tutoring Ethiopian Software Engineering exit exam students.

Topic: {q['topic']}
Question: {q['text']}
Options:
{opt_lines}
Correct answer: {q['answer']}

Write detailed educational JSON. For EVERY option (A,B,C,D):
- Explain the CS/SE CONCEPT that option represents
- For WRONG options: explain WHY that concept does NOT answer THIS specific question (not generic "distractor")
- For CORRECT option: explain the concept and why it fits
- Use 3-5 sentences per option. Never say "common distractor" or "may sound related".

Return JSON only:
{{
  "overview": "4-5 sentences teaching the core concept and solution method",
  "options": {{
    "A": "detailed concept explanation for A",
    "B": "...",
    "C": "...",
    "D": "..."
  }},
  "studyTip": "2 sentences exam memory aid"
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


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("Set OPENAI_API_KEY to generate via AI.")
        print("Example: set OPENAI_API_KEY=sk-... && python generate_bdu_deep.py")
        return

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    data = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    existing = {}
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8"))

    for q in data["questions"]:
        num = str(q["examNumber"])
        print(f"Generating {num}...", flush=True)
        try:
            existing[num] = ai_one(q, api_key, base_url, model)
            OUT.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
            time.sleep(0.5)
        except Exception as e:
            print(f"  Error on {num}: {e}")

    print(f"Done -> {OUT} ({len(existing)} entries)")


if __name__ == "__main__":
    main()
