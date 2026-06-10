"""Rich per-option explanations when the concept engine falls back to generic text."""

from __future__ import annotations

import re
from typing import Any

from bdu_concept_engine import (
    _glossary_lookup,
    _norm,
    _stem_intent,
    explain_correct_option,
    explain_wrong_option,
)

GENERIC_WRONG_MARKERS = (
    "does not answer the specific concept",
    "is not the standard term for",
    "To see why",
    "ask yourself what concept",
)

GENERIC_CORRECT_MARKERS = (
    "correctly answers the specific concept tested",
    "matches the specific concept tested in this question",
    "directly addresses the specific concept tested",
    "this is the standard textbook answer for this scenario",
)


def is_generic_fallback(body: str) -> bool:
    return any(m in body for m in GENERIC_WRONG_MARKERS + GENERIC_CORRECT_MARKERS)


def _opts(q: dict) -> dict[str, str]:
    return {o["key"]: o["text"] for o in q["options"]}


def _term_hit(phrase: str, t: str) -> bool:
    if phrase in t:
        return True
    if t.startswith(phrase):
        return True
    if phrase.endswith("y") and (phrase[:-1] + "ies") in t:
        return True
    if (phrase + "s") in t or (phrase + "es") in t:
        return True
    return False


def _try_rules(q: dict, key: str, text: str) -> str | None:
    stem = _norm(q.get("text", ""))
    t = _norm(text)
    correct = q["answer"]
    topic = q.get("topic", "General")

    if "class" in stem and ("css" in stem or "select" in stem):
        if t.startswith(".") or t == ".classname":
            return (
                f"'{text}' is the CSS class selector — a dot followed by the class name selects all elements "
                f'with class="{text.lstrip(".")}". This is the standard answer for class-based selection.'
            ) if key == correct else None
        if t.startswith("#") or "classname" in t and "#" in text:
            return (
                f"'{text}' uses the ID selector (#). IDs are unique per page; the question asks how to select "
                f"by class name, which uses a dot prefix (.classname), not a hash."
            )
        if "element.class" in t or "element" in t and "class" in t:
            return (
                f"'{text}' is a compound selector (element + class), not the basic syntax for selecting "
                f"any element with a given class. The canonical class-only selector is .classname."
            )
        if "class:" in t and "element" in t:
            return (
                f"'{text}' is not valid CSS selector syntax. CSS uses selector {{ property: value; }} — "
                f"the colon belongs inside the rule block, not in the selector name."
            )

    if "project planning" in t or "project initiating" in t or "project executing" in t or "project closing" in t:
        mapping = {
            "project planning": "Planning produces WBS, schedule, and cost estimates — the outputs asked for in planning-phase questions.",
            "project initiating": "Initiating authorizes the project and defines the charter — it comes before detailed planning.",
            "project executing": "Executing carries out the work defined in the plan — after planning is complete.",
            "project closing": "Closing archives deliverables and closes contracts — the final lifecycle phase.",
        }
        for phrase, expl in mapping.items():
            if phrase in t:
                return expl if key == correct else expl.replace("— the outputs", "— not the planning outputs").replace("it comes", "that phase comes")

    if "queue" in t and len(t) < 12:
        return "A queue is a linear FIFO structure — elements enter at rear and leave at front; not hierarchical like a tree."
    if "stack" in t and len(t) < 12:
        return "A stack is a linear LIFO structure — last in, first out; not hierarchical like a tree."
    if "linked" in t and "list" in t:
        return "A linked list is a linear sequence of nodes — each node points to the next; trees branch into children."
    if t == "tree" or "tree" in t and len(t) < 8:
        return "A tree is a non-linear hierarchical structure — nodes have parent-child relationships, unlike linear lists."

    if "uniform" in t and "search" in stem:
        return "Uniform-cost search expands by path cost, not heuristic promise; A* uses f(n)=g(n)+h(n) for informed optimal search."
    if t in ("cost", "search") and "informed" in stem:
        return f"'{text}' alone is not the name of an informed search algorithm. A* Search combines actual cost g(n) and heuristic h(n)."

    if topic == "Security" and "risk" in t:
        strategies = {
            "risk transfer": "Risk transfer shifts liability to another party (e.g., insurance) — different from accepting the risk yourself.",
            "risk retention": "Risk retention means accepting the risk and budgeting for potential loss — the strategy when you keep the exposure.",
            "risk reduction": "Risk reduction (mitigation) lowers probability or impact through controls — not the same as retaining/accepting risk.",
            "risk avoidance": "Risk avoidance eliminates the activity causing risk — stronger than retention or transfer.",
        }
        for term, expl in strategies.items():
            if term in t:
                return expl

    if "chmod" in stem or "rwx" in stem or re.search(r"[-][rwx]{9}", q.get("text", "")):
        if t.strip() in ("744", "755", "700", "766"):
            octal_map = {
                "755": "755 = rwxr-xr-- (owner rwx, group r-x, other r--) — standard for executables.",
                "744": "744 = rwxr--r-- — group and others lack execute; does not match rwxr-xr--.",
                "700": "700 = rwx------ — only owner has any access; too restrictive for rwxr-xr--.",
                "766": "766 would grant group/other write bits not present in rwxr-xr--.",
            }
            if t.strip() in octal_map:
                return octal_map[t.strip()]

    if "manifest" in stem or ("permission" in stem and "android" in stem):
        if "manifest" in t:
            return (
                "AndroidManifest.xml declares components, permissions, intent filters, and package metadata — "
                "required at install time; permissions like GPS/Camera are declared here."
            ) if key == correct else (
                "Views, Intents, and Content Providers are runtime components — permissions are declared in "
                "AndroidManifest.xml, not inside individual UI widgets or intent objects."
            )
        if "fragment" in t:
            return (
                "Fragments are reusable UI portions hosted inside an Activity — they are not the manifest file "
                "where permissions are declared."
            )

    if "fragment" in stem and "reusable" in stem:
        if "fragment" in t:
            return "Fragments encapsulate reusable UI and logic inside an Activity lifecycle — the standard Android answer."
        if "activity" in t and len(t) < 20:
            return "Activities host screens; Fragments are the reusable sub-units placed inside an Activity."

    if "android" in stem or topic == "Android":
        android_parts = {
            "broadcast": "BroadcastReceivers listen for system-wide Intents (e.g., connectivity changes) — not reusable UI inside an Activity.",
            "activity": "Activities represent full screens with their own lifecycle — broader than a reusable UI portion inside one screen.",
            "content provider": "ContentProviders expose structured data to other apps via content URIs — not a reusable UI widget.",
            "fragment": "Fragments are reusable UI/logic portions hosted inside an Activity — the answer for reusable in-activity components.",
            "service": "Services run background work without a UI — different from screen-level or reusable UI components.",
            "intent": "Intents are messaging objects for navigation and data passing — not a UI component type.",
        }
        for phrase, expl in android_parts.items():
            if _term_hit(phrase, t):
                return expl

    if "osi" in stem and "layer" in stem:
        layers = {
            "application": "Application layer (L7) handles network transparency, resource allocation, and user-facing services like HTTP and DNS.",
            "transport": "Transport layer (L4) provides end-to-end delivery, segmentation, and flow control — not transparency/resource allocation at the application level.",
            "network": "Network layer (L3) handles routing and logical IP addressing — below the application services asked about here.",
            "data link": "Data link layer (L2) handles framing and MAC addressing on a single link — not application-level transparency.",
            "presentation": "Presentation layer (L6) handles encryption, compression, and data translation between formats.",
            "session": "Session layer (L5) manages dialog control and synchronization between communicating applications.",
        }
        for layer, expl in layers.items():
            if _term_hit(layer, t):
                return expl

    if "breakpoint" in stem or ("debugging" in stem and "pause" in stem):
        if "pause" in t or "breakpoint" in t:
            return "A breakpoint pauses program execution at a chosen line so you can inspect variables and step through code."
        if "loop" in t:
            return "Loops are control structures — breakpoints pause execution anywhere, not specifically loop starts."
        if "error" in t or "exception" in t:
            return "Errors/exceptions signal problems at runtime — breakpoints are proactive debugger stops, not error indicators."
        if "function" in t or "end" in t:
            return "Function boundaries are code structure — a breakpoint's purpose is pausing execution for inspection, not marking scope ends."

    if "top-level window" in stem or ("title" in stem and "border" in stem):
        widgets = {
            "frame": "Frame is the AWT/Swing class for a top-level window with title bar and border decorations.",
            "window": "Window is a generic term; in Java AWT the specific top-level decorated window class is Frame.",
            "panel": "Panel is a container for grouping components inside a window — not itself a top-level window.",
            "container": "Container is a general superclass for components that hold others — not the decorated top-level window class.",
        }
        for w, expl in widgets.items():
            if w in t:
                return expl

    if "risk" in stem and ("transfer" in stem or "third party" in stem or "insurance" in stem):
        risks = {
            "risk transference": "Risk transference shifts liability to a third party (insurance, outsourcing) — matches the stem.",
            "risk mitigation": "Risk mitigation reduces probability or impact through controls — you still own the risk.",
            "risk acceptance": "Risk acceptance means tolerating the risk and budgeting for loss — not shifting it externally.",
            "risk avoidance": "Risk avoidance eliminates the risky activity entirely — stronger than transferring impact.",
        }
        for term, expl in risks.items():
            if _term_hit(term, t):
                return expl

    if "package manager" in t or ("configuration files" in stem and "installation" in stem):
        if "package manager" in t:
            return "Package managers install software and track dependency versions during installation and configuration."
        if "version control" in t:
            return "Version control tracks source-code history — package managers handle installed binaries and dependency resolution."
        if "document generation" in t:
            return "Documentation tools generate docs — they do not manage installed software packages or dependencies."

    if "hash table" in t or "hash table" in stem:
        if "hash table" in t:
            return "Hash tables offer O(1) average lookup/insert/delete — ideal for real-time data with frequent updates."
        if "stack" in t:
            return "Stacks are LIFO — efficient for undo/backtracking, not general keyed lookup at scale."
        if "queue" in t:
            return "Queues are FIFO — good for ordering, not keyed random access for real-time analysis."
        if "binary tree" in t or "tree" in t:
            return "Trees support ordered search but insertion/deletion is slower than hash tables for keyed real-time data."

    if "maintenance" in stem and ("fault" in stem or "repair" in stem):
        maint = {
            "corrective": "Corrective maintenance fixes discovered faults/defects after deployment — the textbook term for repair.",
            "adaptive": "Adaptive maintenance adapts software to a changed environment (OS, regulations) — not fault repair.",
            "perfective": "Perfective maintenance improves performance or maintainability without fixing a specific fault.",
            "preventive": "Preventive maintenance reduces future failure risk proactively — broader than fixing an existing bug.",
        }
        for term, expl in maint.items():
            if _term_hit(term, t):
                return expl

    if "flow control" in stem or ("packet" in stem and "too quickly" in stem):
        if "flow control" in t:
            return "TCP flow control (windowing) prevents overwhelming the receiver — the direct answer for rate mismatch."
        if "encapsulation" in t:
            return "Encapsulation wraps data with headers — it does not throttle send rate between two hosts."

    if "integration test" in stem or ("between modules" in stem and "test" in stem):
        if "integration" in t:
            return "Integration testing verifies interfaces and interactions between combined modules — after unit tests pass."
        if "unit" in t:
            return "Unit testing isolates a single module/function — it does not test cross-module wiring."
        if "system" in t:
            return "System testing validates the complete integrated application — broader than module-to-module interaction alone."
        if "acceptance" in t or "uat" in t:
            return "User acceptance testing confirms fitness for business needs — it follows integration and system testing."

    if "supervised" in stem or "labeled data" in stem:
        if "supervised" in t:
            return "Supervised learning trains on labeled input–output pairs — classification and regression are supervised tasks."
        if "unsupervised" in t:
            return "Unsupervised learning finds structure in unlabeled data — clustering, not labeled classification."
        if "classification" in t and "spam" in stem:
            return "Email spam detection is a labeled yes/no classification problem — supervised learning with a training set."

    if "time-series" in t or "time series" in t:
        return "Time-series forecasting models sequential observations over time — suited to demand forecasting and predictive maintenance."

    if "exokernel" in t or "microkernel" in t:
        kernels = {
            "exokernel": "Exokernel exposes low-level hardware resources and pushes policy to applications — minimalist delegation.",
            "microkernel": "Microkernel runs minimal services in kernel space with drivers in user space — not the same as exokernel exam answer.",
            "monolithic": "Monolithic kernel bundles drivers and services in one address space — opposite of minimalist delegation.",
            "hybrid": "Hybrid kernels (e.g., Windows NT style) mix monolithic and microkernel ideas — not minimalist exokernel design.",
        }
        for term, expl in kernels.items():
            if term in t:
                return expl

    if "do-while" in t or "do while" in t:
        return "do-while evaluates the condition after the body — guaranteed at least one execution even when the condition is initially false."

    if "while loop" in t and "at least once" in stem:
        return "while checks the condition before each iteration — if false initially, the body never runs."

    if "gdpr" in stem or "ccpa" in stem or "data privacy" in stem:
        if "informed" in t or "inform" in t:
            return "GDPR/CCPA require transparency — users must know what data is collected and how it is used before meaningful consent."
        if "without user consent" in t or "without consent" in t:
            return "Privacy laws require lawful basis/consent for collection — collecting without consent violates GDPR/CCPA principles."

    if "wbs" in stem or "work breakdown" in stem:
        if "hierarchical" in t or "deliverable" in t:
            return "A WBS decomposes project deliverables into hierarchical work packages — standard PM practice for task allocation."
        if "single team" in t or "random tasks" in t:
            return "Effective WBS follows deliverable structure, not arbitrary splits or one-team ownership of everything."

    if "aes" in t and ("encrypt" in stem or "database" in stem):
        return "AES is a symmetric encryption standard widely used to protect data at rest, including database storage."

    if "encrypt" in stem or "database" in stem and "storage" in stem:
        crypto = {
            "sha": "SHA-256 is a one-way hash for integrity checks — it does not encrypt database contents for confidentiality.",
            "hash": "Hashing produces a fixed digest for integrity — reversible encryption (AES) is needed to protect stored data.",
            "rsa": "RSA is asymmetric encryption — used for keys/signatures, not the standard choice for bulk database encryption at rest.",
        }
        for term, expl in crypto.items():
            if term in t:
                return expl

    if "demand forecasting" in stem or "predictive maintenance" in stem or "time-series" in stem:
        ml_types = {
            "regression": "Regression predicts continuous values from features — time-series forecasting models temporal sequences explicitly.",
            "classification": "Classification assigns discrete labels — demand forecasting needs sequential temporal prediction.",
            "clustering": "Clustering finds groups in unlabeled data — not supervised forecasting of future demand.",
            "time-series": "Time-series forecasting models sequential observations over time — suited to demand and maintenance prediction.",
        }
        for term, expl in ml_types.items():
            if term in t:
                return expl

    if "function point" in t:
        return "Function Points measure software size for estimation — not a type of software maintenance."

    if "builder" in t and "pattern" in stem:
        return "Builder separates construction of a complex object from its representation — assemble parts step by step independently."

    if "mutual exclusion" in t and "deadlock" in stem:
        return "Mutual exclusion means only one process may hold a non-sharable resource at a time — one of Coffman’s deadlock conditions."

    if "hold and wait" in t and "deadlock" in stem:
        return "Hold and Wait: a process holds resources while waiting for additional ones — a deadlock condition, not mutual exclusion alone."

    if "fcfs" in t or "first-come" in t or "first come" in t:
        return "FCFS (First-Come, First-Served) schedules processes in arrival order — non-preemptive and simple."

    if "innerhtml" in t or "getelementbyid" in t:
        return "element.innerHTML reads/writes the HTML content inside a DOM node — the standard way to change page content dynamically."

    if "public key infrastructure" in t or "pki" in t:
        return "PKI uses digital certificates and certificate authorities to bind public keys to identities — certificate-based authentication."

    if "stateful" in t and "firewall" in stem:
        return "Stateful inspection tracks connection state and allows only packets belonging to legitimate established sessions."

    if "xss" in t or "cross-site scripting" in t:
        return "XSS injects malicious JavaScript into pages viewed by other users — can steal session cookies and user data."

    if "event-driven" in t and "architecture" in stem:
        return "Event-driven architecture reacts to events asynchronously — supports responsiveness and real-time processing pipelines."

    if "refactor" in stem:
        if "internal" in t or "structure" in t:
            return "Refactoring improves internal structure without changing external behavior — not adding features or rewriting for performance alone."

    if "normal form" in stem and "partial" in stem:
        if "2nf" in t or "second normal" in t:
            return "2NF eliminates partial dependencies — non-key attributes must depend on the whole primary key, not part of it."

    if "foreign key" in stem:
        if "referential" in t or "integrity" in t:
            return "Foreign keys enforce referential integrity — child rows must reference an existing parent primary key (or NULL if allowed)."

    if "select *" in t or "select all" in t:
        return "SELECT * retrieves all columns from the named table — standard SQL syntax for full-row projection."

    return None


