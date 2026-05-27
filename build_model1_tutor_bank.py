"""Generate rich tutor-style explanations for every Model Exam 1 question."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from model1_answers import ANSWERS

ROOT = Path(__file__).parent
QUESTIONS_PATH = ROOT / "data" / "exams" / "model1" / "questions.json"
OUT_PATH = ROOT / "data" / "exams" / "model1" / "tutor_bank.json"

# Hand-authored mini-lessons: examNumber -> overview paragraph(s) before the answer line
OVERVIEWS: dict[int, str] = {
    1: (
        "Operating systems use several schedulers at different levels.\n\n"
        "Long-term scheduling admits jobs into the system. Medium-term scheduling swaps processes between RAM and disk. "
        "Short-term scheduling (CPU scheduling) picks which ready process gets the processor. "
        "I/O scheduling orders disk/device requests.\n\n"
        "This question asks: which scheduler decides which available process the CPU executes?"
    ),
    2: (
        "When analyzing algorithms we measure cost under different inputs:\n"
        "Best case = fastest completion, Worst case = slowest, Average case = typical expectation.\n\n"
        "The question asks for the analysis that uses inputs producing the least time."
    ),
    3: (
        "UML behavioral (dynamic) diagrams model how objects behave over time: Sequence, Collaboration, Activity, State.\n"
        "Structural diagrams model structure: Class, Component, Deployment.\n\n"
        "Which option is NOT used for dynamic behavior during analysis?"
    ),
    11: (
        "Decision (branch) coverage requires each decision outcome (True/False) to be tested at least once.\n"
        "Count each if/else condition in the nested fragment separately.\n\n"
        "Decisions: (1) width > length, (2) height > width, (3) height > length — each needs T and F."
    ),
    19: (
        "Trace Java pre-increment: `++a` changes `a` BEFORE the expression uses it.\n"
        "Start: a = 4 → ++a makes a = 5 → then 5 * 5 = ?"
    ),
    22: (
        "Trace the loop: `i < arr.length - 2` with arr.length = 5 means `i < 3`.\n"
        "So i takes values 0, 1, 2 — printing arr[0], arr[1], arr[2]."
    ),
}

# Per-question, per-option teaching notes (examNumber -> key -> text)
OPTION_NOTES: dict[int, dict[str, str]] = {
    1: {
        "A": "Long-term scheduling controls job admission and multiprogramming level. It does not dispatch CPU time to ready processes.",
        "B": "I/O scheduling orders storage device requests — unrelated to CPU process selection.",
        "C": "Short-term scheduling selects a process from the ready queue for CPU execution. This matches the question exactly.",
        "D": "Medium-term scheduling handles swapping processes in/out of memory — not CPU dispatch.",
    },
    2: {
        "A": "Best-case analysis uses inputs that minimize running time — the fastest completion.",
        "B": "Average case is typical performance, not the minimum possible time.",
        "C": "Not a formal analysis category in algorithms courses.",
        "D": "Worst case maximizes running time — opposite of what is asked.",
    },
}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def _answer_line(q: dict) -> str:
    ans = q["answer"]
    text = next(o["text"] for o in q["options"] if o["key"] == ans)
    return f"\n\n✅ Exact answer: {ans} — {text}"


def _overview(q: dict) -> str:
    n = q["examNumber"]
    if n in OVERVIEWS:
        return OVERVIEWS[n] + _answer_line(q)

    topic = q.get("topic", "General")
    stem = q.get("text", "")
    ans = q["answer"]
    correct = next(o["text"] for o in q["options"] if o["key"] == ans)

    intro = f"Topic: {topic}.\n\n"
    intro += f"Question: {stem}\n\n"

    if re.search(r"not correct|not true|incorrect|false|not among|not a|not the|different from", stem, re.I):
        intro += "Strategy: find the statement that is FALSE or does NOT belong. Eliminate options that are clearly valid definitions.\n\n"
    elif re.search(r"output|following program|following code", stem, re.I):
        intro += "Strategy: trace the code line by line on paper. Write variable values after each statement.\n\n"
    elif re.search(r"complexity|O\(", stem, re.I):
        intro += "Strategy: count nested loops, identify the dominant term, drop constants → Big-O.\n\n"
    else:
        intro += "Strategy: recall the precise definition taught in class, then match each option to that definition.\n\n"

    intro += f"The correct choice is {ans} — {correct}."
    return intro


def _concept_of(option_text: str, topic: str) -> str:
    t = _norm(option_text)
    concepts = [
        (r"short-term|cpu schedul", "Short-term (CPU) scheduling dispatches ready processes to the CPU."),
        (r"long-term", "Long-term scheduling admits jobs and controls multiprogramming."),
        (r"medium-term", "Medium-term scheduling manages swapping between memory and disk."),
        (r"best case", "Best-case analysis minimizes running time."),
        (r"worst case", "Worst-case analysis maximizes running time."),
        (r"opacity", "CSS opacity (0–1) controls element transparency."),
        (r"json\.stringify|stringify", "JSON.stringify() serializes JS objects to JSON strings."),
        (r"ssh|port 22|\b22\b", "SSH uses TCP port 22."),
        (r"scrum", "Scrum is the leading agile project-management framework."),
        (r"protected", "protected access: same class + subclasses."),
        (r"distinct", "SELECT DISTINCT removes duplicate rows."),
        (r"java\.lang\.object", "Every Java class extends java.lang.Object."),
        (r"border-radius", "CSS border-radius rounds corners."),
        (r"confidentiality", "Confidentiality prevents unauthorized disclosure."),
        (r"over fit|overfitting", "Overfitting: great on training data, poor on new data."),
        (r"polymorph|overrid", "Method overriding enables runtime polymorphism."),
        (r"dalvik", "Android runs on Dalvik/ART, not desktop JVM."),
        (r"oncreate", "onCreate() is the first Activity lifecycle callback."),
        (r"spam", "Unsolicited commercial email is spam."),
        (r"logical error", "Logical error: program runs but output is wrong."),
        (r"validation", "Validation = building the right product for stakeholders."),
        (r"verification", "Verification = building the product right per specs."),
        (r"encapsulation.*layer|adding.*header", "Encapsulation adds headers going down the OSI stack."),
        (r"cascade", "ON UPDATE CASCADE propagates primary-key changes to foreign keys."),
        (r"case tools", "CASE tools support SDLC activities like design and debugging."),
        (r"precision", "Precision = true detected faults / all reported faults."),
        (r"robustness", "Robustness = continuing despite unexpected faults."),
        (r"pareto", "Pareto: ~80% of effects from ~20% of causes."),
        (r"gradient descent", "Gradient descent optimizes model parameters iteratively."),
        (r"quad.?tree|\b4\b.*children", "Quad-tree internal nodes have 4 children."),
        (r"fileinputstream", "FileInputStream reads bytes from files in Java."),
        (r"implements payable", "Interfaces use `implements`; method signatures must match exactly."),
        (r"affinity", "Affinity diagrams group ideas into clusters for analysis."),
        (r"bootloader|bootstrap", "Bootloader initializes hardware and loads the OS kernel."),
        (r"integration test", "Integration testing checks combined modules/interfaces."),
        (r"ospf", "OSPF is a network-layer routing protocol (Layer 3)."),
        (r"iostream", "C++ <iostream> provides cin/cout stream I/O."),
        (r"ensemble|bagging|boosting|random forest", "Ensemble methods combine multiple models."),
        (r"lasso", "Lasso is L1 regularization — not an ensemble method."),
        (r"primary key.*not null|not null", "Primary keys must be NOT NULL and unique."),
        (r"for\(.*;.*;", "C/Java for-loop syntax: for(init; condition; update)."),
    ]
    for pat, desc in concepts:
        if re.search(pat, t):
            return desc
    return f"In {topic}, this option refers to: {option_text}."


def _option_body(q: dict, key: str) -> str:
    n = q["examNumber"]
    if n in OPTION_NOTES and key in OPTION_NOTES[n]:
        return OPTION_NOTES[n][key]

    ans = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    text = opts.get(key, "")
    correct_text = opts[ans]
    stem = q.get("text", "")
    topic = q.get("topic", "General")
    concept = _concept_of(text, topic)

    if key == ans:
        return (
            f"✓ CORRECT. {concept} "
            f"This directly satisfies what the question asks. "
            f"On the exam, when you see wording like \"{stem[:80]}…\", "
            f"the standard answer is {ans}: {correct_text}."
        )

    return (
        f"✗ Not the answer. {concept} "
        f"However, this question specifically requires: {correct_text} (option {ans}). "
        f"Re-read the stem and match the exact term/definition — do not pick a related but different concept."
    )


def build_entry(q: dict) -> dict[str, Any]:
    tips = {
        "Operating Systems": "Draw the scheduling levels: admit → swap → CPU dispatch. Know boot sequence: BIOS → bootloader → kernel.",
        "Java / OOP": "Trace every code question on paper. Abstract methods must match signature exactly.",
        "Networking": "Label each scenario with an OSI layer before choosing.",
        "Database": "PK = unique + NOT NULL. CASCADE updates FK when PK changes.",
        "Software Testing": "Unit → Integration → System. Decision coverage = every branch T and F.",
        "Web Development": "HTML=structure, CSS=presentation, JS=behavior.",
        "Android": "Lifecycle: onCreate first. APK = Android Package Kit.",
        "AI / ML": "Agent + Environment. Ensemble ≠ Lasso. Overfitting = memorizes training data.",
        "Security": "CIA: Confidentiality, Integrity, Availability.",
        "Project Management": "Validation=right product. Verification=built correctly. Project=temporary unique endeavor.",
    }
    topic = q.get("topic", "General")
    return {
        "overview": _overview(q),
        "options": {k: _option_body(q, k) for k in "ABCD" if k in {o["key"] for o in q["options"]}},
        "studyTip": tips.get(topic, f"Master core {topic} definitions — exit exams test precise terminology."),
    }


def main() -> None:
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    bank: dict[str, dict] = {}
    for q in data["questions"]:
        bank[str(q["examNumber"])] = build_entry(q)
    OUT_PATH.write_text(json.dumps(bank, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote tutor bank for {len(bank)} questions -> {OUT_PATH}")


if __name__ == "__main__":
    main()
