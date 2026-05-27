"""Rich study-quality explanations for MoEE Model Exam 1 — tutor style, no boilerplate."""

from __future__ import annotations

import re
from typing import Any

# examNumber -> {overview, options: {A..D}, studyTip}
BANK: dict[int, dict[str, Any]] = {}


def _r(num: int, overview: str, options: dict[str, str], tip: str) -> None:
    BANK[num] = {"overview": overview, "options": options, "studyTip": tip}


def _build_bank() -> None:
    _r(
        1,
        "Operating systems use several schedulers, each at a different level.\n\n"
        "• Long-term scheduling (job scheduler) — decides which jobs are admitted into the system.\n"
        "• Medium-term scheduling — controls swapping processes between RAM and disk.\n"
        "• Short-term scheduling (CPU scheduler) — picks which ready process gets the processor next.\n"
        "• I/O scheduling — orders requests to storage devices.\n\n"
        "The question asks about the decision of which available process the processor will execute. "
        "That is the CPU dispatcher's job — it runs very frequently (milliseconds).\n\n"
        "✅ Answer: C — Short-term scheduling",
        {
            "A": "Long-term scheduling decides whether a new job enters the system and controls the degree of multiprogramming. "
                 "It runs occasionally (seconds/minutes), not on every CPU cycle. "
                 "It never picks which ready process runs next — that is short-term scheduling.",
            "B": "I/O scheduling determines the order of disk/device access requests. "
                 "It is unrelated to selecting a process for CPU execution. "
                 "Do not confuse device queues with the ready queue.",
            "C": "Correct. Short-term scheduling (CPU scheduling) selects one process from the ready queue and allocates the CPU. "
                 "Algorithms like FCFS, SJF, Round Robin, and Priority all operate at this level.",
            "D": "Medium-term scheduling handles swapping — moving entire processes between memory and disk to control memory pressure. "
                 "It does not dispatch CPU time to ready processes.",
        },
        "Memory trick: Long = admit jobs | Medium = swap in/out | Short = CPU dispatch.",
    )
    _r(
        2,
        "Algorithm analysis measures running time as a function of input size n under different input assumptions:\n\n"
        "• Best case — input arrangement that makes the algorithm finish fastest.\n"
        "• Worst case — input that maximizes running time.\n"
        "• Average case — expected time over typical random inputs.\n\n"
        "The question asks for the analysis that uses inputs producing the least time (fastest completion).\n\n"
        "✅ Answer: A — Best case",
        {
            "A": "Correct. Best-case analysis deliberately chooses inputs that minimize comparisons, passes, or iterations. "
                 "Example: linear search finds the target at index 0 — that is the best case, O(1).",
            "B": "Average case considers typical performance across many inputs — not the minimum possible time. "
                 "It is useful for expected behavior but is not the 'fastest possible' analysis.",
            "C": "'Standard case' is not a formal term in algorithm analysis. Exams use best, worst, and average case.",
            "D": "Worst case uses adversarial inputs that maximize work — the opposite of what the question asks.",
        },
        "Best = fastest input | Worst = slowest input | Average = typical input.",
    )
    _r(
        3,
        "UML diagrams are grouped into structural (what exists) and behavioral/dynamic (what happens over time).\n\n"
        "Dynamic/behavioral diagrams include: Sequence, Communication/Collaboration, Activity, State Machine, and Use Case.\n"
        "Structural diagrams include: Class, Object, Component, Deployment, Package.\n\n"
        "An 'instance diagram' showing object snapshots is not a standard UML dynamic-behavior diagram used during analysis.\n\n"
        "✅ Answer: A — Instance diagram",
        {
            "A": "Correct. Object/instance diagrams show a snapshot of objects and links at one moment. "
                 "They are structural snapshots — not the standard way to model dynamic behavior over time during analysis.",
            "B": "Sequence diagrams model message exchange between objects over time — a core dynamic-behavior diagram.",
            "C": "Collaboration (communication) diagrams show object interactions and message ordering — dynamic behavior.",
            "D": "Activity diagrams model workflows, control flow, and parallel activities — dynamic behavior.",
        },
        "Dynamic UML = sequence, activity, state, collaboration. Structural = class, component, deployment.",
    )
    _r(
        4,
        "Java abstract classes can declare abstract methods that concrete subclasses must implement.\n\n"
        "Rules:\n"
        "• Subclass must implement every abstract method OR be declared abstract itself.\n"
        "• Implementation must match signature exactly: same name, parameters, and return type.\n"
        "• `void welcome(String)` does NOT satisfy `String welcome()` — different signature and return type.\n\n"
        "All listed options fail to properly implement `String welcome()` with no parameters.\n"
        "Option A is the keyed answer in this exam set (only defines a different method).\n\n"
        "✅ Answer: A",
        {
            "A": "Does not implement welcome() — normally a compile error unless Class B is abstract. "
                 "This is the exam's keyed answer; in strict Java all options shown would fail compilation.",
            "B": "Wrong return type (void vs String) and wrong parameters (String param vs no params). "
                 "This is method overloading, not overriding the abstract method.",
            "C": "Same problem as A — missing proper welcome() implementation.",
            "D": "Same signature error as B — cannot satisfy the abstract contract.",
        },
        "Abstract method implementation must match name, parameters, and return type exactly.",
    )
    _r(
        5,
        "Ensemble learning combines multiple models to improve prediction accuracy.\n\n"
        "Common ensemble methods: Bagging (Bootstrap Aggregating), Boosting (AdaBoost, Gradient Boosting), Random Forest.\n"
        "Lasso (L1 regularization) is a single-model regression technique — it shrinks coefficients but is NOT an ensemble.\n\n"
        "✅ Answer: A — Lasso",
        {
            "A": "Correct. Lasso regression adds L1 penalty to linear models — it is regularization, not ensemble learning.",
            "B": "Boosting trains models sequentially, each correcting previous errors — classic ensemble method.",
            "C": "Bagging trains models on bootstrap samples and averages/votes — ensemble method.",
            "D": "Random Forest is an ensemble of decision trees — ensemble method.",
        },
        "Ensemble = combine many models (bagging, boosting, RF). Lasso = single model regularization.",
    )
    _r(
        6,
        "Automatic programming generates executable code from high-level specifications or logical descriptions.\n\n"
        "The stem describes generating plans with conditionals and loops from logical specs — that is code/plan generation, not learning or monitoring.\n\n"
        "✅ Answer: A — Automatic programming",
        {
            "A": "Correct. Automatic programming synthesizes programs from formal or logical specifications — including control structures.",
            "B": "Automatic learning refers to machine learning — acquiring patterns from data, not generating code from specs.",
            "C": "Automatic monitoring observes system behavior — not program synthesis.",
            "D": "'Automatic recursive' is not a standard SE/AI term in this context.",
        },
        "Spec → code generation = automatic programming.",
    )
    _r(
        7,
        "CSS controls visual presentation. Transparency is controlled by the opacity property (value 0.0 = fully transparent, 1.0 = fully opaque).\n\n"
        "There is no property literally named 'transparency' in standard CSS.\n\n"
        "✅ Answer: B — Opacity",
        {
            "A": "No standard CSS property named 'transparency'. Opacity is the correct property name.",
            "B": "Correct. `opacity: 0.5` makes an element 50% transparent. Works on the whole element including children.",
            "C": "background sets color/image behind content — separate from transparency control.",
            "D": "Alpha is a color channel concept (RGBA); CSS uses the opacity property for element transparency.",
        },
        "CSS transparency → opacity property (0 to 1).",
    )
    _r(
        8,
        "The OSI model layers:\n"
        "• Application (Layer 7) — network services to applications, process-to-process communication (HTTP, FTP, SMTP).\n"
        "• Transport (Layer 4) — end-to-end delivery (TCP, UDP).\n"
        "• Network (Layer 3) — routing, IP addressing.\n"
        "• Data Link (Layer 2) — frames, MAC addresses.\n"
        "• Physical (Layer 1) — bits on the wire.\n\n"
        "✅ Answer: D — Process-to-process interaction",
        {
            "A": "Frame encapsulation is Data Link layer (Layer 2) — not application layer.",
            "B": "Packet encapsulation is Network layer (Layer 3) work.",
            "C": "Mechanical/electrical connectivity is Physical layer (Layer 1).",
            "D": "Correct. Application layer protocols enable process-to-process communication across the network.",
        },
        "Layer 7 Application = process-to-process (HTTP, DNS, SMTP).",
    )
    _r(
        9,
        "JavaScript provides built-in JSON methods:\n"
        "• JSON.stringify(obj) — converts a JavaScript object → JSON string (serialization).\n"
        "• JSON.parse(str) — converts a JSON string → JavaScript object (deserialization).\n\n"
        "The PDF OCR shows 'stringify0' — that refers to JSON.stringify().\n\n"
        "✅ Answer: C — JSON.stringify()",
        {
            "A": "parseJson() is not the standard built-in name — use JSON.parse() for the opposite operation.",
            "B": "toJson() is not a standard JavaScript built-in method.",
            "C": "Correct. JSON.stringify() serializes objects to JSON strings for storage or transmission.",
            "D": "JSON.parse() deserializes strings into objects — the reverse of what the question asks.",
        },
        "Object → string: JSON.stringify | string → object: JSON.parse",
    )
    _r(
        10,
        "Well-known TCP ports (memorize for exams):\n"
        "• 22 — SSH (secure shell)\n"
        "• 21 — FTP control | 20 — FTP data\n"
        "• 23 — Telnet\n"
        "• 80 — HTTP | 443 — HTTPS\n\n"
        "✅ Answer: B — 22",
        {
            "A": "Port 20 is FTP data transfer — not SSH.",
            "B": "Correct. SSH (Secure Shell) uses TCP port 22.",
            "C": "Port 23 is Telnet — unencrypted remote login.",
            "D": "Port 21 is FTP control channel.",
        },
        "SSH=22, FTP=21/20, Telnet=23, HTTP=80, HTTPS=443.",
    )


_build_bank()
