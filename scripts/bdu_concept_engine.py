"""Concept-based per-option explanations — no generic distractor templates."""

from __future__ import annotations

import re
from typing import Any

# What each term/concept MEANS (used to explain wrong options by contrast)
GLOSSARY: dict[str, str] = {
    "stack": "a LIFO structure used for recursion, undo operations, and DFS",
    "queue": "a FIFO structure used for BFS, job scheduling, and buffering",
    "tree": "a hierarchical structure with parent-child nodes and one root",
    "graph": "nodes with arbitrary connections, may contain cycles",
    "circular linked list": "a linear list whose last node points back to the first",
    "singly linked list": "nodes linked forward only; last node points to NULL",
    "doubly linked list": "nodes with next and prev pointers",
    "binary search": "search on sorted data by halving the range — O(log n)",
    "big-oh": "upper bound on worst-case growth rate",
    "theta": "tight bound — both upper and lower",
    "omega": "lower bound — best-case growth",
    "reference parameter": "alias to original variable — changes inside function affect caller",
    "pass by value": "copy of argument — caller variable unchanged after function",
    "new": "C++ operator that allocates memory on the heap",
    "delete": "C++ operator that frees heap memory allocated by new",
    "intent": "Android message object for navigation and passing data between components",
    "manifest": "AndroidManifest.xml — declares app components, permissions, and metadata",
    "wbs": "Work Breakdown Structure — decomposes project into work packages",
    "scalability": "ability to handle growing load (users, queries, data)",
    "vulnerability": "weakness in safeguards that can be exploited",
    "threat": "potential danger to information or systems",
    "dirty read": "reading uncommitted data from another transaction",
    "deferred modification": "database changes written only after transaction commits",
    "api gateway": "single entry point that hides internal microservice boundaries",
    "quality scenario": "stimulus–response pair used in ATAM architecture evaluation",
    "reference model": "abstract elements and relationships for a domain (e.g. OSI)",
    "data mining": "discovering patterns and predicting trends from large datasets",
    "supervised learning": "learning from labeled training examples",
    "informed search": "search using heuristics to explore promising paths first",
    "black box testing": "testing without seeing internal code — based on inputs/outputs",
    "white box testing": "testing based on internal code structure and paths",
    "equivalence partitioning": "black-box technique dividing inputs into equivalent classes",
    "boundary value analysis": "black-box technique testing edges of input partitions",
    "ipv6": "128-bit IP addresses",
    "multiplexing": "transmitting multiple signals simultaneously on one medium",
    "biometric authentication": "identity verification using fingerprint, iris, or palm scan",
    "sql injection": "attack inserting malicious SQL through unescaped user input",
    "xss": "Cross-Site Scripting — injecting scripts via unsanitized user input",
    "mvc model": "stores program state and business logic in Model-View-Controller",
    "pthread_exit": "terminates the calling thread, optionally returning a void* value",
    "hypertext": "clickable text linking to other documents or locations",
    "web server": "program accepting HTTP requests and returning HTTP responses",
    "reset": "HTML form button that clears all fields to default values",
    "onClick": "Android/UI handler invoked when user clicks a button",
    "linux kernel": "Android is built on the Linux kernel",
    "rapid application development": "RAD — iterative prototyping with fast user feedback",
    "pert": "Program Evaluation and Review Technique for project scheduling",
    "agile manifesto": "values individuals, working software, customer collaboration, responding to change",
    "nosql": "databases for unstructured/semi-structured data at scale",
    "use case diagram": "UML behavioral diagram — NOT a structural diagram",
    "class diagram": "UML structural diagram showing classes and relationships",
    "coupling": "degree of dependency between software modules",
    "layered architecture": "separation into layers (presentation, business, data) for modifiability",
    "overloading": "same method name, different parameters — compile-time polymorphism",
    "runtime polymorphism": "dynamic dispatch via virtual functions and overriding",
    "constructor": "special method initializing an object — no return type, same name as class",
    "interface": "Java contract of abstract methods — implemented by classes",
    "abstract class": "class that may have abstract methods — can have state and constructors",
    "inheritance": "subclass inherits fields and methods from superclass",
    "normalization": "organizing relations to reduce redundancy using FDs and keys",
    "functional dependency": "α → β: same α values force same β values in all legal relations",
    "primary key": "unique identifier for each tuple in a relation",
    "foreign key": "attribute referencing primary key of another relation",
    "corrective maintenance": "fixes faults/defects discovered after deployment",
    "adaptive maintenance": "adapts software to environmental changes (OS, regulations)",
    "perfective maintenance": "improves performance or maintainability without fixing a specific fault",
    "integration testing": "tests interactions between combined modules after unit tests",
    "flow control": "TCP/windowing mechanism preventing sender from overwhelming receiver",
    "exokernel": "minimal kernel exposing hardware resources; apps manage policy",
    "fragment": "reusable Android UI component hosted inside an Activity",
    "fragments": "reusable Android UI components hosted inside an Activity",
    "activity": "Android screen component with lifecycle callbacks (onCreate, onPause, etc.)",
    "activities": "Android screen components — one focused user task per Activity",
    "broadcast receiver": "Android component that listens for system-wide broadcast Intents",
    "broadcast receivers": "Android components that respond to broadcast Intents (e.g., battery low)",
    "content provider": "Android component that shares structured app data with other apps",
    "content providers": "Android components exposing data via a content URI for cross-app access",
    "application layer": "OSI layer 7 — network transparency, resource allocation, user services (HTTP, DNS)",
    "transport layer": "OSI layer 4 — end-to-end delivery, segmentation, flow and error control",
    "network layer": "OSI layer 3 — routing and logical addressing (IP)",
    "data link layer": "OSI layer 2 — framing, MAC addressing, hop-to-hop delivery",
    "breakpoint": "debugger marker that pauses program execution at a chosen line",
    "package manager": "tool that installs, updates, and tracks software packages and dependencies",
    "package managers": "tools (apt, npm, pip) that install software and resolve dependency versions",
    "frame": "Java AWT/Swing top-level window with title bar and border decorations",
    "risk transference": "shifts risk impact to a third party (insurance, outsourcing)",
    "risk mitigation": "reduces probability or impact of a risk through controls",
    "risk acceptance": "acknowledges the risk and budgets for potential loss",
    "risk avoidance": "eliminates the activity or threat source causing the risk",
    "sha-256": "cryptographic hash for integrity — one-way digest, not encryption for data at rest",
    "rsa": "asymmetric encryption for key exchange and signatures — not bulk database storage encryption",
    "hashing algorithm": "one-way digest verifying integrity — different from symmetric encryption like AES",
    "regression": "supervised learning predicting continuous values — not sequential time-series forecasting",
    "clustering": "unsupervised grouping of unlabeled data — not demand forecasting over time",
    "classification": "supervised learning with discrete class labels — different from time-series forecasting",
    "function points": "software size metric for estimation — not a maintenance type",
    "system testing": "validates the complete integrated system — broader than module-to-module interaction",
    "unit testing": "tests individual modules in isolation — before combining modules",
    "user acceptance testing": "end-user validation of fitness for purpose — after system/integration tests",
    "flow control": "TCP windowing that prevents a fast sender from overwhelming the receiver",
    "access method": "how devices share a medium (CSMA/CD, token) — not TCP receive-window throttling",
    "requirements analysis": "first SDLC step — gather and analyze needs before design or coding",
    "websocket": "application protocol enabling full-duplex real-time client-server communication",
    "merge sort": "divide-and-conquer sorting algorithm splitting arrays recursively",
    "regression testing": "re-runs existing tests to ensure new changes did not break prior functionality",
    "supervised learning": "learning from labeled training examples",
    "unsupervised learning": "finding patterns in unlabeled data",
    "classification": "supervised learning predicting discrete class labels",
    "aes": "Advanced Encryption Standard — symmetric encryption for data at rest",
    "builder pattern": "constructs complex objects step by step, separating construction from representation",
    "mutual exclusion": "only one process may use a non-sharable resource at a time",
    "hold and wait": "process holds resources while waiting to acquire more — deadlock condition",
    "fcfs": "First-Come First-Served scheduling in arrival order",
    "innerhtml": "DOM property to read/write HTML inside an element",
    "pki": "Public Key Infrastructure — certificate-based identity and key management",
    "stateful inspection": "firewall tracking connection state for legitimate session packets",
    "event-driven architecture": "components react to events asynchronously for responsiveness",
    "refactoring": "improves internal code structure without changing external behavior",
    "deadlock": "circular wait where processes hold resources others need",
    "process": "program in execution with its own address space",
    "thread": "lightweight unit of execution within a process",
    "deadlock": "circular wait preventing progress",
    "fifo": "First In First Out — queue discipline",
    "lifo": "Last In First Out — stack discipline",
    "tcp": "reliable, connection-oriented transport protocol",
    "udp": "unreliable, connectionless transport protocol",
    "dns": "Domain Name System — resolves names to IP addresses",
    "http": "Hypertext Transfer Protocol — request/response web protocol",
    "css": "Cascading Style Sheets — controls visual presentation of HTML",
    "javascript": "client-side scripting language for web interactivity",
    "php": "server-side scripting language — runs on server, not in browser",
}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def _glossary_lookup(text: str) -> str | None:
    t = _norm(text)
    if t in GLOSSARY:
        return GLOSSARY[t]
    for term, definition in sorted(GLOSSARY.items(), key=lambda x: -len(x[0])):
        if t == term:
            return definition
    for term, definition in sorted(GLOSSARY.items(), key=lambda x: -len(x[0])):
        pattern = r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b"
        if re.search(pattern, t):
            return definition
    return None


