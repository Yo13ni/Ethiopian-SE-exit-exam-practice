import json
import glob
import re
from collections import Counter, defaultdict

exam_files = glob.glob("data/exams/*/questions.json")
arch_keywords = re.compile(
    r"architect|ATAM|SOLID|design pattern|coupling|cohesion|4\+1|Kruchten|"
    r"layered|client.?server|pipe.?filter|MVC|broker|peer.?to.?peer|"
    r"quality attribute|modifiability|availability|utility tree|"
    r"factory method|singleton|adapter|observer|facade|decorator|"
    r"component.?and.?connector|module structure|allocation|"
    r"reference model|architectural style|architectural pattern|"
    r"Liskov|separation of concern|information hiding|"
    r"views and beyond|tradeoff|sensitivity point|"
    r"creational|structural pattern|behavioral pattern|"
    r"open.?closed|single responsibility|dependency inversion|"
    r"interface segregation|proxy pattern|flyweight|composite|"
    r"strategy pattern|state pattern|command pattern|mediator|"
    r"memento|template method|chain of responsibility|iterator|"
    r"abstract factory|builder pattern|prototype pattern|"
    r"pipe and filter|n.?tier|three tier|microservice|"
    r"deployment view|logical view|process view|physical view|"
    r"scenario view|development view|black box|"
    r"architecture business cycle|ABC|ATAM|"
    r"performance tactic|modifiability tactic|security tactic",
    re.I,
)

results = []
topic_counts = Counter()
concept_counts = Counter()
text_patterns = Counter()
theme_counts = Counter()
by_exam = defaultdict(list)

THEME_RULES = [
    ("Quality Attributes", r"quality attribute|availability|modifiability|performance|security|testability|usability|interoperability|scalability|MTBF|MTTR|tactic"),
    ("Architectural Styles", r"layered|client.?server|pipe.?filter|MVC|broker|peer.?to.?peer|n.?tier|three tier|microservice|architectural style|architectural pattern"),
    ("Architecture Definition & Structures", r"software architecture|module structure|component.?and.?connector|allocation|4\+1|Kruchten|logical view|process view|development view|physical view|scenario|reference model|reference architecture|black box|architecture business"),
    ("Design Patterns", r"design pattern|factory|singleton|adapter|observer|facade|decorator|proxy|flyweight|composite|strategy|state|command|mediator|memento|template method|chain of responsibility|iterator|creational|structural|behavioral|abstract factory|builder|prototype|GoF|gang of four"),
    ("SOLID & Design Principles", r"SOLID|single responsibility|open.?closed|Liskov|interface segregation|dependency inversion|coupling|cohesion|separation of concern|information hiding|modularity|abstraction"),
    ("ATAM & Documentation", r"ATAM|utility tree|tradeoff|sensitivity|architecture documentation|views and beyond|Kruchten.*7|architecture review"),
    ("Coupling & Cohesion", r"coupling|cohesion|stamp coupling|content coupling|functional cohesion|coincidental"),
]


def classify_theme(text, concept, topic):
    blob = f"{text} {concept} {topic}".lower()
    themes = []
    for name, pat in THEME_RULES:
        if re.search(pat, blob, re.I):
            themes.append(name)
    return themes or ["Other Architecture"]


for path in sorted(exam_files):
    exam_id = path.replace("\\", "/").split("/")[2]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for q in data.get("questions", []):
        topic = q.get("topic", "")
        text = q.get("text", "")
        concept = q.get("concept", "")
        is_arch_topic = topic.lower() in (
            "software architecture",
            "architecture",
            "software design",
        )
        is_arch_text = bool(arch_keywords.search(text + " " + concept + " " + topic))
        if is_arch_topic or is_arch_text:
            themes = classify_theme(text, concept, topic)
            entry = {
                "exam": exam_id,
                "id": q.get("id"),
                "examNumber": q.get("examNumber"),
                "topic": topic,
                "text": text,
                "answer": q.get("answer"),
                "concept": concept,
                "themes": themes,
                "options": [o.get("text", "") for o in q.get("options", [])],
            }
            results.append(entry)
            topic_counts[topic] += 1
            concept_counts[concept or "none"] += 1
            for th in themes:
                theme_counts[th] += 1
            by_exam[exam_id].append(entry)
            tl = text.lower()
            if re.search(r"\bnot\b|\bexcept\b|\bincorrect\b|\bfalse\b", tl):
                text_patterns["negation (NOT/EXCEPT/FALSE)"] += 1
            elif re.search(r"\bbest\b|\bmost\b|\bprimary\b|\bmain\b", tl):
                text_patterns["best/most/primary"] += 1
            elif re.search(r"\badvantage\b|\bbenefit\b|\bdrawback\b|\bdisadvantage\b|\blimitation\b", tl):
                text_patterns["pros/cons/limitations"] += 1
            elif re.search(r"\bexample\b|\bscenario\b|\binstance\b", tl):
                text_patterns["example/scenario"] += 1
            elif re.search(r"\bmatch\b|\bpair\b|\bassociate\b|\bcorrespond\b", tl):
                text_patterns["matching/pairing"] += 1
            elif re.search(r"\bstep\b|\bphase\b|\border\b|\bsequence\b", tl):
                text_patterns["steps/sequence/order"] += 1
            else:
                text_patterns["definition/identification"] += 1

print("=" * 60)
print(f"TOTAL ARCHITECTURE-RELATED QUESTIONS: {len(results)}")
print("=" * 60)
print("\nBY EXAM:")
for e, qs in sorted(by_exam.items(), key=lambda x: -len(x[1])):
    print(f"  {e:12} {len(qs):3} questions")

print("\nBY TOPIC LABEL:")
for t, c in topic_counts.most_common():
    print(f"  {t}: {c}")

print("\nBY THEME (question may count in multiple themes):")
for th, c in theme_counts.most_common():
    print(f"  {th}: {c}")

print("\nQUESTION PATTERNS:")
for p, c in text_patterns.most_common():
    pct = 100 * c / len(results) if results else 0
    print(f"  {p}: {c} ({pct:.0f}%)")

print("\nTOP CONCEPTS (by frequency):")
for c, n in concept_counts.most_common(50):
    if c != "none":
        print(f"  [{n:2}] {c}")

print("\n" + "=" * 60)
print("ALL QUESTIONS BY EXAM")
print("=" * 60)
for exam_id in sorted(by_exam.keys()):
    print(f"\n--- {exam_id.upper()} ({len(by_exam[exam_id])} questions) ---")
    for q in by_exam[exam_id]:
        themes = ", ".join(q["themes"])
        print(f"  Q{q.get('examNumber', q['id'])} [{themes}]")
        print(f"    {q['text'][:120]}{'...' if len(q['text'])>120 else ''}")
        print(f"    ANS: {q['answer']} | {q['concept'][:80]}")

# Write JSON for reference
with open("data/arch_questions_analysis.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "total": len(results),
            "by_exam": {k: len(v) for k, v in by_exam.items()},
            "themes": dict(theme_counts),
            "patterns": dict(text_patterns),
            "questions": results,
        },
        f,
        indent=2,
        ensure_ascii=False,
    )
print("\nSaved: data/arch_questions_analysis.json")
