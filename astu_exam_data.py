"""Manual overrides and focus guide for ASTU Software Engineering exam."""

from __future__ import annotations

FOCUS_GUIDE: dict[str, str] = {
    "Software Engineering": "SDLC phases, process models (Waterfall, Spiral, RAD, Agile), and 4GT.",
    "Project Management": "COCOMO, estimation, metrics, risk management, and configuration management.",
    "Software Testing": "Black-box testing, maintenance testing, and quality models.",
    "Software Architecture": "RUP, behavioral/context models, and reengineering.",
    "General": "Structured analysis, DFD notation, and software standards.",
}

MANUAL_OVERRIDES: dict[int, dict] = {
    40: {
        "options": [
            {"key": "A", "text": "Transformation of a textual problem description into a graphic model"},
            {"key": "B", "text": "Functional decomposition"},
            {
                "key": "C",
                "text": "All the functions represented in the DFD are mapped to a module structure",
            },
            {"key": "D", "text": "All of the mentioned"},
        ],
    },
}