def _stem_intent(stem: str) -> str:
    s = _norm(stem)
    if "worst" in s and ("notation" in s or "complexity" in s):
        return "identifying worst-case asymptotic notation"
    if "complexity order" in s or "time function" in s:
        return "finding the dominant term in a complexity expression"
    if "binary search" in s:
        return "the time complexity of binary search on sorted data"
    if "output" in s or "cout" in s or "print" in s:
        return "tracing code execution to determine printed output"
    if "reference" in s and ("parameter" in s or "&" in s):
        return "understanding pass-by-reference — changes affect the original variable"
    if "valid identifier" in s:
        return "C++ identifier rules — letters, digits, underscore; cannot start with digit; not a keyword"
    if "circular" in s or ("last node" in s and "first" in s):
        return "identifying a circular linked list (last → first)"
    if "recurs" in s:
        return "which structure implements recursive call activation"
    if "hierarch" in s:
        return "which structure models parent-child hierarchy"
    if "dynamically" in s and ("alloc" in s or "memory" in s or "c++" in s):
        return "which C++ operator performs dynamic heap allocation"
    if "css syntax" in s:
        return "valid CSS rule syntax: selector { property: value; }"
    if "web server" in s or ("http" in s and "request" in s):
        return "which component accepts HTTP requests and serves responses"
    if "bold" in s and "html" in s:
        return "which HTML tag renders bold text"
    if "form" in s and ("clear" in s or "reset" in s):
        return "which HTML input type clears form fields"
    if "transaction" in s and "commit" in s:
        return "when database writes occur relative to commit"
    if "lock" in s and "phase" in s:
        return "two-phase locking — growing vs shrinking phase"
    if "dirty read" in s or ("intermediate" in s and "transaction" in s):
        return "concurrency anomaly when reading uncommitted data"
    if "scalability" in s or "growing" in s and "quer" in s:
        return "which non-functional requirement handles growing load"
    if "threat" in s and len(s) < 30:
        return "definition of a security threat"
    if "vulnerabilit" in s or ("weakness" in s and "safeguard" in s):
        return "definition of a vulnerability"
    if "sql injection" in s:
        return "how to prevent SQL injection attacks"
    if "wbs" in s or "work package" in s:
        return "which document contains detailed work package descriptions"
    if "reference model" in s or ("elements" in s and "relationship" in s):
        return "abstract domain model vs concrete architecture"
    if "architecture" in s and "qualitative" in s:
        return "artifacts for qualitative architecture analysis (ATAM)"
    if "coupling" in s and ("quantitative" in s or "analyze" in s):
        return "quantitative architecture problem indicators"
    if "ipv6" in s and "bit" in s:
        return "bit length of IPv6 addresses"
    if "transport layer" in s:
        return "services provided by the OSI transport layer"
    if "encryption" in s and "layer" in s:
        return "which OSI layer handles encryption/decryption"
    if "denial of service" in s or "dos" in s:
        return "which security factor DoS attacks primarily affect"
    if "agile manifesto" in s:
        return "which statement contradicts the Agile Manifesto values"
    if "boundary value" in s:
        return "which testing technique boundary value analysis belongs to"
    if "equivalence partition" in s:
        return "properties of equivalence partitioning as a test technique"
    if "data mining" in s or ("predict" in s and "trend" in s):
        return "which technique predicts trends from data"
    if "informed search" in s or ("promising" in s and "explored" in s):
        return "search strategy using heuristics"
    if "nosql" in s or "not a nosql" in s:
        return "identifying which database is NOT NoSQL"
    if "structural diagram" in s:
        return "which UML diagram is NOT structural"
    if "pthread_exit" in s:
        return "correct POSIX thread exit function signature"
    if "test planning" in s:
        return "main task of the test planning phase"
    if "decision coverage" in s:
        return "formula for decision coverage percentage"
    if "manifest" in s and "android" in s:
        return "purpose of AndroidManifest.xml"
    if "onclick" in s or ("click" in s and "button" in s):
        return "which method handles button click events"
    if "layout" in s and ("xml" in s or "stored" in s or "directory" in s):
        return "where Android XML layout files are stored"
    if "inheritance" in s and "consequence" in s:
        return "consequences of class inheritance coupling"
    if "runtime polymorphism" in s or ("run time" in s and "polymorph" in s):
        return "what fully describes runtime (dynamic) polymorphism"
    if "constructor" in s and "incorrect" in s:
        return "which statement about Java constructors is FALSE"
    if "array" in s and "true" in s:
        return "true statements about arrays in C/Java"
    if "function calling" in s or "function call" in s:
        return "correct syntax for calling vs declaring a function"
    if "linked list" in s and "end" in s and "head" in s:
        return "complexity of appending to singly linked list with only head pointer"
    return "the specific concept tested in this question"


