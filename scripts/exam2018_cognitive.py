"""MoEE Feb 2024 blueprint cognitive domain helpers for predicted 2018 exams."""

from __future__ import annotations

from collections import Counter

# MoEE Feb 2024 blueprint: cognitive + affective domains total 100 items
# (Remember 3 + Understand 21 + Apply 22 + Analyze 10 + Evaluate 6 + Create 33 + Affective 5)
BLUEPRINT_COGNITIVE_TOTALS = {
    "Remember": 3,
    "Understand": 21,
    "Apply": 22,
    "Analyze": 10,
    "Evaluate": 6,
    "Create": 33,
    "Affective": 5,
}


def q(
    topic: str,
    text: str,
    opts: list[str],
    answer: str,
    concept: str,
    cognitive: str,
) -> dict:
    keys = "ABCD"
    return {
        "topic": topic,
        "text": text,
        "options": [{"key": k, "text": t} for k, t in zip(keys, opts)],
        "answer": answer,
        "concept": f"Key idea ({topic}): {concept}",
        "cognitiveLevel": cognitive,
    }


def validate_bank(questions: list[dict], topic_counts: dict[str, int]) -> None:
    assert len(questions) == 100, len(questions)
    tc = Counter(q["topic"] for q in questions)
    for topic, n in topic_counts.items():
        assert tc[topic] == n, f"{topic}: expected {n}, got {tc[topic]}"
    cc = Counter(q["cognitiveLevel"] for q in questions)
    for level, n in BLUEPRINT_COGNITIVE_TOTALS.items():
        assert cc[level] == n, f"{level}: expected {n}, got {cc[level]}"


FOCUS_GUIDE_COGNITIVE = (
    "Feb 2024 MoEE blueprint mix: Remember 3 · Understand 21 · Apply 22 · Analyze 10 · "
    "Evaluate 6 · Create 33 · Affective 5. Questions use scenarios, traces, design choices, "
    "and professional-judgment stems—not simple definition recall."
)
