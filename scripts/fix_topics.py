"""Re-classify and correct question topics across exam banks."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters: more specific patterns first
TOPIC_RULES = [
    ("Software Architecture", r"software architecture|quality scenario|ATAM|architecture description|layered architecture|coupling|cohesion|microservice|API gateway|stakeholder communication.*architecture"),
    ("Software Testing", r"software test|tester|test process|coverage|traceability|defect|configuration management|test planning|test analysis|integration test"),
    ("Database", r"SQL|relation schema|functional dependency|foreign key|normal form|normalization|entity|attribute|tuple|INSERT|database|ER diagram|cardinality|DORM|HOTEL|schema R|\bjoin\b"),
    ("Android", r"android|activity|intent|APK|manifest|ViewGroup|layout|service|content provider|onCreate|stopService|Dalvik"),
    ("Java / OOP", r"(?<![a-z/])java(?![a-z/])|interface|abstract class|constructor|inheritance|polymorphism|UML|try.?catch|garbage collection|Payable|Invoice|Student class|OOP|object.?oriented"),
    ("Web Development", r"CSS|HTML|JavaScript|javascript|PHP|HTTP request|DOM|GET method|POST method|cookie|substring|web page|web application|\bform\b|<form|HTML form|web form|React|Redux|Axios"),
    ("Networking", r"OSI|TCP|UDP|subnet|firewall|router|switch|hub|collision|IPv4|IPv6|HTTP|SMTP|DNS|cross.?over|ACL|OAuth|SSH|SSL|DES|packet|frame|segment|ICMP|CORS|REST|WAN|LAN|Ethernet|CDN|Content Delivery"),
    ("Security", r"confidentiality|integrity|authorization|authentication|cyber security|economy of mechanism|least privilege|risk retention|risk transfer|virus|worm|intrusion|encryption|digital signature|malware|Saltzer|\bthreat\b|biometric|palm scan|fingerprint scan|iris scan|unauthorized disclosure"),
    ("Project Management", r"project|agile|waterfall|spiral|incremental|Tuckman|ROI|stakeholder|WBS|resource level|critical path|communication management|scrum|milestone"),
    ("AI / ML", r"machine learning|supervised|unsupervised|reinforcement|data mining|search algorithm|A\*|heuristic|BFS|DFS|UCS|Dijkstra|intelligent agent|association rule|neural|CRISP|informed search|uninformed search|Artificial Intelligence|overfit|preprocessing|knowledge representation|ensemble|local search"),
    ("Operating Systems", r"operating system|process state|deadlock|banker|memory management|page replacement|scheduling|blocked|ready|FIFO|LIFO|fork|thread|swapping|paging"),
    ("C++", r"C\+\+|#include|iostream|cout|for loop|identifier|void solve|linking|compiling program"),
    ("Data Structures", r"time complexity|O\(|binary search|selection sort|linked.?list|tree|stack|queue|non.?linear|swap|data structure|sort algorithm"),
    ("Software Engineering", r"requirement|SRS|maintenance|evolution|SDLC|software model|design principle|UML element|software development"),
]

# Verified fixes for questions wrongly tagged as Web Development (form substring bug).
TOPIC_CORRECTIONS: dict[tuple[str, int], str] = {
    ("2015", 10): "Project Management",
    ("2015", 23): "Security",
    ("2015", 27): "AI / ML",
    ("2015", 44): "AI / ML",
    ("2015", 46): "AI / ML",
    ("2015", 84): "AI / ML",
    ("2015", 88): "AI / ML",
    ("2015", 92): "Security",
    ("2016", 76): "AI / ML",
    ("2017", 17): "Networking",
    ("2017", 66): "Database",
    ("aau", 4): "Data Structures",
    ("aau", 17): "Project Management",
    ("aau", 68): "AI / ML",
    ("aau", 73): "AI / ML",
    ("aau", 76): "AI / ML",
    ("aau", 100): "AI / ML",
    ("bdu", 35): "Database",
    ("bdu", 42): "Security",
    ("bdu", 57): "Software Architecture",
    ("bdu", 59): "Security",
    ("bdu", 61): "AI / ML",
    ("bdu", 91): "AI / ML",
    ("model1", 23): "AI / ML",
    ("model1", 24): "Software Testing",
    ("model1", 29): "AI / ML",
    ("model1", 48): "Security",
    ("model1", 67): "Android",
    ("model1", 78): "Software Architecture",
    ("model1", 79): "AI / ML",
    ("model1", 82): "Software Architecture",
    ("model1", 91): "AI / ML",
}

EXAM_PATHS = [
    "data/exams/2015/questions.json",
    "data/exams/2016/questions.json",
    "data/exams/2017/questions.json",
    "data/exams/aau/questions.json",
    "data/exams/bdu/questions.json",
    "data/exams/model1/questions.json",
]


def classify(text: str) -> str:
    for topic, pat in TOPIC_RULES:
        if re.search(pat, text, re.I):
            return topic
    return "General"


def question_blob(q: dict) -> str:
    return q["text"] + " " + " ".join(o["text"] for o in q["options"])


def update_concept_topic(concept: str, old_topic: str, new_topic: str) -> str:
    if not concept or old_topic == new_topic:
        return concept
    updated = concept.replace(f"Key idea ({old_topic}):", f"Key idea ({new_topic}):")
    updated = updated.replace(f"({old_topic})", f"({new_topic})", 1)
    return updated


def apply_corrections(exam_id: str, path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for q in data["questions"]:
        exam_num = q.get("examNumber", q.get("id"))
        key = (exam_id, exam_num)
        new_topic = TOPIC_CORRECTIONS.get(key)
        if not new_topic:
            continue
        old_topic = q.get("topic", "General")
        if old_topic == new_topic:
            continue
        q["topic"] = new_topic
        if q.get("concept"):
            q["concept"] = update_concept_topic(q["concept"], old_topic, new_topic)
        changed += 1
    if changed:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return changed


def reclassify_exam(path: Path) -> int:
    """Re-run keyword classify (used for exams built from fix_topics rules)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for q in data["questions"]:
        new_topic = classify(question_blob(q))
        if q.get("topic") != new_topic:
            old_topic = q.get("topic", "General")
            q["topic"] = new_topic
            if q.get("concept"):
                q["concept"] = update_concept_topic(q["concept"], old_topic, new_topic)
            changed += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return changed


def main() -> None:
    total = 0
    for rel in EXAM_PATHS:
        exam_id = Path(rel).parent.name
        path = ROOT / rel
        if not path.exists():
            continue
        n = apply_corrections(exam_id, path)
        total += n
        print(f"{rel}: corrected {n} topics")
    print(f"Total corrections: {total}")


if __name__ == "__main__":
    main()
