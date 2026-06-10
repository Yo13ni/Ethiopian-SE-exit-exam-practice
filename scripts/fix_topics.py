"""Re-classify question topics for 2015 and AAU exams."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters: more specific patterns first
TOPIC_RULES = [
    ("Software Architecture", r"software architecture|quality scenario|ATAM|architecture description|layered architecture|coupling|cohesion|microservice|API gateway|stakeholder communication.*architecture"),
    ("Software Testing", r"software test|tester|test process|coverage|traceability|defect|configuration management|test planning|test analysis"),
    ("Database", r"SQL|relation schema|functional dependency|foreign key|normal form|normalization|entity|attribute|tuple|INSERT|database|ER diagram|cardinality|DORM|HOTEL|schema R"),
    ("Android", r"android|activity|intent|APK|manifest|ViewGroup|layout|service|content provider|onCreate|stopService"),
    ("Java / OOP", r"(?<![a-z/])java(?![a-z/])|interface|abstract class|constructor|inheritance|polymorphism|UML|try.?catch|garbage collection|Payable|Invoice|Student class|OOP|object.?oriented"),
    ("Web Development", r"CSS|HTML|JavaScript|javascript|PHP|HTTP request|DOM|GET method|POST method|cookie|substring|web page|form"),
    ("Networking", r"OSI|TCP|UDP|subnet|firewall|router|switch|hub|collision|IPv4|IPv6|HTTP|SMTP|DNS|cross.?over|ACL|OAuth|SSH|SSL|DES|packet|frame|segment|ICMP|CORS|REST|WAN|LAN|Ethernet"),
    ("Security", r"confidentiality|integrity|authorization|authentication|cyber security|economy of mechanism|least privilege|risk retention|risk transfer|virus|worm|intrusion|encryption|digital signature|malware|Saltzer"),
    ("Project Management", r"project|agile|waterfall|spiral|incremental|Tuckman|ROI|stakeholder|WBS|resource level|critical path|communication management|scrum|milestone"),
    ("AI / ML", r"machine learning|supervised|unsupervised|reinforcement|data mining|search algorithm|A\*|heuristic|BFS|DFS|UCS|Dijkstra|intelligent agent|association rule|neural|CRISP"),
    ("Operating Systems", r"operating system|process state|deadlock|banker|memory management|page replacement|scheduling|blocked|ready|FIFO|LIFO|fork|thread|swapping|paging"),
    ("C++", r"C\+\+|#include|iostream|cout|for loop|identifier|void solve|linking|compiling program"),
    ("Data Structures", r"time complexity|O\(|binary search|selection sort|linked.?list|tree|stack|queue|non.?linear|swap|data structure|sort algorithm"),
    ("Software Engineering", r"requirement|SRS|maintenance|evolution|SDLC|software model|design principle|UML element|software development"),
]


def classify(text: str) -> str:
    for topic, pat in TOPIC_RULES:
        if re.search(pat, text, re.I):
            return topic
    return "General"


def fix_exam(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for q in data["questions"]:
        blob = q["text"] + " " + " ".join(o["text"] for o in q["options"])
        new_topic = classify(blob)
        if q.get("topic") != new_topic:
            q["topic"] = new_topic
            changed += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return changed


def main():
    for rel in [
        "data/exams/2015/questions.json",
        "data/exams/aau/questions.json",
        "data/exams/bdu/questions.json",
    ]:
        p = ROOT / rel
        if p.exists():
            n = fix_exam(p)
            print(f"{rel}: updated {n} topics")


if __name__ == "__main__":
    main()