def _explain_code_output_wrong(stem: str, wrong: str, correct: str, key: str) -> str:
    s = _norm(stem)
    if "reference" in s or "&" in s:
        if wrong == "5" or wrong.strip() == "5":
            return (
                "5 is the original value of i before the function modifies it. "
                "You would get 5 only with pass-by-VALUE (no &). "
                "With a reference parameter (int &i), the function multiplies the actual variable in main: 5 × 5 = 25."
            )
        if wrong in ("10", "20"):
            return (
                f"{wrong} does not follow from multiplying i=5 by 5. "
                f"Reference assignment i = i * 5 changes the caller's variable to 25, not {wrong}."
            )
    if "continue" in s:
        return (
            f"Output {wrong} would require a different loop path. "
            "'continue' skips the rest of the current iteration — trace which iterations reach cout "
            f"to see why the actual output is {correct}, not {wrong}."
        )
    return (
        f"If the program printed {wrong}, a different branch or calculation would execute. "
        f"Trace the code line-by-line with the given inputs to verify the output is {correct}."
    )


def _explain_complexity_wrong(stem: str, wrong: str, correct: str) -> str:
    w = _norm(wrong)
    if "log" in w and "n log" not in w:
        return (
            f"{wrong} describes logarithmic growth — the slowest class among typical terms. "
            f"In this expression, higher-order terms like n² dominate, so the order is not logarithmic."
        )
    if re.search(r"n\s*\^?\s*2|n2|\(n2\)", w):
        return (
            f"{wrong} would be correct only if n² were absent or not dominant. "
            f"Compare growth rates: n² overtakes n and n log n for large n."
        )
    if re.search(r"n\s*log", w):
        return (
            f"{wrong} fits algorithms like merge sort. "
            f"When n² appears in the sum, quadratic growth dominates n log n."
        )
    if re.search(r"o\s*\(\s*n\s*\)", w) and "log" not in w:
        return (
            f"{wrong} means linear growth dominates. "
            f"Linear terms (n, 2n) exist here but are overshadowed by the n² term."
        )
    if "o(1)" in w.replace(" ", ""):
        return f"{wrong} means constant time — impossible when the expression contains n and n² terms."
    if "big" in w and "oh" in w:
        return (
            f"{wrong} is worst-case notation, but the question asks for the complexity ORDER of this specific sum — "
            f"compute the dominant term first, then express it in Big-O."
        )
    return f"{wrong} does not match the dominant growth rate of the given expression."


