"""Detailed per-choice explanations for BDU Model Exit Exam."""

from __future__ import annotations

import re
from typing import Any

from bdu_concept_engine import build_overview, explain_correct_option, explain_wrong_option
from generic_deep_builder import enrich_with_concept

# examNumber -> hand-crafted entry (overview, options bodies without prefix, studyTip)
CURATED: dict[int, dict[str, Any]] = {}


def _opt(correct: str, key: str, text: str, body: str) -> str:
    tag = "CORRECT" if key == correct else "INCORRECT"
    return f'Option {key} ({tag}): "{text}". {body}'


def _entry(overview: str, opts: dict[str, str], tip: str) -> dict[str, Any]:
    return {"overview": overview, "options": opts, "studyTip": tip}


def _r(num: int, overview: str, opts: dict[str, str], tip: str) -> None:
    CURATED[num] = _entry(overview, opts, tip)


def _build_curated() -> None:
    _r(
        1,
        "Asymptotic notation answers depend on WHICH bound the question asks for. "
        "Big-Oh O(f(n)) describes an UPPER bound on growth in the WORST case — the algorithm will not do worse than f(n) for large n. "
        "Theta gives a tight bound (upper and lower), and Omega gives a lower (best-case) bound. "
        "The stem explicitly says 'worst possible set of inputs', so Big-Oh is the standard notation.",
        {
            "A": "Theta Θ(n) means the algorithm grows proportionally to n in BOTH worst and best case — a tight bound. "
                 "The question only asks for worst-case upper-bound notation, not a tight bound. Theta is stricter than what the stem requires.",
            "B": "Big-Oh is the conventional notation for worst-case upper bounds in exit exams. "
                 "If an algorithm's worst case is at most 3n² + 5n, we say O(n²). This directly matches 'worst possible inputs'.",
            "C": "Big-Omega Ω(f(n)) describes a LOWER bound — how fast the algorithm must grow at minimum (often linked to best case). "
                 "Worst-case analysis uses Big-Oh, not Omega. Picking Omega confuses best-case and worst-case notation.",
            "D": "'All' is never correct when the four notations serve different purposes. "
                 "Only one notation specifically denotes worst-case upper bounds — Big-Oh.",
        },
        "Worst case → Big-Oh O(·). Best case → Omega Ω(·). Tight bound → Theta Θ(·).",
    )
    _r(
        2,
        "Binary search repeatedly halves the search space. Each comparison eliminates half of the remaining elements. "
        "Halving n times until one element remains takes log₂(n) steps, giving O(log n) time. "
        "It requires a sorted array and random access (indexable structure).",
        {
            "A": "O(n) is linear search complexity — scan every element once. Binary search never examines all n elements; "
                 "it eliminates half each step, which is logarithmic, not linear.",
            "B": "O(n²) is quadratic — typical of nested loops comparing all pairs. Binary search has one loop that divides the range, not n² work.",
            "C": "O(1) is constant time — e.g. accessing arr[0]. Binary search still performs multiple comparisons as n grows; work increases with n.",
            "D": "O(log n) is correct. For n = 1,000,000, binary search needs at most about 20 comparisons (log₂ 1,000,000 ≈ 20), not millions.",
        },
        "Sorted array + halving → binary search → O(log n).",
    )
    _r(
        3,
        "To find Big-O, identify the DOMINANT term — the one that grows fastest as n → ∞. "
        "Compare: log n < n < n log n < n². "
        "In T(n) = 2n + 3n² + log n + n log n + n, the term 3n² dominates because n² grows faster than every other term. "
        "Drop constants (3) and lower-order terms → O(n²).",
        {
            "A": "O(n) would mean linear growth dominates. While 2n and n are linear terms, they are overwhelmed by 3n² for large n. "
                 "Example: at n = 10,000, n = 10,000 but n² = 100,000,000 — n² wins.",
            "B": "O(n²) is correct. The highest-degree term is n² (coefficient 3). All other terms become insignificant compared to 3n² as n grows.",
            "C": "O(log n) is the slowest-growing term in the entire expression (from 'log n' alone). "
                 "The full function is NOT logarithmic — one small term does not define the whole complexity.",
            "D": "O(n log n) is faster than O(n) but slower than O(n²). Since 3n² appears in the sum, n² dominates n log n. "
                 "Merge sort is O(n log n); this polynomial has an n² term, so it is quadratic, not linearithmic.",
        },
        "List all terms → pick highest power of n → drop constants → that is Big-O.",
    )
    _r(
        4,
        "To insert at the END of a singly linked list when you only have a pointer to the HEAD, you must traverse from head to tail — visiting up to n nodes — then append. "
        "No tail pointer is given, so you cannot jump to the end in O(1). Traversal is O(n). "
        "With BOTH head and tail pointers, append can be O(1).",
        {
            "A": "O(1) would apply only if you already had a pointer to the tail node (or a tail reference). "
                 "The question states the pointer points to the HEAD only, so you must walk the whole list first.",
            "B": "O(n) is correct. In the worst case the last node is n steps from the head; each step is one pointer follow.",
            "C": "O(log n) applies to divide-and-conquer on sorted indexable data, not linked-list traversal. Linked lists do not support random access or halving.",
            "D": "O(n²) would require nested loops over n — e.g. comparing every pair. A single traversal to find the tail is one pass → O(n), not O(n²).",
        },
        "Singly linked list, head only, insert at end → traverse n nodes → O(n).",
    )
    _r(
        5,
        "A circular linked list is a linear list where the last node's next pointer points back to the first node, forming a ring. "
        "Singly linked ends with NULL; doubly linked has prev+next but need not wrap; a tree is hierarchical, not linear.",
        {
            "A": "A tree is hierarchical (parent/child), not a linear list where last connects to first. Trees do not have a 'last node pointing to first' structure.",
            "B": "Doubly linked lists have forward and backward pointers but typically end with NULL at both ends unless explicitly made circular. "
                 "The defining feature here is last→first wrap-around, which names 'circular' linked list.",
            "C": "Circular linked list exactly matches: last node points to the first node, so traversal can continue indefinitely around the ring.",
            "D": "Singly linked list ends with NULL at the last node — it does NOT point back to the first. That is the key difference from circular.",
        },
        "Last → first pointer = circular linked list.",
    )
    _r(
        6,
        "In C++, 'new' allocates memory dynamically on the heap and returns a pointer. "
        "'delete' frees that memory. 'struct' declares a structure type; 'create' is not a C++ operator.",
        {
            "A": "'new' is the C++ operator for dynamic allocation (e.g. int* p = new int[10]). Correct answer.",
            "B": "'struct' is a keyword to define composite types — it does not allocate memory by itself.",
            "C": "'create' is not a standard C++ memory operator. Some languages use 'new' or 'malloc' (C), not 'create'.",
            "D": "'delete' releases memory allocated by 'new', but the question asks which operator ALLOCATES — that is 'new', not 'delete'.",
        },
        "Allocate → new. Free → delete. Never confuse the two directions.",
    )
    _r(
        7,
        "Recursion uses the call stack: each recursive call pushes a stack frame; when the call returns, it pops. "
        "Function calls (including recursion) are naturally implemented with a stack — LIFO order matches nested calls.",
        {
            "A": "Stack is correct. Recursive factorial, DFS, and backtracking all rely on the call stack to hold local variables and return addresses.",
            "B": "Tree is a data structure shape, not the mechanism the runtime uses to execute recursive calls. You may BUILD a tree recursively, but execution uses a stack.",
            "C": "Queue is FIFO — used for BFS, scheduling, buffers — not for nested function calls which are LIFO.",
            "D": "Linked list is a general structure; the OS/runtime specifically uses a call stack (which may be implemented as a linked structure internally, but 'Stack' is the exam answer).",
        },
        "Recursion → call stack → choose Stack.",
    )
    _r(
        8,
        "Hierarchical relationships (parent-child, levels, one root) are modeled by trees. "
        "Examples: file systems, org charts, DOM (partially), BSTs. Graphs allow cycles; queues/stacks are linear.",
        {
            "A": "Tree is correct — hierarchical = tree structure with root and levels.",
            "B": "Priority queue orders by priority, not hierarchy. It is a linear ADT with special ordering.",
            "C": "Graph can represent hierarchy but also arbitrary connections and cycles. When the question says 'hierarchical', tree is the precise answer.",
            "D": "Deque allows insertion/deletion at both ends — linear, not hierarchical.",
        },
        "Hierarchical → Tree. Network with cycles → Graph.",
    )
    _r(
        9,
        "C++ identifiers must start with a letter or underscore, contain only letters/digits/underscores, "
        "and must NOT be a reserved keyword. 'int' and 'class' are keywords; '2value' starts with a digit.",
        {
            "A": "'int' is a reserved keyword in C++ (integer type). Keywords cannot be used as variable names.",
            "B": "'_count' starts with underscore followed by letters — valid identifier syntax.",
            "C": "'2value' begins with digit '2' — C++ identifiers cannot start with a number.",
            "D": "'class' is a reserved keyword used to define classes — not a valid user identifier.",
        },
        "Valid identifier: starts with letter/_ , not a keyword, no leading digit.",
    )
    _r(
        10,
        "The 'continue' statement skips the rest of the current loop iteration and jumps to the next iteration. "
        "Trace which values reach the print/cout statement — only iterations that do not hit 'continue' on that line contribute.",
        {
            "A": "0 would print only if no iteration reached the output statement with a non-skipped path.",
            "B": "1 would result from a different loop count or condition than continue provides.",
            "C": "1.0 is a floating-point format — check whether the code prints int vs double.",
            "D": "1.2 matches the traced output when continue skips specific iterations and the remaining path prints this value.",
        },
        "Trace loops with continue: skip body, go to next iteration.",
    )
    _r(
        11,
        "Pass-by-reference (int &i) creates an alias to the caller's variable. "
        "void f(int &i) { i = i * 5; } with i=5 in main changes main's i to 25. "
        "Pass-by-value would leave i as 5.",
        {
            "A": "5 is the value BEFORE the function modifies i — correct only for pass-by-VALUE without &. Reference (&) means main's i becomes 5×5=25.",
            "B": "25 = 5 × 5. The reference parameter modifies the original variable in main — cout prints the updated value 25.",
            "C": "10 might come from adding 5 or wrong arithmetic — the code multiplies by 5, giving 25.",
            "D": "20 would require multiplying by 4 (5×4=20), not by 5 as the function does.",
        },
        "Reference (&) = alias. Changes inside function affect caller. 5×5=25.",
    )
    _r(
        12,
        "Function CALL uses name(args); — e.g. sum(num1, num2);. "
        "Function DECLARATION specifies return type and parameter types: int sum(int, int);. "
        "The question asks for correct CALLING, not declaration syntax.",
        {
            "A": "'int sum(num1, num2):' mixes declaration syntax with invalid colon — not a function call.",
            "B": "'sum(num1, num2);' is the actual call — name, parentheses, arguments, semicolon. Correct.",
            "C": "Option unclear in OCR — a valid call is sum(num1, num2); with semicolon.",
            "D": "'sum(int num1, int num2);' is a declaration/prototype with types — calls omit parameter types.",
        },
        "Call: name(args); — Declaration: type name(type args);",
    )
    _r(
        13,
        "Array facts: arrays cannot be assigned to each other directly in C/C++; "
        "last index is size−1 not size; out-of-bounds access is illegal. All three are true → All of the above.",
        {
            "A": "True — you cannot assign one array to another with = in C/C++; use element-wise copy.",
            "B": "True — for size n, valid indices are 0..n−1; index n is out of bounds.",
            "C": "True — accessing beyond array bounds is illegal/undefined behavior.",
            "D": "All of the above — since A, B, and C are each true statements about arrays.",
        },
        "Arrays: no direct assignment, last index = size−1, bounds matter.",
    )


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def _blob(stem: str, opts: dict[str, str]) -> str:
    return _norm(stem + " " + " ".join(opts.values()))