def explain_wrong_rich(q: dict, key: str, text: str) -> str:
    ruled = _try_rules(q, key, text)
    if ruled:
        return ruled

    body = explain_wrong_option(q, key, text)
    if not is_generic_fallback(body):
        return body

    correct = q["answer"]
    opts = _opts(q)
    correct_text = opts.get(correct, "")
    topic = q.get("topic", "General")
    intent = _stem_intent(q.get("text", ""))
    w_def = _glossary_lookup(text)
    c_def = _glossary_lookup(correct_text)

    if w_def and c_def:
        return (
            f"'{text}' refers to {w_def}. This question tests {intent}, which needs "
            f"'{correct_text}' ({c_def}). These are different concepts — do not swap them on the exam."
        )
    if w_def:
        return (
            f"'{text}' means {w_def}. That is a real {topic} concept, but this stem asks for "
            f"{intent} — the answer is {correct}: {correct_text}."
        )
    stem_hint = q.get("text", "").strip()
    if len(stem_hint) > 40:
        stem_hint = stem_hint[:120] + ("…" if len(stem_hint) > 120 else "")
        return (
            f"'{text}' does not fit the scenario: {stem_hint} "
            f"The keyed answer is {correct} — {correct_text}."
        )
    return (
        f"'{text}' is a plausible {topic} term but not what this stem requires. "
        f"Compare carefully with {correct}: {correct_text}."
    )


def explain_correct_rich(q: dict, text: str) -> str:
    ruled = _try_rules(q, q["answer"], text)
    if ruled:
        return ruled

    body = explain_correct_option(q, text)
    if not is_generic_fallback(body):
        return body

    topic = q.get("topic", "General")
    intent = _stem_intent(q.get("text", ""))
    c_def = _glossary_lookup(text)
    if c_def:
        return f"'{text}' is correct because it matches {intent}. Definition: {c_def}."
    return f"'{text}' is the correct answer — it directly addresses {intent} in {topic}."
