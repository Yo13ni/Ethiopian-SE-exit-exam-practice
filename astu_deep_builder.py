"""Deep explanations for ASTU Software Engineering MCQs (no BDU curated bank)."""

from __future__ import annotations

import re
from typing import Any

from bdu_concept_engine import build_overview, explain_correct_option, explain_wrong_option


def _opt(correct: str, key: str, text: str, body: str) -> str:
    tag = "CORRECT" if key == correct else "INCORRECT"
    return f'Option {key} ({tag}): "{text}". {body}'


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def _explain_se(stem: str, key: str, text: str, correct: str) -> str | None:
    s, t = _norm(stem), _norm(text)

    if "first step" in s and "software development lifecycle" in s:
        if "preliminary" in t or "investigation" in t:
            return (
                "SDLC begins with preliminary investigation and analysis — understanding the problem, "
                "feasibility, scope, and initial requirements before design or coding."
                if key == correct
                else "This phase comes after requirements are understood."
            )
        if "design" in t:
            return "System design follows requirements analysis — it is not the first SDLC step."
        if "coding" in t:
            return "Coding is an implementation activity that happens after analysis and design."
        if "testing" in t:
            return "Testing validates built software — it cannot be the first lifecycle step."

    if "study of an existing system" in s:
        if "system analysis" in t:
            return "Studying an existing system to understand how it works is system analysis." if key == correct else ""
        if "feasibility" in t:
            return "Feasibility study decides whether a project is viable — broader than studying the current system alone."
        if "planning" in t:
            return "System planning schedules work; analysis focuses on understanding the current system."

    if "rad stand for" in s or s.startswith("what does rad stand"):
        if "rapid application development" in t:
            return "RAD = Rapid Application Development — iterative prototyping with heavy user involvement." if key == correct else ""
        if "document" in t:
            return "RAD is about development speed and prototyping, not a 'document' acronym."

    if "prototyp" in s and "not associated" in s and "diagonal" in t:
        return "Common prototype types are horizontal (UI layer), vertical (full stack slice), and domain — not 'diagonal'." if key == correct else ""

    if "drawback of rad" in s:
        if "highly skilled" in t:
            return "RAD needs skilled teams and active users; 'both (a) and (c)' captures multiple drawbacks." if key == correct else ""
        if "both" in t:
            return "RAD drawbacks include needing skilled developers AND tight user feedback — not increased reusability as a drawback."

    if "drawback of the spiral model" in s:
        if "smaller projects" in t:
            return "Spiral's overhead (risk analysis, iterations) makes it heavy for small projects." if key == correct else ""
        if "risk analysis" in t:
            return "More risk analysis is a feature of Spiral, not its major drawback."

    if "4gt" in s or "fourth generation" in s:
        if "unix shell" in t and "fourth generation" in s:
            return "4GL examples include Unix shell, SQL, and report generators — high-level, problem-oriented languages." if key == correct else ""
        if "time required" in s and "advantage" in s:
            return "4GT's main advantage is faster development by generating code from high-level specs." if key == correct else ""

    if "cocomo" in s:
        if "both cocomo and fp" in t or ("cocomo" in t and "fp" in t):
            return "COCOMO and function-point-based estimation both predict effort from size metrics." if key == correct else ""
        if "application composition" in t and "requirements are stabilized" in s:
            return "After requirements stabilize and architecture is set, COCOMO uses the post-architecture/application composition stage." if key == correct else ""

    if "df d" in s.replace(" ", "") or "data flow diagram" in s:
        if "data flow" in t and ("directed arc" in s or "arc or line" in s):
            return "In a DFD, directed arcs represent data flow between processes, stores, and external entities." if key == correct else ""
        if "data store" in s and "logical file" in t:
            return "A data store symbol can represent logical files, physical files, or data structures." if key == correct else ""

    if "aviation industry" in s and "rtcado" in t.replace(" ", ""):
        return "DO-178B (RTCADO-178B in OCR) is the aviation software standard." if key == correct else ""

    if "third-party certification" in s and "1998" in t:
        return "UL 1998 Second Edition is referenced for third-party software safety certification." if key == correct else ""

    return None


def build_deep_entry(q: dict) -> dict[str, Any]:
    correct = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    options_out: dict[str, str] = {}

    for key in "ABCD":
        text = opts.get(key, "(option unclear in OCR)")
        if key == correct:
            body = _explain_se(q.get("text", ""), key, text, correct) or explain_correct_option(q, text)
        else:
            body = _explain_se(q.get("text", ""), key, text, correct) or explain_wrong_option(q, key, text)
        options_out[key] = _opt(correct, key, text, body)

    tips = {
        "Software Engineering": "Map each question to SDLC phase, process model, or 4GT/RAD/Agile definition before choosing.",
        "Project Management": "COCOMO stages, estimation techniques, and risk terms (identification vs projection) are high yield.",
        "Software Testing": "Distinguish black-box vs white-box, maintenance retesting, and ISO quality models.",
        "Software Architecture": "RUP perspectives, behavioral vs data models, reengineering vs forward engineering.",
        "General": "DFD symbols, structured analysis steps, and certification standards (DO-178B, UL 1998).",
    }

    return {
        "overview": build_overview(q),
        "options": options_out,
        "studyTip": tips.get(q.get("topic", ""), "Review Software Engineering process models and definitions from your course notes."),
    }


def enrich_with_concept(q: dict, entry: dict) -> dict:
    concept = q.get("concept", "")
    if concept and concept not in entry["overview"]:
        entry["overview"] = entry["overview"] + " " + concept
    entry["source"] = "offline-deep"
    return entry
