import json
import glob
import re
from collections import Counter, defaultdict

files = glob.glob("data/exams/*/questions.json")

STRICT_TOPIC = {"Software Architecture", "Architecture", "Software Design"}
STRONG = re.compile(
    r"software architect|architectural (style|pattern|quality|decision|notation|structure|view|erosion)|"
    r"4\+1|Kruchten|ATAM|utility tree|reference model|reference architecture|"
    r"component.and.connector|module structure|allocation structure|"
    r"layered architect|MVC|model.view.controller|pipe.and.filter|microservice|"
    r"event.driven architect|API gateway|design pattern|GoF|creational|behavioral pattern|structural pattern|"
    r"factory method|abstract factory|singleton|adapter pattern|observer pattern|"
    r"facade|decorator|proxy pattern|flyweight|bridge pattern|builder pattern|"
    r"memento|mediator|strategy pattern|state pattern|command pattern|"
    r"SOLID|single responsibility|open/closed|Liskov|interface segregation|dependency inversion|"
    r"quality attribute|quality scenario|modifiability|architectural notation|"
    r"coupling.*cohesion|cohesion.*coupling|stamp coupling|content coupling|"
    r"architecture documentation|views and beyond|tradeoff point|sensitivity point|"
    r"client.server (architect|style)|peer.to.peer|horizontal scaling",
    re.I,
)
WEAK_EXCLUDE = re.compile(
    r"OSI (model|layer|reference)|packet data unit|spiral model|RUP|4GT|"
    r"regression test|boundary value|equivalence partition|black box test|"
    r"work breakdown|WBS|DFD|reverse engineering|android architecture layer|"
    r"linux kernel|denial of service|ACL|functional organization structure|"
    r"data mining|requirement engineering.*first step|mediator . memento.*editor",
    re.I,
)

THEMES = [
    ("Arch Definition & Importance", r"software architect|role of.*architect|why.*architect|goal.*architect|assess.*architect|evaluate.*architect|architectural decision|architectural notation|document.*architect|purpose.*document|understood by other design experts"),
    ("Quality Attributes", r"quality attribute|quality scenario|maintainability|modifiability|performance|scalability|availability|robustness|security.*architect|modifi|localize critical"),
    ("Architectural Styles", r"layered|MVC|model.view.controller|client.server|microservice|pipe|filter|broker|peer|event.driven|architectural style|API gateway|horizontal scaling|servic|web.based|odd"),
    ("Architecture Structures & Views", r"module structure|component.and.connector|allocation|4\+1|logical view|process view|development view|physical view|reference model|reference architecture|context view|class diagram.*struct|UML diagram.*structure"),
    ("Design Patterns", r"design pattern|factory|singleton|adapter|observer|facade|decorator|proxy|flyweight|bridge|builder|memento|mediator|strategy|state|command|chain|iterator|prototype|template method|visitor|creational|behavioral|structural|GoF|restore.*state|complex object|abstraction from.*implementation"),
    ("SOLID & Design Quality", r"SOLID|single responsibility|open/closed|open for extension|Liskov|interface segregation|dependency inversion|coupling|cohesion|information hiding|separation of concern|fine.grain|producer.*consumer|self.contained components"),
    ("ATAM & Tradeoffs", r"ATAM|utility tree|tradeoff|sensitivity|risk theme"),
    ("Layered Architecture Rules", r"layer.*call|architectural erosion|ordering relation"),
]


def themes_for(entry):
    blob = (entry["text"] + " " + entry["concept"]).lower()
    found = [name for name, pat in THEMES if re.search(pat, blob, re.I)]
    return found or ["General"]


strict = []
for path in sorted(files):
    exam = path.replace("\\", "/").split("/")[2]
    data = json.load(open(path, encoding="utf-8"))
    for q in data["questions"]:
        topic = q.get("topic", "")
        text = q.get("text", "")
        concept = q.get("concept", "")
        blob = text + " " + concept
        if topic in STRICT_TOPIC:
            include = True
        elif STRONG.search(blob) and not WEAK_EXCLUDE.search(blob):
            include = True
        else:
            include = False
        if include:
            strict.append(
                {
                    "exam": exam,
                    "id": q.get("id"),
                    "n": q.get("examNumber"),
                    "topic": topic,
                    "text": text,
                    "ans": q.get("answer"),
                    "concept": concept,
                    "opts": [o["text"] for o in q.get("options", [])],
                }
            )

themes = Counter()
patterns = Counter()
by_exam = Counter()
concept_freq = Counter()
theme_questions = defaultdict(list)