def _explain_definition_wrong(wrong: str, correct: str, topic: str, stem: str) -> str:
    w_def = _glossary_lookup(wrong)
    c_def = _glossary_lookup(correct)
    if w_def and c_def:
        return (
            f"'{wrong}' refers to {w_def}. "
            f"The question asks about {_stem_intent(stem)}. "
            f"That requires '{correct}' — {c_def}. "
            f"These are different concepts; do not confuse them on the exam."
        )
    if w_def:
        return (
            f"'{wrong}' means {w_def}. "
            f"That answers a different kind of question. "
            f"Here, the stem points to '{correct}' instead."
        )
    return (
        f"'{wrong}' is not the standard term for {_stem_intent(stem)}. "
        f"The curriculum answer is '{correct}'."
    )


def explain_wrong_option(q: dict, key: str, text: str) -> str:
    stem = q.get("text", "")
    correct = q["answer"]
    topic = q.get("topic", "General")
    opts = {o["key"]: o["text"] for o in q["options"]}
    correct_text = opts.get(correct, "")

    if "(option unclear" in text:
        return (
            "This option text was damaged during OCR and cannot be read clearly. "
            f"Focus on why '{correct_text}' is correct for {_stem_intent(stem)}."
        )

    s = _norm(stem)
    t = _norm(text)

    # SQL injection — per-option specifics
    if "sql injection" in s:
        if "merge" in t:
            return (
                "'Merge tables' combines table structures or data — it is a database design/query task. "
                "SQL injection is prevented by parameterized queries or escaping user input so malicious SQL "
                "cannot be injected through form fields. Merging tables does not sanitize input."
            )
        if "escape" in t or "parameter" in t:
            return (
                "'Escape queries' / parameterized queries bind user input as data, not executable SQL code. "
                "The database treats input as values, so injected commands like ' OR 1=1 -- cannot run."
            )
        if "interrupt" in t:
            return (
                "'Interrupt requests' relates to OS/process signals, not database security. "
                "SQL injection is a web/database attack where user input alters SQL queries — stopped by input escaping."
            )
        if t in ("all", "all of the above", "all of above"):
            return (
                "'All' is wrong because merging tables and interrupting requests do NOT prevent SQL injection. "
                "Only proper input handling (escaping/parameterization) does."
            )

    # DoS / availability
    if "denial of service" in s or "dos" in s:
        if "availability" in t:
            return "DoS floods resources so legitimate users cannot access the service — attacks availability." if key == correct else ""
        if "confidentiality" in t:
            return "DoS does not primarily steal secrets — it blocks access. Confidentiality = preventing unauthorized disclosure."
        if "integrity" in t:
            return "DoS may corrupt availability but its primary CIA target is availability, not data integrity modification."

    # Threat vs vulnerability
    if ("threat" in s and len(s) < 40) or t == "threat":
        if "potential" in t or "danger" in t:
            return "A threat is a potential danger — something that could cause harm." if key == correct else ""
        if "vulnerabilit" in t or "weakness" in t or "flaw" in t:
            return "Vulnerability is a weakness in the system. Threat is the potential danger itself — different security terms."
        if "illegal access" in t or "exploit" in t:
            return "That describes an attack or intrusion event, not the definition of 'threat' (potential danger)."

    # Agile manifesto incorrect statement
    if "agile manifesto" in s and "incorrect" in s:
        if "contract" in t and "collaboration" in t:
            return (
                "The Manifesto says 'Customer collaboration OVER contract negotiation' — this option reverses the priority, "
                "so it is the INCORRECT statement."
            ) if key == correct else ""
        if "respond to change" in t or "working software" in t:
            return "This aligns with the Agile Manifesto values — it is a correct statement, not the incorrect one asked."

    # "All of the above" wrong when not all options are true
    if t in ("all", "all of the above", "all of above", "all of the mentioned"):
        return (
            f"'All of the above' is only correct when EVERY other option is true. "
            f"Verify each choice A, B, C individually — if any is false, 'All' is wrong. "
            f"Here, '{correct_text}' is the specific correct answer."
        )

    # Code output
    if re.search(r"output|cout|print|following code", s, re.I):
        return _explain_code_output_wrong(stem, text, correct_text, key)

    # Complexity / Big-O
    if re.search(r"complexity|big.?oh|omega|theta|o\(|time function|asymptotic", s + " " + t):
        exp = _explain_complexity_wrong(stem, text, correct_text)
        if exp:
            return exp

    # C++ identifiers
    if "valid identifier" in s:
        if t == "int" or t == "class":
            return f"'{text}' is a reserved C++ keyword — keywords cannot be used as identifiers."
        if t.startswith("2") or re.match(r"^\d", t):
            return f"'{text}' starts with a digit — C++ identifiers cannot begin with a number."

    # Numeric wrong answers for reference/multiply questions
    if "reference" in s and text.strip().isdigit():
        return _explain_code_output_wrong(stem, text, correct_text, key)

    # Definition / which-is questions
    if re.search(r"which|what is|called|defines|true about|incorrect|false|not a|not related", s):
        exp = _explain_definition_wrong(text, correct_text, topic, stem)
        if exp:
            return exp

    # Contrast using glossary
    w_def = _glossary_lookup(text)
    c_def = _glossary_lookup(correct_text)
    intent = _stem_intent(stem)

    if w_def:
        return (
            f"'{text}' represents {w_def}. "
            f"This question tests {intent}. "
            f"That requires '{correct_text}'"
            + (f" ({c_def})" if c_def else "")
            + f", not '{text}'."
        )

    # Conceptual fallback — explain what the option means in plain terms
    return (
        f"'{text}' does not answer {intent}. "
        f"The question is in {topic} and the accepted answer is '{correct_text}'. "
        f"To see why '{text}' fails: ask yourself what concept '{text}' represents, "
        f"then check whether the question stem asks for that concept — here it does not."
    )