# ── Pattern-based option explainers ─────────────────────────────────────────

def _explain_complexity_option(stem: str, key: str, text: str, correct: str, opts: dict[str, str]) -> str | None:
    t = _norm(text)
    if not re.search(r"o\s*\(|log\s*n|n\s*\^?\s*2|theta|omega|big.?oh", t + " " + _norm(stem)):
        return None

    if re.search(r"worst|big.?oh|upper bound", _norm(stem)):
        if "big" in t and "oh" in t:
            return (
                "Big-Oh describes worst-case upper bounds. The question asks about worst possible inputs, "
                "so this notation directly applies."
                if key == correct
                else "Big-Oh is for worst-case upper bounds, but another option is the specific match here; re-read the stem."
            )
        if "theta" in t:
            return "Theta is a tight bound (upper AND lower). The question asks only for worst-case notation — that is Big-Oh, not Theta."
        if "omega" in t:
            return "Omega is a lower bound (best-case growth). Worst-case analysis uses Big-Oh, not Omega."
        if t in ("all", "all of the above", "all of above"):
            return "These notations have distinct meanings; they are not interchangeable for worst-case analysis."

    if re.search(r"2n|n\^2|n2|complexity order|dominant|time function", _norm(stem)):
        if re.search(r"n\s*\^?\s*2|n2|\(n2\)", t):
            return (
                "n² is the dominant term in the given expression — it grows faster than n, n log n, and log n. "
                "Drop lower terms and constants → O(n²)."
                if key == correct
                else "n² appears in the expression but is NOT the dominant term in this question's context."
            )
        if re.search(r"log\s*n|logn", t) and "n log" not in t:
            return "log n alone is the slowest-growing term in typical sums — it never dominates n, n log n, or n² unless those are absent."
        if re.search(r"n\s*log", t):
            return "n log n grows faster than n but slower than n². If n² is in the expression, n² dominates, not n log n."
        if re.search(r"o\s*\(\s*1\s*\)|constant", t):
            return "O(1) means work does not grow with n. This expression clearly contains n and n² terms, so it is not constant."
        if re.search(r"o\s*\(\s*n\s*\)", t) and "log" not in t:
            return "O(n) means linear growth dominates. If n² or higher appears in the sum, linear terms are overshadowed for large n."

    if re.search(r"binary search", _norm(stem)):
        if re.search(r"log", t):
            return "Binary search halves the search space each step → O(log n)." if key == correct else "Binary search is O(log n), not this complexity class."
        if re.search(r"o\s*\(\s*n\s*\)", t):
            return "O(n) is linear search — checking every element. Binary search eliminates half each time → logarithmic."
        if re.search(r"n\s*\^?\s*2|n2", t):
            return "O(n²) implies nested loops over data. Binary search is a single halving loop → O(log n)."

    return None


