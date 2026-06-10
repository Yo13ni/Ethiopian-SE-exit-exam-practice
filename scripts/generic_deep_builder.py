"""Rich offline deep explanations from question + answer metadata."""

from __future__ import annotations

import re
from typing import Any


def _opt(correct: str, key: str, text: str, body: str) -> str:
    tag = "CORRECT" if key == correct else "INCORRECT"
    return f'Option {key} ({tag}): "{text}". {body}'


def _why_correct(topic: str, text: str, question: str) -> str:
    return (
        f"This is the best match for what the question asks in {topic}. "
        f'"{text}" aligns with standard software-engineering curriculum definitions and the stem: '
        f"{question[:120]}{'…' if len(question) > 120 else ''}. "
        f"On exit exams, when an option states the canonical rule or notation taught in class, choose it unless the wording is clearly wrong."
    )


def _why_wrong(topic: str, text: str, correct: str, correct_text: str) -> str:
    return (
        f'"{text}" is a common distractor in {topic}. '
        f"It may sound related, but it does not satisfy the specific requirement in the stem. "
        f"Compare carefully with the correct choice ({correct}: {correct_text[:80]}{'…' if len(correct_text) > 80 else ''}). "
        f"Students often pick this when they recognize a keyword from the topic but miss the precise concept being tested."
    )


def _overview(q: dict) -> str:
    topic = q.get("topic", "General")
    answer = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    correct_text = opts.get(answer, "")
    stem = q.get("text", "")

    return (
        f"This {topic} question evaluates whether you can identify the right concept, rule, or complexity class. "
        f"The stem asks: {stem[:200]}{'…' if len(stem) > 200 else ''} "
        f"The correct answer is {answer} — {correct_text}. "
        f"Read every option literally; exit exams often trap you with partially true statements that fail one detail."
    )


def _study_tip(topic: str, q: dict) -> str:
    tips = {
        "Data Structures": "Write the algorithm on paper and count dominant terms or trace one small example before picking complexity.",
        "Java / OOP": "Recall Java language rules: interfaces, constructors, exceptions, and what Java forbids (e.g., pointers).",
        "Database": "Normalize step-by-step, check keys and FDs, and verify SQL syntax against relational algebra meaning.",
        "Networking": "Map the scenario to OSI/TCP layers, protocol behavior, or topology properties before choosing.",
        "Security": "Use Saltzer-Schroeder principles and CIA triad vocabulary to eliminate distractors quickly.",
        "Software Architecture": "Think quality attributes and ATAM scenarios—not team size or log files.",
        "Software Testing": "Match the question to test levels, coverage types, or traceability definitions.",
        "Project Management": "Identify lifecycle model, risk strategy, or WBS/critical-path terminology explicitly asked.",
        "AI / ML": "Classify learning type or search strategy (informed vs uninformed, optimal vs greedy).",
        "Operating Systems": "Relate to process states, scheduling, memory policies, or deadlock conditions.",
        "Web Development": "Check HTTP methods, CSS selectors, DOM APIs, and client-server roles.",
        "Android": "Activity/Intent/Service/Manifest rules are high-frequency on Ethiopian exit exams.",
        "C++": "Trace small code fragments and validate syntax against C++ compilation rules.",
        "Software Engineering": "SRS, requirements, maintenance types, and SDLC phases appear often—match exact definitions.",
    }
    base = tips.get(topic, f"Review your {topic} lecture notes and redo similar MCQs under timed conditions.")
    return f"{base} Flag this question if the wording was OCR-noisy and verify against your course slides."


def build_deep_entry(q: dict) -> dict[str, Any]:
    correct = q["answer"]
    topic = q.get("topic", "General")
    stem = q.get("text", "")
    opts = {o["key"]: o["text"] for o in q["options"]}
    correct_text = opts.get(correct, "")

    options_out: dict[str, str] = {}
    for key in "ABCD":
        text = opts.get(key, "(option text unclear in OCR)")
        if key == correct:
            body = _why_correct(topic, text, stem)
        else:
            body = _why_wrong(topic, text, correct, correct_text)
        options_out[key] = _opt(correct, key, text, body)

    return {
        "overview": _overview(q),
        "options": options_out,
        "studyTip": _study_tip(topic, q),
    }


def enrich_with_concept(q: dict, entry: dict) -> dict:
    concept = q.get("concept", "")
    if concept and concept not in entry["overview"]:
        entry["overview"] = entry["overview"] + " " + concept
    return entry
