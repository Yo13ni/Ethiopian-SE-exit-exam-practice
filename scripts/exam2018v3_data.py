"""Predicted 2018 exit exam v3 — MoEE blueprint credit-hour + cognitive domains."""

from __future__ import annotations

from exam2018_cognitive import FOCUS_GUIDE_COGNITIVE
from exam2018_cognitive_banks import BANK_V3, TOPIC_COUNTS_V3

TOPIC_COUNTS = TOPIC_COUNTS_V3

FOCUS_GUIDE = {
    "Fundamentals of Programming": "Blueprint 11% programming theme — algorithms, modular design, debugging traces.",
    "C++": "Syntax traces, memory, references, and OOP-based design choices.",
    "Data Structures": "Structure selection, complexity analysis, BFS/DFS, sorting/search reasoning.",
    "Java / OOP": "Polymorphism, interfaces, exceptions, GUI/event-driven design.",
    "Web Development": "Blueprint 9 items — HTTP/API design, AJAX, sessions, responsive integration.",
    "Android": "Components, lifecycle, permissions, ethical mobile design.",
    "Database": "Normalization, SQL, transactions, integrity incidents.",
    "Operating Systems": "Scheduling, deadlock, paging, synchronization design.",
    "Software Engineering": "Requirements, change control, maintenance, release planning.",
    "Software Architecture": "Quality attributes, patterns, service boundaries, scalability.",
    "Project Management": "WBS, EVM, risk register, agile/waterfall trade-offs.",
    "Software Testing": "Test plans, coverage, regression, incident reporting.",
    "Networking": "Subnetting, routing, OSI/TCP behavior, campus network design.",
    "Security": "Threat modeling, crypto, access control, incident response.",
    "AI / ML": "Search, logic, supervised/unsupervised ML, model evaluation pipelines.",
    "_blueprint": FOCUS_GUIDE_COGNITIVE,
}

PREDICTED_2018V3_QUESTIONS = BANK_V3
