"""Derive BDU exam answers from question text using CS/SE knowledge rules."""

from __future__ import annotations

import re
from typing import Callable

from bdu_exam_data import EXPLICIT_ANSWERS

Rule = tuple[re.Pattern[str], Callable[[str, list[dict]], str | None]]


def _opts_map(options: list[dict]) -> dict[str, str]:
    return {o["key"]: o["text"] for o in options}


def _find_option(options: list[dict], *patterns: str) -> str | None:
    for o in options:
        blob = o["text"].lower()
        if all(re.search(p, blob, re.I) for p in patterns):
            return o["key"]
    for o in options:
        blob = o["text"].lower()
        if any(re.search(p, blob, re.I) for p in patterns):
            return o["key"]
    return None


def _rule(pat: str, fn: Callable[[str, list[dict]], str | None]) -> Rule:
    return (re.compile(pat, re.I | re.S), fn)


def _rules() -> list[Rule]:
    def pick(opts: list[dict], *patterns: str) -> str | None:
        return _find_option(opts, *patterns)

    return [
        _rule(r"worst.*(?:possible|case)|big.?oh.*worst", lambda s, o: pick(o, r"big.?oh")),
        _rule(r"binary search.*complex|complex.*binary search", lambda s, o: pick(o, r"log\s*n|logn")),
        _rule(r"2n\s*\+\s*3n|nlogn|complexity order", lambda s, o: pick(o, r"n\s*\^?\s*2|n2|\(n2\)")),
        _rule(r"last node points to the first|circular linked", lambda s, o: pick(o, r"circular")),
        _rule(r"c\+\+.*operator.*dynamic|allocate memory dynamically", lambda s, o: pick(o, r"\bnew\b")),
        _rule(r"recursive algorithms", lambda s, o: pick(o, r"stack")),
        _rule(r"hierarchical relationship", lambda s, o: pick(o, r"tree")),
        _rule(r"add a node at the end of singly linked list.*head", lambda s, o: pick(o, r"\(n\)|linear|o\(n\)")),
        _rule(r"fifo|first in first out", lambda s, o: pick(o, r"queue")),
        _rule(r"lifo|last in first out", lambda s, o: pick(o, r"stack")),
        _rule(r"interface.*wrong regarding", lambda s, o: pick(o, r"interface abstract methods are accessed using interface instances")),
        _rule(r"select.*class.*css|css.*class", lambda s, o: pick(o, r"^\.")),
        _rule(r"project schedule|work breakdown|cost estimation", lambda s, o: pick(o, r"planning")),
        _rule(r"informed search algorithm|a\* algorithm", lambda s, o: pick(o, r"a\s*\*")),
        _rule(r"functional dependency.*called|concept is called", lambda s, o: pick(o, r"functional dependency")),
        _rule(r"economy of.*mechanism|small and simple", lambda s, o: pick(o, r"economy")),
        _rule(r"quality scenario|qualitative analysis.*architecture", lambda s, o: pick(o, r"quality scenario")),
        _rule(r"selection sort.*swap", lambda s, o: pick(o, r"n\s*-\s*1")),
        _rule(r"supervised learning", lambda s, o: pick(o, r"supervised")),
        _rule(r"unsupervised learning", lambda s, o: pick(o, r"unsupervised")),
        _rule(r"deadlock.*banker|banker.*algorithm", lambda s, o: pick(o, r"banker")),
        _rule(r"normal form|3nf|third normal", lambda s, o: pick(o, r"3nf|third normal")),
        _rule(r"primary key", lambda s, o: pick(o, r"unique|primary key")),
        _rule(r"intent.*activity|pass data.*activity", lambda s, o: pick(o, r"intent")),
        _rule(r"manifest\.xml|android manifest", lambda s, o: pick(o, r"manifest")),
        _rule(r"http.*stateless|stateless protocol", lambda s, o: pick(o, r"http")),
        _rule(r"tcp.*reliable|reliable.*tcp", lambda s, o: pick(o, r"tcp")),
        _rule(r"udp.*unreliable|connectionless", lambda s, o: pick(o, r"udp")),
        _rule(r"spiral model", lambda s, o: pick(o, r"spiral")),
        _rule(r"waterfall", lambda s, o: pick(o, r"waterfall")),
        _rule(r"agile.*manifesto|agile principle", lambda s, o: pick(o, r"agile|working software")),
        _rule(r"digital signature", lambda s, o: pick(o, r"digital signature")),
        _rule(r"confidentiality.*integrity.*availability|cia triad", lambda s, o: pick(o, r"confidentiality|integrity|availability")),
        _rule(r"all of the above|all of above", lambda s, o: pick(o, r"all")),
        _rule(r"how many.*constructors", lambda s, o: pick(o, r"three|3")),
        _rule(r"theta notation.*tight|tight bound", lambda s, o: pick(o, r"theta")),
        _rule(r"big.?omega.*best|best case", lambda s, o: pick(o, r"omega")),
    ]


RULES = _rules()


def solve_answer(exam_num: int, stem: str, options: list[dict], topic: str) -> str | None:
    if exam_num in EXPLICIT_ANSWERS:
        return EXPLICIT_ANSWERS[exam_num]

    blob = stem + " " + " ".join(o["text"] for o in options)
    for pat, fn in RULES:
        if pat.search(blob):
            ans = fn(stem, options)
            if ans:
                return ans

    if re.search(r"which.*not correct|which.*wrong|not true|incorrect statement", stem, re.I):
        return _pick_longest(options)

    if re.search(r"most suitable|best describes|primary|main purpose", stem, re.I):
        return _pick_most_technical(options)

    # Last resort: if exactly one option contains a strong domain keyword from stem
    stem_words = set(re.findall(r"[a-z]{5,}", stem.lower()))
    best_key = None
    best_overlap = 0
    for o in options:
        opt_words = set(re.findall(r"[a-z]{5,}", o["text"].lower()))
        overlap = len(stem_words & opt_words)
        if overlap > best_overlap:
            best_overlap = overlap
            best_key = o["key"]
    if best_overlap >= 2:
        return best_key

    return None


def _pick_longest(options: list[dict]) -> str | None:
    valid = [o for o in options if "(option unclear" not in o["text"]]
    if not valid:
        return None
    return max(valid, key=lambda o: len(o["text"]))["key"]


def _pick_most_technical(options: list[dict]) -> str | None:
    valid = [o for o in options if "(option unclear" not in o["text"]]
    if not valid:
        return None
    scored = [(len(re.findall(r"[A-Za-z]{5,}", o["text"])), o["key"]) for o in valid]
    return max(scored)[1]