def explain_correct_option(q: dict, text: str) -> str:
    stem = q.get("text", "")
    topic = q.get("topic", "General")
    intent = _stem_intent(stem)
    c_def = _glossary_lookup(text)
    s = _norm(stem)

    if "reference" in s and text.strip().isdigit():
        return (
            f"'{text}' is the value printed after the reference parameter modifies the original variable. "
            f"With i=5 and i = i * 5 inside the function, main's i becomes {text}."
        )

    if re.search(r"complexity|o\(|big.?oh|time function", s + " " + _norm(text)):
        return (
            f"'{text}' matches the dominant growth rate of the expression. "
            f"Identify the fastest-growing term, drop constants, and express in Big-O notation."
        )

    parts = [f"'{text}' correctly answers {intent}."]
    if c_def:
        parts.append(f"Concept: {c_def}.")
    else:
        parts.append(f"In {topic}, this is the standard textbook answer for this scenario.")
    return " ".join(parts)


def build_overview(q: dict) -> str:
    stem = q.get("text", "")
    topic = q.get("topic", "General")
    answer = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    correct_text = opts.get(answer, "")
    intent = _stem_intent(stem)

    intro = f"**Concept ({topic}):** {intent}. "
    if re.search(r"2n|n\^2|complexity order|time function", stem, re.I):
        intro += (
            "Method: list terms → rank growth (log n < n < n log n < n²) → "
            "pick dominant term → drop constants → Big-O. "
        )
    intro += f"**Correct answer: {answer}** — {correct_text}. "
    intro += "Each option below explains the underlying concept and why it fits or fails."
    return intro
