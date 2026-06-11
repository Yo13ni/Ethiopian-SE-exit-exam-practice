"""Reorder 2016 questions to match OCR Question N headers."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / "data" / "exams" / "2016" / "exitexam_ocr_pages.json"
BANK = ROOT / "data" / "exams" / "2016" / "questions.json"
OUT = ROOT / "data" / "exams" / "2016" / "bank_97.json"

OFFICIAL_COUNT = 97

# Authoritative answers/topics (question number from Moodle header)
AUTH: dict[int, tuple[str, str]] = {
    1: ("A", "Java / OOP"),
    2: ("A", "Web Development"),
    3: ("D", "Project Management"),
    4: ("D", "Java / OOP"),
    5: ("B", "Networking"),
    6: ("C", "Operating Systems"),
    7: ("A", "AI / ML"),
    8: ("D", "Networking"),
    9: ("A", "Database"),
    10: ("B", "Project Management"),
    11: ("C", "Android"),
    12: ("D", "Project Management"),
    13: ("C", "Operating Systems"),
    14: ("D", "Operating Systems"),
    15: ("D", "Android"),
    16: ("B", "Java / OOP"),
    17: ("A", "Security"),
    18: ("C", "Networking"),
    19: ("A", "Security"),
    20: ("A", "Project Management"),
    21: ("A", "Software Engineering"),
    22: ("C", "Data Structures"),
    23: ("C", "Data Structures"),
    24: ("C", "Java / OOP"),
    25: ("C", "Java / OOP"),
    26: ("C", "Android"),
    27: ("D", "Data Structures"),
    28: ("A", "Java / OOP"),
    29: ("A", "Operating Systems"),
    30: ("D", "AI / ML"),
    31: ("A", "Software Testing"),
    32: ("A", "Operating Systems"),
    33: ("D", "Networking"),
    34: ("C", "Software Engineering"),
    35: ("C", "AI / ML"),
    36: ("A", "Android"),
    37: ("C", "AI / ML"),
    38: ("C", "Web Development"),
    39: ("A", "Data Structures"),
    40: ("A", "Database"),
    41: ("A", "Networking"),
    42: ("D", "Software Testing"),
    43: ("C", "Security"),
    44: ("B", "Software Architecture"),
    45: ("A", "Operating Systems"),
    46: ("B", "Software Architecture"),
    47: ("C", "Java / OOP"),
    48: ("D", "Data Structures"),
    49: ("B", "Database"),
    50: ("D", "AI / ML"),
    51: ("D", "Software Architecture"),
    52: ("D", "Networking"),
    53: ("D", "Database"),
    54: ("A", "Software Testing"),
    55: ("A", "Project Management"),
    56: ("D", "Data Structures"),
    57: ("C", "Security"),
    58: ("C", "Software Engineering"),
    59: ("C", "Security"),
    60: ("D", "Project Management"),
    61: ("A", "Software Testing"),
    62: ("D", "Software Testing"),
    63: ("C", "Software Engineering"),
    64: ("D", "Database"),
    65: ("D", "Data Structures"),
    66: ("B", "Software Testing"),
    67: ("D", "C++"),
    68: ("B", "Software Engineering"),
    69: ("C", "Software Engineering"),
    70: ("C", "Software Engineering"),
    71: ("A", "Project Management"),
    72: ("A", "Java / OOP"),
    73: ("C", "Project Management"),
    74: ("D", "C++"),
    75: ("A", "Software Engineering"),
    76: ("B", "Software Testing"),
    77: ("D", "Networking"),
    78: ("B", "AI / ML"),
    79: ("B", "Database"),
    80: ("B", "Java / OOP"),
    81: ("D", "Software Architecture"),
    82: ("D", "AI / ML"),
    83: ("B", "Security"),
    84: ("D", "C++"),
    85: ("B", "Java / OOP"),
    86: ("D", "C++"),
    87: ("D", "C++"),
    88: ("A", "Web Development"),
    89: ("C", "Software Engineering"),
    90: ("D", "Android"),
    91: ("C", "Project Management"),
    92: ("C", "Security"),
    93: ("D", "Android"),
    94: ("D", "AI / ML"),
    95: ("A", "AI / ML"),
    96: ("D", "Database"),
    97: ("C", "Software Engineering"),
}

# Hand-curated clean stems keyed by official question number (OCR order).
CURATED: dict[int, dict] = {
    1: {
        "text": "Which of the following is wrong regarding interface?",
        "options": [
            {"key": "A", "text": "Interface abstract methods are accessed using interface instances"},
            {"key": "B", "text": "Like a class, an interface is a reference data type"},
            {"key": "C", "text": "Interface includes abstract methods"},
            {"key": "D", "text": "One class can implement multiple interfaces"},
        ],
    },
    2: {
        "text": "How can we select an element with a specific class in CSS?",
        "options": [
            {"key": "A", "text": ".classname"},
            {"key": "B", "text": "#classname"},
            {"key": "C", "text": "element.class"},
            {"key": "D", "text": "class: element"},
        ],
    },
    28: {
        "text": "Which of the following is true about abstract class?",
        "options": [
            {"key": "A", "text": "Cannot be instantiated"},
            {"key": "B", "text": "Is a mechanism of encapsulation"},
            {"key": "C", "text": "Can contain both abstract and non-abstract methods"},
            {"key": "D", "text": "Cannot be inherited"},
        ],
    },
    30: {
        "text": (
            "A salesperson at Markato shop noticed people who buy shoes also buy socks with high probability. "
            "Which big data analytics technique best supports this pattern?"
        ),
        "options": [
            {"key": "A", "text": "Clustering algorithm"},
            {"key": "B", "text": "Predictive modeling"},
            {"key": "C", "text": "Regression modeling"},
            {"key": "D", "text": "Association rule"},
        ],
    },
    39: {
        "text": (
            "What is the time complexity for the following code snippet?\n\n"
            "function someFunction(n) {\n"
            "  for (var i = 0; i < n * 10; i++) {\n"
            "    console.log(n);\n"
            "  }\n"
            "}"
        ),
        "options": [
            {"key": "A", "text": "O(n)"},
            {"key": "B", "text": "O(n^2)"},
            {"key": "C", "text": "O(n log n)"},
            {"key": "D", "text": "O(log n)"},
        ],
    },
    80: {
        "text": (
            "The result of the following program after running will be:\n\n"
            "class PrintResult {\n"
            "    public static void main(String[] args) {\n"
            "        int[] arr = {3, 4, 5, 6, 7};\n"
            "        for (int i = 0; i < arr.length - 1; i++)\n"
            "            System.out.print(arr[i]);\n"
            "    }\n"
            "}"
        ),
        "options": [
            {"key": "A", "text": "34567"},
            {"key": "B", "text": "3456"},
            {"key": "C", "text": "34"},
            {"key": "D", "text": "345"},
        ],
    },
}


def norm(s: str) -> str:
    s = re.sub(r"(?i)(not yet answered|marked out.*?|flag question)", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def overlap(a: str, b: str) -> float:
    aw = {w for w in norm(a).split() if len(w) > 3}
    bw = {w for w in norm(b).split() if len(w) > 3}
    if not aw:
        return 0.0
    return len(aw & bw) / len(aw)


def parse_ocr_stems() -> dict[int, str]:
    pages = json.loads(OCR.read_text(encoding="utf-8"))
    by_num: dict[int, str] = {}
    next_guess = 1
    for page in pages:
        m = re.search(r"(?i)\bquestion\s+(\d{1,3})\b", page)
        if m:
            num = int(m.group(1))
            if num >= next_guess:
                next_guess = num + 1
        elif re.search(r"(?i)\bquestion\b", page):
            num = next_guess
            next_guess += 1
        else:
            continue
        if 1 <= num <= OFFICIAL_COUNT:
            prev = by_num.get(num, "")
            if len(page) > len(prev):
                by_num[num] = page
    return by_num


def main() -> None:
    ocr = parse_ocr_stems()
    bank = json.loads(BANK.read_text(encoding="utf-8"))["questions"]
    used: set[int] = set()
    official: list[dict] = []

    for qnum in range(1, OFFICIAL_COUNT + 1):
        if qnum not in ocr:
            raise SystemExit(f"Missing OCR for Q{qnum}")

        if qnum in CURATED:
            body = CURATED[qnum]
        else:
            best_i = None
            best_score = 0.0
            for i, q in enumerate(bank):
                if i in used:
                    continue
                score = overlap(q["text"], ocr[qnum])
                if score > best_score:
                    best_score = score
                    best_i = i
            if best_i is None or best_score < 0.25:
                raise SystemExit(f"Could not match bank entry for official Q{qnum} (best={best_score:.2f})")
            used.add(best_i)
            body = {"text": bank[best_i]["text"], "options": bank[best_i]["options"]}

        ans, topic = AUTH[qnum]
        official.append(
            {
                "id": qnum,
                "text": body["text"].strip(),
                "options": body["options"],
                "answer": ans,
                "topic": topic,
            }
        )

    OUT.write_text(json.dumps(official, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(official)} official questions -> {OUT}")


if __name__ == "__main__":
    main()
