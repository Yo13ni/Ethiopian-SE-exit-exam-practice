"""Official 2016 exam set aligned to OCR Question N headers.

This module returns exactly 97 questions (Q1..Q97), where each question number
is resolved from the OCR header text ("Question N ..."), then paired with the
clean question bank entries.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

OFFICIAL_COUNT = 97

_ROOT = Path(__file__).resolve().parent.parent
_OCR_PATH = _ROOT / "data" / "exams" / "2016" / "exitexam_ocr_pages.json"
_BANK_PATH = _ROOT / "data" / "exams" / "2016" / "questions.json"

# Authoritative map provided by user:
# qnum -> (clue, answer, topic)
_AUTH: dict[int, tuple[str, str, str]] = {
    1: ("interface wrong", "A", "Java / OOP"),
    2: ("CSS class selector", "A", "Web Development"),
    3: ("project planning", "D", "Project Management"),
    4: ("Student UML", "D", "Java / OOP"),
    5: ("subnet invalid host", "B", "Networking"),
    6: ("chmod 755", "C", "Operating Systems"),
    7: ("IDA*", "A", "AI / ML"),
    8: ("HTTP request line+header", "D", "Networking"),
    9: ("unstructured Google", "A", "Database"),
    10: ("anti-agile", "B", "Project Management"),
    11: ("Intent", "C", "Android"),
    12: ("conflicting requirements", "D", "Project Management"),
    13: ("blocked->Ready", "C", "Operating Systems"),
    14: ("replacement policy", "D", "Operating Systems"),
    15: ("Manifest all info", "D", "Android"),
    16: ("Payable/Invoice", "B", "Java / OOP"),
    17: ("firewall stop unauthorized", "A", "Security"),
    18: ("NOT crossover switch-to-pc", "C", "Networking"),
    19: ("OAuth Authorization Server", "A", "Security"),
    20: ("ROI 20%", "A", "Project Management"),
    21: ("layered architecture ordering", "A", "Software Engineering"),
    22: ("Tree non-linear", "C", "Data Structures"),
    23: ("time complexity O(n^3)", "C", "Data Structures"),
    24: ("try-catch wrong catch once", "C", "Java / OOP"),
    25: ("Class_B String welcome()", "C", "Java / OOP"),
    26: ("ViewGroup", "C", "Android"),
    27: ("algorithm NOT language details", "D", "Data Structures"),
    28: ("abstract class cannot be instantiated", "A", "Java / OOP"),
    29: ("NOT process creation multiple execution", "A", "Operating Systems"),
    30: ("association rule Markato", "D", "AI / ML"),
    31: ("tester documents faults", "A", "Software Testing"),
    32: ("NOT banker's scheduling algorithm", "A", "Operating Systems"),
    33: ("collision retry delay", "D", "Networking"),
    34: ("generalization NOT higher more specific", "C", "Software Engineering"),
    35: ("DA vs UCS", "C", "AI / ML"),
    36: ("Android Activity", "A", "Android"),
    37: ("data mining Training Testing Evaluation Deployment", "C", "AI / ML"),
    38: ("JS substring itex", "C", "Web Development"),
    39: ("loop n*10 O(n)", "A", "Data Structures"),
    40: ("2NF", "A", "Database"),
    41: ("switches increase collision domains", "A", "Networking"),
    42: ("testing meets requirements", "D", "Software Testing"),
    43: ("SSH secure channel", "C", "Security"),
    44: ("API gateway", "B", "Software Architecture"),
    45: ("deadlock", "A", "Operating Systems"),
    46: ("architecture NOT considered distribution", "B", "Software Architecture"),
    47: ("inheritance Pet", "C", "Java / OOP"),
    48: ("best case", "D", "Data Structures"),
    49: ("NOT database feature app-data dependency", "B", "Database"),
    50: ("Agent", "D", "AI / ML"),
    51: ("architecture doc NOT source code flow", "D", "Software Architecture"),
    52: ("Internet Layer", "D", "Networking"),
    53: ("database coherent all attributes related", "D", "Database"),
    54: ("decision coverage 4 tests", "A", "Software Testing"),
    55: ("project lifecycle NOT true", "A", "Project Management"),
    56: ("queues indirect multiprogramming", "D", "Data Structures"),
    57: ("confidentiality", "C", "Security"),
    58: ("Memento pattern", "C", "Software Engineering"),
    59: ("ACL classify traffic", "C", "Security"),
    60: ("Tuckman forming storming norming performing adjourning", "D", "Project Management"),
    61: ("testing NOT requesting more time", "A", "Software Testing"),
    62: ("config management test planning", "D", "Software Testing"),
    63: ("maintainability fine-grain", "C", "Software Engineering"),
    64: ("HOTEL INSERT", "D", "Database"),
    65: ("LIFO queue", "D", "Data Structures"),
    66: ("branch coverage", "B", "Software Testing"),
    67: ("C++ 4^3=64", "D", "C++"),
    68: ("evolution sequence", "B", "Software Engineering"),
    69: ("UML wrong Activity for events", "C", "Software Engineering"),
    70: ("traceability wrong cost/schedule", "C", "Software Engineering"),
    71: ("Pareto", "A", "Project Management"),
    72: ("constructor", "A", "Java / OOP"),
    73: ("Agile changing environment", "C", "Project Management"),
    74: ("continue", "D", "C++"),
    75: ("functional vs non-functional", "A", "Software Engineering"),
    76: ("test analysis and design", "B", "Software Testing"),
    77: ("OSI bit frame packet segment", "D", "Networking"),
    78: ("unsupervised learning", "B", "AI / ML"),
    79: ("DORM FK in STUDENT", "B", "Database"),
    80: ("PrintResult 3456", "B", "Java / OOP"),
    81: ("architectural quality attributes", "D", "Software Architecture"),
    82: ("AI definition", "D", "AI / ML"),
    83: ("risk retention", "B", "Security"),
    84: ("C++ linking last", "D", "C++"),
    85: ("Java switch fall-through Hello You welcome", "B", "Java / OOP"),
    86: ("C++ for loop", "D", "C++"),
    87: ("C++ identifier variable_1234", "D", "C++"),
    88: ("form GET", "A", "Web Development"),
    89: ("incremental model", "C", "Software Engineering"),
    90: ("Linux Kernel", "D", "Android"),
    91: ("resource leveling", "C", "Project Management"),
    92: ("NOT WannaCry", "C", "Security"),
    93: ("APK Package Kit", "D", "Android"),
    94: ("automatic programming", "D", "AI / ML"),
    95: ("business understanding first", "A", "AI / ML"),
    96: ("database design sequence", "D", "Database"),
    97: ("design principle NOT reinvent wheel", "C", "Software Engineering"),
}


def _extract_ocr_headers() -> dict[int, str]:
    pages: list[str] = json.loads(_OCR_PATH.read_text(encoding="utf-8"))
    by_num: dict[int, str] = {}
    next_guess = 1
    for raw in pages:
        text = str(raw)
        nums = re.findall(r"(?i)\bquestion\s+(\d{1,3})\b", text)
        if not nums:
            nums = re.findall(r"(?i)\bq\w*tion\s+(\d{1,3})\b", text)
        if nums:
            qnum = int(nums[0])
            if qnum >= next_guess:
                next_guess = qnum + 1
        elif re.search(r"(?i)\bquestion\b", text):
            # OCR sometimes drops the numeral (e.g., "Question Not yet ...").
            qnum = next_guess
            next_guess += 1
        else:
            continue
        if not (1 <= qnum <= OFFICIAL_COUNT):
            continue
        # Keep the longest snippet for each question number.
        prev = by_num.get(qnum, "")
        if len(text) > len(prev):
            by_num[qnum] = text
    return by_num


def _load_bank_questions() -> list[dict]:
    payload = json.loads(_BANK_PATH.read_text(encoding="utf-8"))
    return payload["questions"]


def get_official_questions() -> list[dict]:
    from exam2016_curated import build_exam2016_curated

    return build_exam2016_curated()

