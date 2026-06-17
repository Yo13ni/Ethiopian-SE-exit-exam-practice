"""Classify MCQ stems into MoEE Feb 2024 blueprint cognitive levels."""

from __future__ import annotations

import re

# MoEE Feb 2024 Test Blueprint — six cognitive domain levels (Bloom's taxonomy)
COGNITIVE_LEVELS = (
    "Remembering",
    "Understanding",
    "Application",
    "Analysis",
    "Evaluation",
    "Creation/Synthesis",
)

# Legacy short labels used in predicted 2018v2/v3 banks
LEGACY_LEVEL_MAP = {
    "Remember": "Remembering",
    "Understand": "Understanding",
    "Apply": "Application",
    "Analyze": "Analysis",
    "Evaluate": "Evaluation",
    "Create": "Creation/Synthesis",
    "Affective": "Evaluation",
}

# Ordered highest → lowest; first match wins
_LEVEL_RULES: list[tuple[str, re.Pattern[str]]] = [
    (
        "Creation/Synthesis",
        re.compile(
            r"\b(?:design(?:ing)?|develop(?:ing)?|create(?:ing)?|formulate(?:ing)?|"
            r"construct(?:ing)?|plan(?:ning)?|architect(?:ure)?(?:\s+for|\s+that|\s+to|\s+a)?|"
            r"build(?:ing)?(?:\s+a|\s+an)?\s+(?:system|application|solution|model|database|network)|"
            r"compose(?:\s+a|\s+an)?|propose(?:\s+a|\s+an)?\s+(?:design|solution|architecture))\b",
            re.I,
        ),
    ),
    (
        "Evaluation",
        re.compile(
            r"\b(?:evaluat(?:e|ing)|assess(?:ing)?|judge(?:ing)?|justify(?:ing)?|"
            r"recommend(?:ing)?|critique(?:ing)?|prioriti[sz]e(?:\s+the)?|"
            r"most\s+(?:appropriate|suitable|effective|important|likely)|"
            r"best\s+(?:suited|choice|approach|practice|option|way|method|describes)|"
            r"primary\s+(?:reason|goal|purpose|concern|objective)|"
            r"should\s+(?:you|the\s+(?:team|developer|architect|engineer))\b|"
            r"\b(?:ethical|professional|legal|moral)\b(?:\s+(?:principle|issue|responsibility|norm|dilemma))?|"
            r"\b(?:advantage|disadvantage|drawback|limitation|benefit)s?\s+(?:of|to)\b)",
            re.I,
        ),
    ),
    (
        "Analysis",
        re.compile(
            r"\b(?:analy[sz]e(?:\s+the)?|analy[sz]ing|compare(?:\s+the)?|contrast(?:\s+the)?|"
            r"differentiat(?:e|ing)|distinguish(?:\s+between|\s+the)?|examine(?:\s+the)?|"
            r"investigat(?:e|ing)|break(?:\s+down|\s+into)|decompos(?:e|ing)|"
            r"relationship\s+between|difference\s+between|similarit(?:y|ies)\s+between|"
            r"impact\s+of|effect\s+of|cause\s+of|reason\s+why|why\s+(?:does|do|would|is|are)|"
            r"what\s+would\s+happen|which\s+(?:is|are)\s+not\b|"
            r"\b(?:not|except|incorrect|false|least\s+likely)\b.*\?|"
            r"trade[\s-]?off|complexit(?:y|ies)|bottleneck|root\s+cause)\b",
            re.I,
        ),
    ),
    (
        "Application",
        re.compile(
            r"\b(?:apply(?:ing)?|use(?:\s+the|\s+a|\s+an)?|implement(?:ing)?|solve(?:\s+the)?|"
            r"calculat(?:e|ing)|execut(?:e|ing)|compute(?:\s+the)?|demonstrat(?:e|ing)|"
            r"configur(?:e|ing)|install(?:ing)?|deploy(?:ing)?|write(?:\s+a|\s+an|\s+the)?|"
            r"trace(?:\s+the|\s+through)?|output(?:\s+of|\s+when|\s+if)?|"
            r"result(?:ing|\s+of|\s+when|\s+if)?|given\s+(?:the|a|an|following)|"
            r"what\s+is\s+the\s+(?:output|result|value|answer)|"
            r"which\s+(?:code|statement|query|command|algorithm|method)\s+(?:will|would|should|is\s+used)|"
            r"is\s+used\s+to\s+(?:select|insert|update|delete|create|secure|implement|solve)|"
            r"following\s+(?:code|program|snippet|algorithm|SQL|query))\b",
            re.I,
        ),
    ),
    (
        "Understanding",
        re.compile(
            r"\b(?:explain(?:\s+the|\s+why|\s+how)?|describe(?:\s+the|\s+how)?|"
            r"summari[sz]e(?:\s+the)?|interpret(?:\s+the|\s+the)?|"
            r"purpose\s+of|role\s+of|meaning\s+of|significance\s+of|"
            r"how\s+does(?:\s+the|\s+a|\s+an)?|how\s+do(?:\s+the|\s+a|\s+an)?|"
            r"what\s+(?:does|do)\s+(?:the|a|an)\b|"
            r"which\s+best\s+describes|characteristic(?:s)?\s+of|"
            r"definition\s+of|concept\s+of|fundamental(?:s)?\s+of|"
            r"in\s+the\s+context\s+of\b)",
            re.I,
        ),
    ),
    (
        "Remembering",
        re.compile(
            r"\b(?:recall(?:\s+the)?|state(?:\s+the|\s+how)?|name(?:\s+the)?|list(?:\s+the)?|"
            r"define(?:\s+the|\s+a|\s+an)?|identify(?:\s+the|\s+a|\s+an)?|"
            r"what\s+is\s+called|refers\s+to|stands\s+for|abbreviation\s+for|"
            r"which\s+(?:one|type|component|level|phase|layer|model|pattern|protocol|"
            r"technique|method|tool|term|keyword|feature|property|attribute)\s+(?:of|is|refers|"
            r"represents|describes|corresponds)|"
            r"which\s+of\s+the\s+following\s+(?:is|are|refers|represents|describes|corresponds))\b",
            re.I,
        ),
    ),
]


def normalize_level(level: str | None) -> str | None:
    if not level:
        return None
    level = level.strip()
    if level in COGNITIVE_LEVELS:
        return level
    return LEGACY_LEVEL_MAP.get(level)


def classify_cognitive_level(text: str, concept: str = "", topic: str = "") -> str:
    """Return one of the six MoEE blueprint cognitive levels for a question stem."""
    blob = f"{text} {concept} {topic}".strip()
    if not blob:
        return "Understanding"

    for level, pattern in _LEVEL_RULES:
        if pattern.search(blob):
            return level

    tl = blob.lower()
    if "?" in text and len(text.split()) <= 18:
        return "Remembering"
    if re.search(r"\bwhich\b", tl):
        return "Understanding"
    return "Understanding"


def classify_question(q: dict) -> str:
    existing = normalize_level(q.get("cognitiveLevel"))
    if existing:
        return existing
    return classify_cognitive_level(
        q.get("text", ""),
        q.get("concept", ""),
        q.get("topic", ""),
    )
