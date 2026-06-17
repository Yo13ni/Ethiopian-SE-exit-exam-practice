"""Predicted 2018 exit exam v2 — cognitive-domain balanced (Feb 2024 blueprint)."""

from __future__ import annotations

from exam2018_cognitive import FOCUS_GUIDE_COGNITIVE
from exam2018_cognitive_banks import BANK_V2
from exam2018_data import FOCUS_GUIDE, TOPIC_COUNTS

PREDICTED_2018V2_QUESTIONS = BANK_V2

FOCUS_GUIDE_V2 = {**FOCUS_GUIDE, "_blueprint": FOCUS_GUIDE_COGNITIVE}