def _explain_ds_structure(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "circular" in t and "last node" in s and "first" in s:
        return "Circular linked list: last node's next points to first — exact match." if key == correct else "Does not define last→first wrap-around."
    if "stack" in t and ("recurs" in s or "recursive" in s):
        return "Recursion uses the call stack (LIFO)." if key == correct else "Not the structure used by recursive call activation."
    if "tree" in t and "hierarch" in s:
        return "Trees model parent-child hierarchy." if key == correct else "Not primarily a hierarchical structure."
    if "new" in t and "c++" in s and "alloc" in s:
        return "'new' allocates on the heap in C++." if key == correct else "Not the C++ dynamic allocation operator."
    if "delete" in t and "alloc" in s:
        return "'delete' frees memory; the question asks which ALLOCATES — that is 'new'."
    if "queue" in t and "fifo" in s:
        return "FIFO → Queue." if key == correct else "Queue is FIFO; this option does not match."
    return None


def _explain_web(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "css" in s and "syntax" in s:
        if re.search(r"\{.*:.*\}", text):
            return "Valid CSS: selector { property: value; }." if key == correct else "Invalid CSS syntax — property/value must use braces and colon."
        if "color=" in t or ".calor" in t:
            return "CSS uses colon inside braces, not '=' like HTML attributes."
    if "web server" in s or "http request" in s:
        if "web server" in t:
            return "Web servers (Apache, Nginx) accept HTTP requests and return responses." if key == correct else "Browsers send requests; servers receive them."
        if "browser" in t:
            return "Browsers are clients that send HTTP requests — they do not serve responses to other clients."
    if "bold" in s and ("strong" in t or "<b>" in t):
        return "<strong> or <b> renders bold text in HTML." if key == correct else "Not the standard HTML tag for bold text."
    if "reset" in t and "clear" in s and "form" in s:
        return "<input type='reset'> clears all form fields to defaults." if key == correct else "Submit sends data; hidden stores values; reset clears the form."
    if "hypertext" in t and ("click" in s or "link" in s):
        return "Hypertext links navigate to other documents or anchors." if key == correct else "URL is the address; hypertext is the clickable linked text concept."
    return None


def _explain_java_oop(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "polymorph" in s and "runtime" in s:
        if "virtual" in t:
            return "Runtime polymorphism uses virtual methods and dynamic dispatch via pointers/references." if key == correct else "Compile-time overloading is not runtime polymorphism."
        if "compile" in t or "fest execution" in t or "fast execution" in t:
            return "Compile-time binding is faster but that describes static/overloading, not runtime polymorphism."
    if "constructor" in s and "incorrect" in s:
        if "return type" in t:
            return "Constructors must NOT have a return type — not even void. A method with void return is not a constructor." if key == correct else "This is actually a valid constructor property."
    if "inheritance" in s and "consequence" in s:
        if "superclass" in t and "subclass" in t:
            return "Changes in superclass propagate to all subclasses — tight coupling consequence." if key == correct else "Not a classic consequence of inheritance coupling."
    if "overloading" in t and "unique" in s:
        return "Overloading (same name, different parameters) is distinct from binding types (early/late/static)." if key == correct else "Early binding, late binding, and static binding are related concepts — overloading is the unique one."
    return None


def _explain_db(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "dirty read" in t or "oilty" in t:
        return "Dirty read: transaction reads uncommitted data from another transaction." if key == correct else "Different isolation anomaly."
    if "deferred modification" in t:
        return "Deferred modification: DB changes written only after commit." if key == correct else "Immediate modification writes before commit."
    if "shrinking" in t and "lock" in s:
        return "Shrinking phase: locks may be released but not acquired (2PL)." if key == correct else "Growing phase acquires locks; deadlock phase is not standard 2PL terminology."
    if "scalability" in t and "quer" in s:
        return "Handling growing query load = scalability NFR." if key == correct else "Maintainability, portability, reliability address different qualities."
    if "recoverable" in s and "schedule" in s:
        return "Non-recoverable schedule: reads uncommitted data that may be rolled back." if key == correct else "Recoverable schedules only read after commit."
    return None


def _explain_network(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "ipv6" in s and "bit" in s:
        if "128" in t:
            return "IPv6 addresses are 128 bits." if key == correct else "IPv4 is 32 bits; IPv6 is 128 bits."
    if "transport layer" in s:
        if "process" in t and "address" in t:
            return "Transport layer uses port numbers for process-to-process addressing." if key == correct else "Physical/MAC is layer 2; network is IP; host addressing is vague."
    if "encryption" in s and "decryption" in s and "layer" in s:
        if "presentation" in t:
            return "Presentation layer handles encryption, compression, encoding (SSL/TLS historically here in OSI model)." if key == correct else "Network routes; transport segments; data link frames."
    if "denial of service" in s or "dos" in s:
        if "availability" in t:
            return "DoS floods resources so legitimate users cannot access the service — attacks availability." if key == correct else "Confidentiality and integrity are not the primary DoS target."
    if "multiplex" in t:
        return "Multiplexing: multiple signals/channels on one medium." if key == correct else "Switching routes; segmentation splits data differently."
    return None


def _explain_security(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "threat" in s and "potential" in t:
        return "Threat = potential danger to assets (not yet realized)." if key == correct else "Vulnerability is weakness; attack is action; threat is potential."
    if "vulnerabilit" in t and ("absence" in s or "weakness" in s):
        return "Vulnerability = weakness that can be exploited." if key == correct else "Threat is potential harm; attack is exploitation attempt."
    if "biometric" in t:
        return "Fingerprint, iris, palm scans are biometric authentication." if key == correct else "2FA, SSO, strong auth are broader categories."
    if "sql injection" in s:
        if "escape" in t or "parameter" in t:
            return "Escaping/parameterized queries prevent SQL injection by separating code from data." if key == correct else "Merging tables or interrupting requests do not prevent injection."
    if "xss" in s:
        if "escape" in t and "input" in t:
            return "Escaping/sanitizing user input prevents XSS script injection." if key == correct else "Avoiding all JavaScript is impractical; education alone is insufficient."
    return None


def _explain_pm(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "wbs" in t and ("work package" in s or "work to accomplish" in s):
        return "WBS decomposes project into work packages — lowest schedulable units." if key == correct else "Scope statement is high-level; activity list is schedule; scope plan is process."
    if "pert" in s and "review" in t:
        return "PERT = Program Evaluation and Review Technique." if key == correct else "Not the standard expansion of PERT."
    if "rad" in s and "rapid" in t:
        return "RAD = Rapid Application Development." if key == correct else "Not the standard RAD acronym."
    if "spiral" in t and "evolutionary" in s:
        return "Spiral is an evolutionary risk-driven model." if key == correct else "Incremental/concurrent are evolutionary; check 'does NOT relate' wording."
    if "agile manifesto" in s and "contract" in t:
        return "Manifesto values customer collaboration OVER contract negotiation — stating the reverse is incorrect." if key == correct else "This statement aligns with the manifesto."
    if "critical path" in s or "pert" in s:
        pass
    if "smoke test" in t:
        return "Smoke testing: shallow pass to see if build is stable enough for further testing." if key == correct else "Regression retests after changes; integration combines modules."
    return None


def _explain_architecture(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "reference model" in t:
        return "Reference model: abstract elements and relationships for a domain (e.g. OSI)." if key == correct else "Reference architecture is concrete; pattern is reusable solution."
    if "quality scenario" in t:
        return "Quality scenarios drive ATAM qualitative analysis." if key == correct else "Team size and logs are not architecture evaluation artifacts."
    if "coupling" in t and "quantitative" in s:
        return "High coupling = many dependencies between components — measurable architecture smell." if key == correct else "Comment count is not a structural architecture metric."
    return None


def _explain_testing(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "boundary value" in s:
        if "black" in t:
            return "Boundary Value Analysis is a black-box technique — tests edges of input partitions without seeing code." if key == correct else "White-box requires source code access."
    if "equivalence partition" in s:
        if "black box" in t and "all levels" in t:
            return "EP divides inputs into partitions; black-box technique usable at multiple test levels." if key == correct else "EP is not white-box or developer-only."
    if "decision coverage" in s and "outcome" in t:
        return "Decision coverage = (executed decision outcomes / total decision outcomes) × 100." if key == correct else "Wrong formula — uses decision outcomes, not loops alone."
    if "test planning" in s and "approach" in t:
        return "Test planning defines WHAT to test and HOW (strategy, scope, resources)." if key == correct else "Measuring results and writing specs come after planning."
    return None


def _explain_ai(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "informed search" in t or ("promising" in s and "first" in s):
        return "Informed search uses heuristics to explore most promising paths first (A*, greedy best-first)." if key == correct else "BFS/DFS/blind search do not use heuristics to prioritize."
    if "supervised" in t:
        return "Supervised learning uses labeled training data." if key == correct else "Unsupervised finds patterns without labels."
    if "data mining" in t and ("predict" in s or "trend" in s):
        return "Data mining discovers patterns and predicts trends from large datasets." if key == correct else "Metadata describes data; warehouse stores; datamart is subset."
    if "knowledge representation" in s:
        if "storage" in t and "computer" in t:
            return "KR = methods to represent knowledge in machine-processable form." if key == correct else "Inference methods or syntax alone are partial views."
    return None


def _explain_android(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "manifest" in s:
        if "all" in t and "information" in t:
            return "AndroidManifest.xml declares app components, permissions, version — complete app metadata." if key == correct else "Manifest covers more than just layouts or activities alone."
    if "res/layout" in t or "/res/layout" in t:
        return "XML layouts live in res/layout/." if key == correct else "Values in res/values; code in src; assets in assets/."
    if "onclick" in t and "button" in s:
        return "onClick listener handles button click events." if key == correct else "onCreate initializes activity; onCreate is not click handler."
    if "linux" in t and "kernal" in s:
        return "Android kernel is based on Linux." if key == correct else "Android is not Windows or macOS kernel."
    if "service" in s and "lifecycle" in s:
        if "oncreate" in t and "startcommand" in t:
            return "Service lifecycle: onCreate → onStartCommand → onDestroy." if key == correct else "Activity lifecycle or broadcast methods differ."
    return None


def _explain_os(stem: str, key: str, text: str, correct: str, opts: dict[str, str] | None = None) -> str | None:
    s, t = _norm(stem), _norm(text)
    if "pthread_exit" in s:
        if "void pthread_exit" in t or "void *" in t:
            return "pthread_exit(void *retval) terminates calling thread and optionally returns value." if key == correct else "Wrong signature — thread exit takes optional void* pointer."
    if "times()" in s or "tms" in s:
        if "cutime" in t or "utime" in t:
            return "tms struct fields: tms_utime (user), tms_stime (system), tms_cutime, tms_cstime for children." if key == correct else "Misspelled or wrong field name."
    if "close(" in s and "file" in s:
        if "null" in t and "error" in t:
            return "close() returns -1 on error, 0 on success — NOT NULL. NULL is for pointers, not file descriptor close." if key == correct else "close uses integer return codes."
    return None


EXPLAINERS = [
    _explain_complexity_option,
    _explain_ds_structure,
    _explain_web,
    _explain_java_oop,
    _explain_db,
    _explain_network,
    _explain_security,
    _explain_pm,
    _explain_architecture,
    _explain_testing,
    _explain_ai,
    _explain_android,
    _explain_os,
]


def build_deep_entry(q: dict) -> dict[str, Any]:
    num = q.get("examNumber")
    correct = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}

    if num in CURATED:
        base = CURATED[num]
        options_out = {}
        for k in "ABCD":
            text = opts.get(k, "(option unclear in OCR)")
            body = base["options"].get(k)
            if not body:
                body = (
                    explain_correct_option(q, text)
                    if k == correct
                    else explain_wrong_option(q, k, text)
                )
            options_out[k] = _opt(correct, k, text, body)
        return {
            "overview": base["overview"],
            "options": options_out,
            "studyTip": base["studyTip"],
        }

    options_out: dict[str, str] = {}
    for key in "ABCD":
        text = opts.get(key, "(option unclear in OCR)")
        if key == correct:
            body = explain_correct_option(q, text)
        else:
            body = explain_wrong_option(q, key, text)
        options_out[key] = _opt(correct, key, text, body)

    tips = {
        "Data Structures": "For complexity: write each term, circle the fastest-growing one, drop constants.",
        "Java / OOP": "Ask: compile-time or runtime? Constructor or method? Interface or class?",
        "C++": "Trace code with references (&), pointers (*), and pass-by-value.",
        "Web Development": "HTML = structure, CSS = style, JS = behavior, HTTP = transport.",
        "Database": "Transaction anomalies: dirty read, lost update, unrepeatable read, phantom.",
        "Networking": "Memorize OSI layer responsibilities and IPv4 vs IPv6 bit lengths.",
        "Security": "Threat vs vulnerability vs attack — three different words, three meanings.",
        "Software Architecture": "Quality attributes + tradeoffs + quality scenarios for ATAM.",
        "Project Management": "WBS = work packages. PERT = Review Technique. RAD = Rapid Application Development.",
        "Software Testing": "Black-box: EP, BVA. White-box: statement, branch, path coverage.",
        "AI / ML": "Supervised = labeled data. Informed search = uses heuristics.",
        "Android": "Manifest = app metadata. Layouts in res/layout. onClick = button handler.",
        "Operating Systems": "Threads: pthread_exit(void*). Files: close returns 0/-1, not NULL.",
    }

    return {
        "overview": build_overview(q),
        "options": options_out,
        "studyTip": tips.get(q.get("topic", ""), f"Study the core concept in this {q.get('topic', 'General')} question and redo it in Review mode."),
    }


_build_curated()