for e in strict:
    by_exam[e["exam"]] += 1
    concept_freq[e["concept"]] += 1
    th_list = themes_for(e)
    for t in th_list:
        themes[t] += 1
        theme_questions[t].append(e)
    tl = e["text"].lower()
    if re.search(r"\bnot\b|\bexcept\b|does not|is not|odd one|incorrect|that is not", tl):
        patterns["NOT / EXCEPT / odd-one-out"] += 1
    elif re.search(r"best|most suitable|most appropriate|most likely|primary|critical feature", tl):
        patterns["BEST / MOST suitable"] += 1
    elif re.search(r"role of|purpose of|why is|goal", tl):
        patterns["Role / Purpose / Why"] += 1
    elif re.search(r"given the following|scenario", tl):
        patterns["Scenario / Given diagram"] += 1
    elif re.search(r"which of the following|what is|identify|select|define", tl):
        patterns["Definition / Which-one"] += 1
    else:
        patterns["Other"] += 1

print("STRICT ARCHITECTURE QUESTIONS:", len(strict))
print("\nBY EXAM:", dict(sorted(by_exam.items(), key=lambda x: -x[1])))
print("\nTHEMES (multi-tag):")
for t, c in themes.most_common():
    print(f"  {c:2}  {t}")
print("\nQUESTION PATTERNS:")
for p, c in patterns.most_common():
    print(f"  {c:2}  {p}  ({100*c/len(strict):.0f}%)")

print("\n" + "=" * 70)
print("QUESTIONS BY THEME")
print("=" * 70)
for theme in [t for t, _ in themes.most_common()]:
    qs = theme_questions[theme]
    print(f"\n## {theme} ({len(qs)})")
    seen = set()
    for e in qs:
        key = e["text"][:80]
        if key in seen:
            continue
        seen.add(key)
        print(f"  [{e['exam']}] Q{e['n']}: {e['text'][:90]}...")
        print(f"    -> {e['ans']} | {e['concept'][:65]}")

# Priority study list
print("\n" + "=" * 70)
print("PRIORITY CONCEPT LIST (sorted by exam frequency)")
print("=" * 70)
priority = [
    ("Quality Attributes & Evaluation", themes["Quality Attributes"] + themes["Arch Definition & Importance"], [
        "Architectural quality attributes as evaluation parameter",
        "Quality scenarios for qualitative analysis",
        "Maintainability / modifiability tactics (fine-grain, producer-consumer separation)",
        "Performance tactics (localize critical operations)",
        "Scalability (horizontal scaling, independent services)",
        "Robustness vs availability",
        "Trade-offs: improving one QA may hurt another",
    ]),
    ("Architectural Styles", themes["Architectural Styles"], [
        "Layered architecture (adjacent layers, erosion rules)",
        "Client-Server (web apps, centralized)",
        "Microservices (large-scale, independent scalable components)",
        "Event-Driven Architecture (responsiveness, real-time)",
        "MVC (Model stores state, View displays, Controller handles input)",
        "Pipe-and-Filter, Broker, P2P — know definitions & when to use",
        "API Gateway (hides microservice boundaries from clients)",
        "Identify what IS vs IS NOT an architectural style (UML is NOT a style)",
    ]),
    ("Architecture Structures & Views", themes["Architecture Structures & Views"], [
        "Module, Component-Connector, Allocation structures",
        "Kruchten 4+1 views (Logical, Process, Development, Physical + Scenarios)",
        "Reference model vs reference architecture",
        "UML Class diagram for system structure",
        "Architecture documentation purposes (NOT: trace source code flow)",
    ]),
    ("Design Patterns", themes["Design Patterns"], [
        "Memento (restore previous object state)",
        "Builder (complex object, algorithm independent of parts)",
        "Bridge (separate abstraction from implementation)",
        "Pattern categories: Creational, Structural, Behavioral",
        "Match pattern to problem description (scenario-based)",
    ]),
    ("SOLID & Design Principles", themes["SOLID & Design Quality"], [
        "Open/Closed Principle (open for extension, closed for modification)",
        "High coupling as architectural problem indicator",
        "Coupling/cohesion scales (if tested)",
        "Information hiding, separation of concerns",
    ]),
    ("Layered Architecture Scenarios", themes["Layered Architecture Rules"], [
        "Which layer can call which (no skip violations / erosion)",
        "Layer ordering MCQ with diagrams",
    ]),
    ("ATAM", themes["ATAM & Tradeoffs"], [
        "9 steps, 3 phases, utility tree, sensitivity vs tradeoff points",
    ]),
]

for name, count, items in priority:
    print(f"\n### {name} (~{count} exam hits)")
    for item in items:
        print(f"  - {item}")

with open("data/arch_questions_strict.json", "w", encoding="utf-8") as f:
    json.dump({"total": len(strict), "themes": dict(themes), "patterns": dict(patterns), "questions": strict}, f, indent=2, ensure_ascii=False)
