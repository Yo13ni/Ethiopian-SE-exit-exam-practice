import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data" / "exams"
YEARS = ["2015", "2016", "2017"]


def bucket(topic: str) -> str:
    m = {
        "Fundamentals of Programming": "Fund. Programming",
        "C++": "Fund. Programming",
        "Data Structures": "DSA",
        "Java / OOP": "OOP",
        "Web Development": "Web Programming",
        "Android": "Mobile Dev",
        "Database": "Database",
        "Operating Systems": "OS",
        "Software Engineering": "Fund. SE",
        "Software Architecture": "Arch & Design",
        "Software Testing": "Testing & QA",
        "Project Management": "SPM",
        "Networking": "Networking",
        "Security": "Info Security",
        "AI / ML": "AI/ML",
        "General": "General",
    }
    return m.get(topic, "Other")


def load_questions(year: str):
    return json.loads((BASE / year / "questions.json").read_text(encoding="utf-8"))["questions"]


def main():
    print("=== BUCKET COUNTS BY YEAR ===")
    year_buckets = {}
    for y in YEARS:
        bc = Counter(bucket(q["topic"]) for q in load_questions(y))
        year_buckets[y] = bc
        print(f"\n{y} (n={sum(bc.values())}):")
        for k, v in bc.most_common():
            print(f"  {k:20} {v:3}")

    bp_collapsed = {
        "Fund. Programming": 11,
        "DSA": 6,
        "OOP": 5,
        "Web Programming": 9,
        "Mobile Dev": 5,
        "Database": 6,
        "OS": 6,
        "Fund. SE": 16,
        "Arch & Design": 5,
        "SPM": 5,
        "Testing & QA": 5,
        "Networking": 6,
        "Info Security": 5,
        "AI/ML": 10,
    }

    recent = Counter()
    for y in ["2016", "2017"]:
        recent.update(bucket(q["topic"]) for q in load_questions(y))
    recent_avg = {k: v / 2 for k, v in recent.items()}
    total_recent = sum(recent_avg.get(k, 0) for k in bp_collapsed) or 1

    pred = {}
    for k, bp in bp_collapsed.items():
        tr = recent_avg.get(k, 0) / total_recent * 100
        pred[k] = round(0.55 * bp + 0.45 * tr)
    pred["Fund. SE"] += 100 - sum(pred.values())

    print("\n=== 2018 PREDICTED DISTRIBUTION (~100 Q) ===")
    for k in sorted(pred, key=lambda x: -pred[x]):
        print(f"  {k:20} {pred[k]:3}")

    print("\n=== RECURRING QUESTION PATTERNS ===")
    patterns = Counter()
    for y in YEARS:
        for q in load_questions(y):
            t = q["text"].lower()
            if "which of the following" in t or "which one of" in t:
                patterns["Which-of-the-following MCQ"] += 1
            elif t.startswith("what"):
                patterns["What is/are definition"] += 1
            elif any(w in t for w in ["calculate", "compute", "subnet", "how many hosts"]):
                patterns["Calculation (subnet/complexity)"] += 1
            elif any(w in t for w in ["code", "for(", "public class", "int main", "output"]):
                patterns["Code trace / output"] += 1
            elif "true" in t and "false" in t:
                patterns["True/False style"] += 1
            else:
                patterns["Scenario / best answer"] += 1
    for p, c in patterns.most_common():
        print(f"  {p}: {c} total across 3 years (~{c//3}/exam)")

    print("\n=== TOPICS TESTED HEAVILY IN 2015 BUT LESS IN 2017 (may return) ===")
    for k in sorted(bp_collapsed):
        d = year_buckets["2017"].get(k, 0) - year_buckets["2015"].get(k, 0)
        if d <= -3:
            print(f"  {k}: {year_buckets['2015'].get(k,0)} (2015) -> {year_buckets['2017'].get(k,0)} (2017)")


if __name__ == "__main__":
    main()
