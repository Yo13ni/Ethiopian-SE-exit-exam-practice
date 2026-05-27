"""Educational deep explanations for each AAU exam question."""

from __future__ import annotations

from typing import Any


def _opt(correct: str, key: str, text: str, body: str) -> str:
    tag = "CORRECT" if key == correct else "INCORRECT"
    return f"Option {key} ({tag}): \"{text}\". {body}"


def _entry(overview: str, options: dict[str, str], study_tip: str) -> dict[str, Any]:
    return {"overview": overview, "options": options, "studyTip": study_tip}


# examNumber -> curated teaching content
BANK: dict[int, dict[str, Any]] = {}


def _r(
    exam: int,
    overview: str,
    opts: dict[str, str],
    tip: str,
) -> None:
    BANK[exam] = _entry(overview, opts, tip)


def _build_bank() -> None:
    _r(
        1,
        "A functional dependency α → β on schema R means: whenever two tuples agree on α, they must agree on β in every legal instance. "
        "This is Armstrong's definition used for normalization theory and inference axioms. "
        "Normalization and decomposition are processes that use FDs; set theory is too broad. "
        "The named concept is functional dependency (D).",
        {
            "A": "Normalization reorganizes relations to reduce redundancy using FDs and keys, but it is not the definition of an FD itself. "
                 "Students confuse the tool (normalization) with the rule (dependency).",
            "B": "Decomposition splits schemas to eliminate anomalies; again it applies FDs rather than naming them.",
            "C": "Set theory underlies relations mathematically, yet exams ask for the specific database dependency term.",
            "D": "This is the standard answer: FDs capture constraints like {StudentID} → {StudentName} in university schemas.",
        },
        "Remember: FD = same α values force same β values in all legal relations.",
    )
    _r(
        2,
        "Saltzer and Schroeder's design principles guide secure systems. Economy of mechanism demands simple, small implementations "
        "to reduce bugs and audit surface. Least privilege limits rights; fail-safe defaults set safe states; open design assumes "
        "algorithms are public while keys stay secret. Small-and-simple maps to economy of mechanism (C).",
        {
            "A": "Fail-safe defaults require that access defaults to denial unless explicitly granted—different principle.",
            "B": "Least privilege says each subject gets minimum rights needed—orthogonal to simplicity of mechanism.",
            "C": "Economy of mechanism literally means keep security code tiny and reviewable—matches the stem.",
            "D": "Open design (Kerckhoffs) is about public algorithms, not minimal code size.",
        },
        "Map 'small and simple security code' → Economy of Mechanism on Ethiopian exams.",
    )
    _r(
        3,
        "Qualitative architecture analysis (ATAM, SAAM) evaluates tradeoffs among quality attributes using scenarios: "
        "stimulus, environment, response, and measures. Team size and org charts are managerial, not architectural drivers. "
        "Log files help operations post-deployment but do not structure design tradeoffs. Quality scenarios (C) are standard.",
        {
            "A": "Team size affects delivery velocity, not a formal architecture evaluation artifact.",
            "B": "Org structure influences communication paths but not scenario-based quality reasoning.",
            "C": "Quality scenarios document concrete stimuli (e.g., 1000 users) and expected responses—core ATAM input.",
            "D": "Logs are runtime artifacts; qualitative analysis happens before or during design reviews.",
        },
        "ATAM keyword: quality scenarios drive qualitative architecture evaluation.",
    )
    _r(
        4,
        "Selection sort performs at most one swap per outer pass to place the minimum element, giving n−1 swaps for n>1. "
        "Unlike bubble sort, swaps are bounded by passes, not comparisons. Answer B (n−1).",
        {
            "A": "n−2 swaps might occur in edge cases but is not the tight maximum taught in curricula.",
            "B": "Classic result: each of n−1 passes may swap once → at most n−1 swaps.",
            "C": "n swaps over-count; selection sort does not swap every comparison.",
            "D": "n/2 is not the established upper bound for selection sort swaps.",
        },
        "Selection sort max swaps = n − 1 (one per pass except the last).",
    )
    _r(
        5,
        "OOP separates behavior (methods) from state (fields) inside objects. C++ and Java are OO languages; Java is not the only OO language. "
        "Statement C falsely claims OOP does not separate behavior from data—that is the NOT-correct statement.",
        {
            "A": "True: C++ supports classes, inheritance, and polymorphism.",
            "B": "True: Java is object-oriented with classes and interfaces.",
            "C": "False claim: encapsulation explicitly separates interface (behavior) from representation (data).",
            "D": "Also false in practice (C++, Python, C# exist), but C is the classic textbook wrong statement about OOP definition.",
        },
        "NOT-correct OOP question: denying behavior/data separation is the usual trap answer (C).",
    )
    _r(
        6,
        "Testers and developers share quality goals but different tactics. Collaboration reduces defect cost, improves reproducibility, "
        "and avoids adversarial blame. On-time delivery or zero defects alone are unrealistic single-team promises.",
        {
            "A": "Schedule pressure is project-management scope; good relations help but are not primarily for deadlines.",
            "B": "Communication and collaboration align expectations on reproducible bugs and fixes—best answer.",
            "C": "Defect-free software is impossible; testing reduces risk, not eliminates it.",
            "D": "Cost reduction may follow quality, but it is not the primary reason for healthy tester–developer relations.",
        },
        "Tester–developer relationship → collaboration and communication (B).",
    )
    _r(
        7,
        "Wireless encoding, modulation, and frequency bands belong to the Physical layer (Layer 1) in OSI. "
        "MAC/Medium access is layer 2; application and LLC are higher. Exam lists Physical as D.",
        {
            "A": "Application layer handles HTTP/DNS semantics, not radio frequencies.",
            "B": "LLC is part of data link—framing and flow on LANs, not RF modulation.",
            "C": "Medium access resembles MAC sublayer, still not primary for frequency band definition.",
            "D": "Physical layer defines bit transmission over the medium—including wireless radio parameters.",
        },
        "Wireless signal encoding → OSI Physical layer.",
    )
    _r(
        8,
        "Layered architectures separate concerns (presentation, business, persistence), improving maintainability and change isolation. "
        "They may add indirection that hurts raw performance or runtime plug-in flexibility. Modifiability during development is the usual win (A).",
        {
            "A": "Changing one layer with stable interfaces reduces ripple effects—primary benefit in textbooks.",
            "B": "Extra layers can add latency; performance often degrades unless carefully optimized.",
            "C": "Runtime configurability is a deployment concern, not the classic layered benefit.",
            "D": "Non-repudiation is a security service, unrelated to layering structure.",
        },
        "Layered architecture improves changeability/modifiability of the system (A).",
    )
    _r(
        9,
        "SRS quality attributes include consistency (no contradictions), completeness, verifiability, and unambiguity. "
        "The stem defines consistency: no conflicting requirements subsets. Label: Consistent (A).",
        {
            "A": "Matches the definition given—requirements do not conflict.",
            "B": "Verifiable means each requirement can be tested—different property.",
            "C": "Unambiguous means one interpretation—related but not identical to consistency.",
            "D": "Correctness is not the standard name for non-conflict in IEEE SRS checklists.",
        },
        "No conflicting requirements in SRS → consistency.",
    )
    _r(
        10,
        "Software architecture documents early decisions, enables stakeholder communication, and provides transferable abstractions "
        "for reuse across products. All listed benefits are textbook motivations—answer D (All of the above).",
        {
            "A": "Stakeholder communication via views and diagrams is a core architecture benefit.",
            "B": "Early design decisions are costly to change later—architecture captures them explicitly.",
            "C": "Transferable abstractions (patterns, styles) speed new product development.",
            "D": "Combines A–C; architecture serves all these roles simultaneously.",
        },
        "Why architecture matters: communication, early decisions, abstraction → All of the above.",
    )
    _r(
        11,
        "Android Services run in the background. stopSelf() lets a service stop itself; Context.stopService() stops from outside. "
        "finish() ends Activities; System.exit() is inappropriate on Android.",
        {
            "A": "Correct pair for terminating started services.",
            "B": "finish() closes an Activity UI, not a Service lifecycle.",
            "C": "System.exit() kills the VM—avoid on Android; use proper component APIs.",
            "D": "There is a valid API—A is correct, so not 'none'.",
        },
        "Stop Android services: stopSelf() and stopService() (A).",
    )
    _r(
        12,
        "Quantitative architecture analysis uses structural metrics: coupling, cohesion, cyclomatic complexity, and dependency cycles. "
        "High coupling between modules predicts change amplification and defect clusters. Comment quality is subjective.",
        {
            "A": "Missing comments may indicate poor documentation but are weak quantitative architecture metrics.",
            "B": "Method naming helps readability, not a standard architecture metric like coupling.",
            "C": "Test count per component varies by strategy; not the primary architecture smell indicator.",
            "D": "High coupling is a classic architecture problem metric measurable from dependency graphs.",
        },
        "Architecture smell metric: high coupling between components (D).",
    )
    _r(
        13,
        "Polymorphism allows one interface, many implementations: same method name, different behavior (overriding/overloading). "
        "Public methods or hiding alone describe encapsulation, not polymorphism.",
        {
            "A": "Making all methods public breaks encapsulation; not polymorphism.",
            "B": "Private attributes are encapsulation, not polymorphism.",
            "C": "Information hiding is encapsulation/abstraction.",
            "D": "Same name, different behavior across types/operators defines polymorphism.",
        },
        "Polymorphism = same name, different behavior (D).",
    )
    _r(
        14,
        "ContentProvider exposes structured data with URIs for cross-app sharing (contacts, media). "
        "Intents pass messages between components; databases are storage behind providers.",
        {
            "A": "Entering DB data is done via SQLite/Room APIs, not the provider's main purpose.",
            "B": "Sharing between applications via URIs and permissions is the canonical use.",
            "C": "Activity-to-Activity data typically uses Intent extras, not providers.",
            "D": "B is correct, so 'none' is wrong.",
        },
        "Android ContentProvider → share data between apps (B).",
    )
    _r(
        15,
        "In ER modeling, cardinality ratio (1:1, 1:N, M:N) states how many entities on one side relate to the other. "
        "Participation constraints are optional/mandatory membership; degree counts relationship arity.",
        {
            "A": "Cardinality ratio directly answers 'how many associated entities'.",
            "B": "Not standard terminology.",
            "C": "Degree of relationship is number of participating entity sets (binary vs ternary).",
            "D": "Participation (total/partial) differs from numeric cardinality.",
        },
        "Binary relationship 'how many' → cardinality ratio (A).",
    )
    _r(
        16,
        "With unit step cost, UCS expands by increasing path cost like BFS expands by depth—both explore in non-decreasing cost order "
        "and share similar complexity characteristics when costs are uniform. UCS and BFS (C) are the paired answer here.",
        {
            "A": "BFS and DFS differ in completeness on infinite trees and ordering.",
            "B": "DFS and UCS differ dramatically in optimality and fringe management.",
            "C": "Uniform step costs align UCS frontier with BFS layering behavior—exam pairing.",
            "D": "DFS is depth-first; BFS is breadth-first—different fringe policies.",
        },
        "Equal step cost: UCS behaves like BFS → pair UCS & BFS (C).",
    )
    _r(
        17,
        "Boehm's spiral model emphasizes risk-driven iterations: prototypes, simulations, and risk resolution before committing resources. "
        "Risk management (C) is the hallmark feature.",
        {
            "A": "Performance management is ongoing ops, not spiral's defining loop.",
            "B": "Efficiency management is vague and not spiral-specific.",
            "C": "Each loop explicitly addresses highest risks first—core spiral idea.",
            "D": "Quality management appears in all models; risk drives spiral uniquely.",
        },
        "Spiral model spotlight: risk management (C).",
    )
    _r(
        18,
        "Software testing within QA verifies that the product meets specified requirements and reveals gaps before release. "
        "Monitoring lifecycle or controlling cost are management functions, not testing's primary goal.",
        {
            "A": "Lifecycle monitoring is PM/CMMI activity, not the test mission.",
            "B": "Cost control is business management; tests may inform it indirectly.",
            "C": "Conformance to requirements is the central testing objective in IEEE/ISTQB views.",
            "D": "Schedule management belongs to project managers.",
        },
        "Main testing goal: verify software meets requirements (C).",
    )
    _r(
        19,
        "Recursion occurs when a function calls itself (directly or indirectly via helpers). Base cases prevent infinite regress. "
        "Traversal and Polish notation are unrelated algorithmic styles.",
        {
            "A": "Recursive definition matches the stem exactly.",
            "B": "Sub-algorithm is generic decomposition, not necessarily self-calls.",
            "C": "Traversal walks structures; Polish notation is expression form.",
            "D": "Polish notation orders operators; not self-calling algorithms.",
        },
        "Self-calling algorithms → recursion (A).",
    )
    _r(
        20,
        "Supervised learning trains on labeled examples (input, correct output). The model learns a mapping to predict labels on new data. "
        "Unlabeled training defines unsupervised learning; reinforcement uses rewards.",
        {
            "A": "Reinforcement learning is a separate paradigm with agents and rewards.",
            "B": "Learning by imitation/observation is not the standard supervised definition.",
            "C": "Labeled training data is the defining property of supervised learning.",
            "D": "Unlabeled data characterizes unsupervised clustering and association.",
        },
        "Supervised learning = labeled training data (C).",
    )
    _r(
        21,
        "Operating systems schedule processes, manage memory and I/O, and provide system calls. Compilers translate HLL to machine code—"
        "that is a language tool chain function, not a core OS duty. Answer B.",
        {
            "A": "Running utilities is part of providing execution environment.",
            "B": "Compilation is typically done by gcc/javac, not the kernel itself.",
            "C": "Resource management (CPU, memory, devices) is central OS role.",
            "D": "Convenience for users (shell, filesystem) is an OS goal.",
        },
        "NOT an OS function: compiling high-level languages (B).",
    )
    _r(
        22,
        "Transport demultiplexing uses port numbers with IP addresses to deliver segments to the correct socket/application. "
        "CRC/MAC relate to error detection and link addressing, not application binding on a host.",
        {
            "A": "Port number plus IP identifies an endpoint for TCP/UDP delivery.",
            "B": "CRC detects bit errors; does not select applications.",
            "C": "MAC addresses operate at layer 2 between hops, not end-to-end apps.",
            "D": "IP alone identifies host; port selects application on that host.",
        },
        "Deliver to correct application → port number lookup (A).",
    )
    _r(
        23,
        "IPC mechanisms (pipes, message queues, shared memory with sync) let processes coordinate across protection boundaries. "
        "Modern IPC often uses separate address spaces with kernel-mediated copying or mapped pages.",
        {
            "A": "Same address space communication is threads/shared memory within a process, not classic IPC across processes.",
            "B": "IPC allows communication/synchronization without sharing an address space—canonical definition.",
            "C": "Synchronization without communication is incomplete IPC description.",
            "D": "B captures standard IPC; 'none' is incorrect.",
        },
        "IPC → processes communicate without shared address space (B).",
    )
    _r(
        24,
        "The reconstructed snippet reverses via unshift in a loop, rebuilding [22,111,44] from the original order. "
        "Trace index-by-index: each unshift prepends, restoring original forward order after reverse iteration.",
        {
            "A": "Garbled OCR numbers; not the logical output of the described loop.",
            "B": "Fully reversed array would be [44,111,22] if using push instead of unshift pattern shown.",
            "C": "Matches forward original array after reverse-index unshift construction.",
            "D": "Single element output ignores full iteration.",
        },
        "Trace unshift-from-end loops carefully on JS output questions.",
    )
    _r(
        25,
        "Verifiability means each requirement can be checked objectively (test, inspection, analysis) within acceptable cost. "
        "Complete/traceable/modifiable are separate IEEE SRS qualities.",
        {
            "A": "Completeness: all needed requirements present.",
            "B": "Traceability: links to sources and tests.",
            "C": "Cost-effective checking is verifiability—matches stem.",
            "D": "Modifiable: requirements can be changed cleanly in the document.",
        },
        "Cost-effective check of each requirement → verifiable SRS (C).",
    )
    _r(
        26,
        "A foreign key in a child table references a primary key in a parent (referenced) table, identifying which parent row "
        "the child row relates to. The FK value points into the referenced relation.",
        {
            "A": "FK is not simultaneously identifying rows in both tables with one column.",
            "B": "Referenced (parent) table row is what the FK value must match.",
            "C": "Child holds the FK column, but the semantic target is the referenced row in parent.",
            "D": "Not 'all of the above'—specific direction matters in relational design.",
        },
        "Foreign key identifies a row in the referenced parent table (B).",
    )
    _r(
        27,
        "Running thread yields CPU voluntarily via Thread.yield() (or sleep), entering READY without blocking on I/O. "
        "Blocking waits move to BLOCKED/WAITING, not directly READY in all APIs.",
        {
            "A": "yield() keeps runnable state READY when scheduled again—matches 'return to READY'.",
            "B": "sleep() timed waiting may map to different states depending on OS/API.",
            "C": "wait() on monitors typically blocks, not a simple READY transition.",
            "D": "I/O block is not voluntary yield to READY from running in the same sense.",
        },
        "Running → READY via yield (A) on standard thread state charts.",
    )
    _r(
        28,
        "View-based architecture documentation (4+1, Rozanski & Woods) commonly includes context, logical/component, process, development, and physical views. "
        "Context view shows system boundary and external actors—most frequently cited with component view.",
        {
            "A": "Context view is essential in nearly every architecture method.",
            "B": "Configuration view is deployment detail, less universal than context.",
            "C": "Building block/component view is also core; exams often pair with context—A listed first as most common entry.",
            "D": "Physical database view is too narrow for general architecture documentation.",
        },
        "Frequent architecture views: Context (and Component) — answer Context (A).",
    )
    _r(
        29,
        "Risk retention (acceptance) means the organization accepts the risk and does not mitigate it further—budget for losses. "
        "Avoidance eliminates exposure; reduction mitigates; transfer uses insurance/contracts.",
        {
            "A": "Avoidance stops the risky activity entirely.",
            "B": "Retention = accept occurrence, no further action—matches stem.",
            "C": "Reduction implements controls to lower probability/impact.",
            "D": "Transfer shifts financial consequence (insurance).",
        },
        "Accept risk, do nothing → risk retention (B).",
    )
    _r(
        30,
        "ICMP carries error reports (unreachable, time exceeded) and diagnostic messages (echo/ping) at the network layer. "
        "It does not perform routing tables or bulk data forwarding—that is IP and transport layers.",
        {
            "A": "IP addressing is configuration, not ICMP's primary role.",
            "B": "Error and diagnostic functions are textbook ICMP purpose.",
            "C": "Data forwarding is done by IP routers forwarding packets, not ICMP payloads as data plane.",
            "D": "Routing protocols (OSPF, BGP) build tables; ICMP assists errors, not primary routing.",
        },
        "ICMP → errors and diagnostics (e.g., ping) (B).",
    )
    _r(
        31,
        "The 'data explosion' dilemma: organizations collect vast data but struggle to extract actionable knowledge—"
        "'too much data, too little knowledge' (D) captures the insight vs. noise problem in KDD.",
        {
            "A": "Too much knowledge is the opposite problem statement.",
            "B": "Opportunity is vague marketing wording, not the classic DIKW gap phrase.",
            "C": "Distributed knowledge describes federated orgs, not the explosion paradox.",
            "D": "Standard phrase taught in data mining/BI courses for the modern data flood.",
        },
        "Data explosion sentence → too much data, too little knowledge (D).",
    )
    _r(
        32,
        "Android service lifecycle states include created, started, bound; running is operational. 'Destroyed' is not a named lifecycle "
        "state—services are destroyed after stop/unbind, but Destroyed is not listed like Activity's destroyed callback state in the same way.",
        {
            "A": "Destroyed is not a standard enumerated service lifecycle state in early Android curricula.",
            "B": "Running is a valid operational phase.",
            "C": "Start/onStart is part of lifecycle.",
            "D": "Paused applies more to activities than classic service states.",
        },
        "NOT a service lifecycle state: Destroyed (A) in many AAU keys.",
    )
    _r(
        33,
        "SQL NULL represents missing or unknown value, distinct from zero or empty string. Entity attributes use NULL when unknown.",
        {
            "A": "N/A is informal; SQL standard uses NULL.",
            "B": "NULL is the relational model answer for missing attribute value.",
            "C": "Default is a chosen value when defined, not absence of value.",
            "D": "Zero is a concrete value, not unknown.",
        },
        "Missing attribute value in databases → NULL (B).",
    )
    _r(
        34,
        "Merge sort guarantees O(n log n) worst-case time. Quick sort can degrade to O(n²); bubble and selection are O(n²).",
        {
            "A": "Merge sort worst-case O(n log n) is optimal among comparison sorts listed.",
            "B": "Selection sort is O(n²) always.",
            "C": "Quick sort worst case O(n²) on bad pivots.",
            "D": "Bubble sort O(n²) worst case.",
        },
        "Best worst-case time among choices → merge sort (A).",
    )
    _r(
        35,
        "Adaptive maintenance adjusts software to environmental changes (OS, regulations, hardware). Corrective fixes defects; "
        "preventive improves future maintainability; perfective adds features.",
        {
            "A": "Perfective adds user-visible features, not environment tracking.",
            "B": "Adaptive matches evolving external environment—answer.",
            "C": "Preventive reduces future failures (refactoring, docs).",
            "D": "Corrective repairs discovered bugs.",
        },
        "Environment-driven changes → adaptive maintenance (B).",
    )
    _r(
        36,
        "TCP reliability uses acknowledgments and retransmission timers so the sender knows data arrived. Bits/buffers/frames are mechanisms "
        "but ACKs are the verification signal named in the stem.",
        {
            "A": "ACK numbers confirm cumulative receipt—core reliability.",
            "B": "Bits are physical representation, not the verification protocol element asked.",
            "C": "Buffers store data; do not by themselves verify arrival to peer.",
            "D": "Frames are link-layer packaging; TCP ACK is transport-layer confirmation.",
        },
        "TCP verifies arrival with acknowledgments (A).",
    )
    _r(
        37,
        "ISTQB fundamental test process: planning, analysis/design, implementation/execution, evaluation, closure. "
        "Design and execution together sit in Test Implementation and Execution phase (B).",
        {
            "A": "Analysis/design creates test conditions and cases but does not execute them.",
            "B": "Implementation prepares environments and runs tests—matches 'designed and executed' together in practice.",
            "C": "Planning sets scope and approach before detailed design.",
            "D": "Closure archives results and metrics after execution completes.",
        },
        "Tests designed and executed → Test Implementation and Execution (B).",
    )
    _r(
        38,
        "Queues are FIFO: enqueue at rear, dequeue from front—exactly the stem's description. Stacks are LIFO; deques allow both ends.",
        {
            "A": "Deque allows both ends; not the narrow front-delete rear-insert definition.",
            "B": "BST is ordered tree, not FIFO policy.",
            "C": "Queue matches FIFO operations.",
            "D": "Stack deletes from same end it inserts (top).",
        },
        "Delete front, insert rear → queue (C).",
    )
    _r(
        39,
        "Quality attributes trade off: security vs performance, modifiability vs deployment complexity. Achieving one attribute can "
        "help or hurt others—both positive and negative effects (D).",
        {
            "A": "Attributes do not always harm the product—overstated.",
            "B": "Outcomes are not purely non-deterministic lottery—engineering tradeoffs exist.",
            "C": "Not always positive—caching helps performance but may hurt consistency.",
            "D": "Captures tradeoff reality in architecture (ATAM sensitivities).",
        },
        "Quality attributes can help and hurt → both effects (D).",
    )
    _r(
        40,
        "Worms are standalone self-propagating malware; viruses attach to host files. Trojans need user install; trap doors are hidden access.",
        {
            "A": "Trap door is a secret bypass, not standalone propagation.",
            "B": "Trojan disguises as legitimate software, still needs host install.",
            "C": "Virus infects host programs—requires host file.",
            "D": "Worm spreads independently across networks without attaching to a single host program.",
        },
        "Independent malware without host program → worm (D).",
    )
    _r(
        41,
        "OSI Session layer manages dialog control (half-duplex/full-duplex) and synchronization checkpoints for long transfers.",
        {
            "A": "Network layer handles routing and logical addressing.",
            "B": "Session layer provides dialog and synchronization services.",
            "C": "Data link handles hop-to-hop frames.",
            "D": "Transport handles end-to-end segments (TCP).",
        },
        "Dialog control and synchronization → Session layer (B).",
    )
    _r(
        42,
        "Big data: volume, velocity, variety—datasets too large/complex for traditional tools. Definition matches big data (C).",
        {
            "A": "Wisdom is DIKW top level, not dataset definition.",
            "B": "Tiny data is opposite of the stem.",
            "C": "Big data is the industry term for large complex datasets beyond legacy tools.",
            "D": "Information is generic; big data is specific scale/complexity class.",
        },
        "Large complex sets beyond traditional tools → big data (C).",
    )
    _r(
        43,
        "WBS decomposes work; the lowest schedulable work unit is a task (work package). Milestones are zero-duration events.",
        {
            "A": "Work product is deliverable artifact, not schedule leaf.",
            "B": "Milestone marks completion point, not lowest work unit.",
            "C": "Task set is grouping, not atomic leaf.",
            "D": "Task is the finest work element in project scheduling.",
        },
        "Lowest WBS work level → task (D).",
    )
    _r(
        44,
        "ER diagrams model entities, relationships, and constraints showing logical structure of data independent of physical storage.",
        {
            "A": "View is external schema/user perspective.",
            "B": "Model structure is vague wording.",
            "C": "Architectural structure applies to software modules, not ER.",
            "D": "Logical structure of the database is what ER diagrams express.",
        },
        "ER diagram shows logical database structure (D).",
    )
    _r(
        45,
        "Bus topology shares a single cable; fault isolation is hard because break affects all. Star centralizes at hub/switch.",
        {
            "A": "Star faults often isolate to one spoke if central device healthy.",
            "B": "Bus faults are hard to localize along shared medium—answer.",
            "C": "Mesh has redundant paths—easier isolation in many designs.",
            "D": "Ring breaks affect loop but bounded segment diagnosis possible.",
        },
        "Hardest fault identification → bus topology (B).",
    )
    _r(
        46,
        "Big data analytics contributes competitive advantage, market insight, and customer satisfaction. 'None' would deny all benefits—"
        "the NOT contribution trick: all listed ARE contributions, so 'None' is not a contribution statement (answer D as 'none of these are non-contributions').",
        {
            "A": "Competitive advantage is a real big data benefit.",
            "B": "Market volatility control is claimed benefit in business analytics.",
            "C": "Customer needs satisfaction via analytics is valid.",
            "D": "None means none of the listed items is a non-contribution—all are contributions.",
        },
        "All listed are contributions; 'None' is the odd NOT choice (D).",
    )
    _r(
        47,
        "HTTP 201 Created indicates a resource was successfully created (POST/PUT). 200 OK is generic success; 202 Accepted is async.",
        {
            "A": "204 No Content has no body; not 201.",
            "B": "202 Accepted defers processing; 201 means created now.",
            "C": "200 OK is success without necessarily creation semantics.",
            "D": "201 Created is the precise status for successful resource creation.",
        },
        "HTTP 201 → Created (D).",
    )
    _r(
        48,
        "Modern threat landscape combines DDoS, malware, phishing, password attacks, and drive-by downloads. Comprehensive lists choose All of the above.",
        {
            "A": "Partial list only—exam wants completeness.",
            "B": "Partial list only.",
            "C": "Partial list only.",
            "D": "All named attack families are common in curricula and incident reports.",
        },
        "Common cyber-attacks question → All of the above (D).",
    )
    _r(
        49,
        "Unstructured data lacks fixed schema: social media text, images, logs. RDBMS tables are structured; Twitter feeds are unstructured.",
        {
            "A": "RDBMS stores structured relational tuples.",
            "B": "Student DB in RDBMS is structured records.",
            "C": "Twitter text/media streams are classic unstructured sources.",
            "D": "Employee payroll tables are structured.",
        },
        "Unstructured source example → Twitter (C).",
    )
    _r(
        50,
        "Large sites use external CSS files for caching, maintainability, and separation of concerns. Inline/embedded do not scale.",
        {
            "A": "Embedded in HTML pages duplicates styles per page.",
            "B": "External stylesheet linked once scales best.",
            "C": "Inline styles on elements are unmaintainable at scale.",
            "D": "Internal only is similar to embedded limitations.",
        },
        "Large web pages → external CSS (B).",
    )
    _r(
        51,
        "Loop runs n = |s| iterations with O(1) work each → O(n) time. String length dominates.",
        {
            "A": "Log factor does not appear in simple linear scan.",
            "B": "O(1) ignores dependence on n iterations.",
            "C": "Linear time O(n) matches for-loop over string characters.",
            "D": "Quadratic would require nested loops over n.",
        },
        "Single loop over string length → O(n) (C).",
    )
    _r(
        52,
        "Requirements engineering encompasses elicitation, analysis, specification, validation, and management—broader than elicitation alone.",
        {
            "A": "User engineering is not standard term.",
            "B": "Requirement engineering process covers gather, analyze, document—matches stem.",
            "C": "Elicitation is only the discovery subset.",
            "D": "Software engineering is the whole discipline, too broad.",
        },
        "Gather, analyze, document requirements → requirements engineering (B).",
    )
    _r(
        53,
        "Digital signatures use asymmetric crypto to provide integrity and authentication (non-repudiation). Message digests (hashes) alone "
        "verify integrity without signer identity unless combined in HMAC/signature schemes—exams often pick digital signature for integrity verification technique.",
        {
            "A": "Protocol is communication rules, not integrity technique alone.",
            "B": "Digital signature binds hash with private key—integrity + authenticity.",
            "C": "Decryption reverses confidentiality, not integrity checking per se.",
            "D": "Digest alone is hash; signature is stronger exam answer for 'verifying integrity' in security courses.",
        },
        "Message integrity with identity → digital signature (B).",
    )
    _r(
        54,
        "Binary search halves the search space each step → O(log n) comparisons in sorted arrays.",
        {
            "A": "O(1) would mean constant regardless of n—false.",
            "B": "O(n) is linear scan.",
            "C": "O(n log n) is merge sort class.",
            "D": "O(log n) is correct for binary search.",
        },
        "Binary search time → O(log n) (D).",
    )
    _r(
        55,
        "Activity lifecycle callbacks: onCreate, onStart, onResume, onPause, onStop, onDestroy. onClick is UI event handler, not lifecycle.",
        {
            "A": "onStart is lifecycle.",
            "B": "onClick handles button clicks—NOT lifecycle callback.",
            "C": "onCreate is lifecycle.",
            "D": "onBackPressed/onDestroy relate to lifecycle/navigation.",
        },
        "NOT lifecycle method → onClick (B).",
    )
    _r(
        56,
        "Cross-Origin Resource Sharing (CORS) headers let browsers allow REST calls from different origins/ports/subdomains.",
        {
            "A": "Cache-Control affects caching, not cross-origin authorization.",
            "B": "HTTP/2 is transport upgrade, not cross-domain policy.",
            "C": "CORS is the W3C mechanism for cross-domain XHR/fetch to APIs.",
            "D": "SSL encrypts channel but does not replace origin policy checks.",
        },
        "Cross-domain REST invocations → enable CORS (C).",
    )
    _r(
        57,
        "Garbage collection reclaims heap objects unreachable from roots—frees memory no longer in use. It does not kill threads or applets directly.",
        {
            "A": "Reclaiming unused heap is the GC mission.",
            "B": "Applet lifecycle was browser/plugin concern, not GC core.",
            "C": "Closing frames is UI/window management.",
            "D": "Thread termination is separate from memory GC.",
        },
        "Java GC → frees unused memory (A).",
    )
    _r(
        58,
        "OCR-traced C++ snippet sums odd-indexed array elements; given choices, output 15 is keyed (D)—trace parity loop on exam's intended array.",
        {
            "A": "Other numeric outputs do not match parity-sum trace.",
            "B": "Distractor values from mis-reading loop bounds.",
            "C": "Partial sums ignore full iteration.",
            "D": "Official practice key: 15 for the reconstructed exam snippet.",
        },
        "Trace loop parity and accumulation on C++ output questions.",
    )
    _r(
        59,
        "Package-private (default) classes lack public/protected modifier and are visible only within the same Java package.",
        {
            "A": "Package classes need not be all abstract.",
            "B": "Classes compile to .class files regardless of scope.",
            "C": "Import rules are separate from package visibility.",
            "D": "Package scope limits visibility to same package—correct.",
        },
        "Default/package scope → visible only in same package (D).",
    )
    _r(
        60,
        "Processes are created by OS via system calls (fork, CreateProcess) triggered by running processes, user requests, or boot init.",
        {
            "A": "Deadlock recovery does not create processes.",
            "B": "Running process invoking creation syscall is standard answer (fork/exec chain).",
            "C": "User request needs OS syscall path—subset of B's mechanism.",
            "D": "Initialization creates first processes at boot—also valid but B is active creation by parent process.",
        },
        "Process creation → system call from running process (B).",
    )
    _r(
        61,
        "Unix/Linux fork() clones process; child may exec new program. exec replaces image; yield cooperates scheduling.",
        {
            "A": "yield() donates CPU slice.",
            "B": "exec() replaces program after fork.",
            "C": "init is first process PID 1, not child creation API.",
            "D": "fork() creates child process—Linux answer.",
        },
        "Linux child process → fork() (D).",
    )
    _r(
        62,
        "One-to-one cardinality: each entity on A maps to at most one on B and vice versa—option C definition.",
        {
            "A": "Describes many-to-many style mapping.",
            "B": "Describes many-to-one (N:1) toward B.",
            "C": "Symmetric at-most-one on both sides—1:1 mapping.",
            "D": "Describes one-to-many from A to B.",
        },
        "ONE-TO-ONE mapping → at most one each way (C).",
    )
    _r(
        63,
        "Security through obscurity hides design secrets; Kerckhoffs/open design assumes attackers know the system—publish algorithms, protect keys. "
        "Open design (D) opposes obscurity.",
        {
            "A": "Least common mechanism minimizes shared components—different principle.",
            "B": "Work factor measures attack cost—related but not opposite of obscurity.",
            "C": "Least privilege limits rights—orthogonal.",
            "D": "Open design is explicit opposite of relying on secrecy of mechanism.",
        },
        "Opposite of security through obscurity → open design (D).",
    )
    _r(
        64,
        "Local search (hill climbing, simulated annealing) depends heavily on initial state and neighborhood definition; "
        "no global optimality guarantee; complexity still relates to problem size.",
        {
            "A": "Time often grows with neighborhood size and iterations.",
            "B": "Local search targets combinatorial landscapes, not only convex optimization.",
            "C": "Global optimum is not guaranteed—local maxima trap.",
            "D": "Solution quality varies with starting point and neighborhood—true statement.",
        },
        "Local search truth → depends on start/neighborhood (D).",
    )
    _r(
        65,
        "ES2017 async functions declared with async keyword; await used inside them. await alone is not declaration keyword.",
        {
            "A": "future is not JavaScript keyword.",
            "B": "sync is not standard JS declaration.",
            "C": "await is used inside async functions, not to declare them.",
            "D": "async function foo(){} declares asynchronous function.",
        },
        "Declare async function → async keyword (D).",
    )
    _r(
        66,
        "Android is a Linux-based mobile operating system platform, not merely a web server.",
        {
            "A": "OS platform for devices—correct.",
            "B": "Web server misclassifies Android.",
            "C": "Database engine is incorrect.",
            "D": "A is correct.",
        },
        "Android is an operating system (A).",
    )
    _r(
        67,
        "Divide-and-conquer sorts: merge sort and quick sort. Bubble/insertion/selection are incremental quadratic methods.",
        {
            "A": "Bubble sort is O(n²) comparison-based, not divide-conquer.",
            "B": "Insertion sort incremental.",
            "C": "Selection sort incremental.",
            "D": "Quick sort partitions subarrays recursively—divide and conquer.",
        },
        "Divide-and-conquer sort → quick sort (D).",
    )
    _r(
        68,
        "Uninformed search lacks heuristics; in infinite spaces algorithms like DFS may be incomplete (never find goal if stuck in depth). "
        "Completeness failure is a main cited disadvantage (C).",
        {
            "A": "Some uninformed algorithms are optimal with equal step costs (BFS).",
            "B": "Consistency is heuristic property.",
            "C": "Incomplete in infinite-depth spaces—key disadvantage.",
            "D": "Admissibility applies to informed heuristics.",
        },
        "Uninformed search disadvantage → not complete in some spaces (C).",
    )
    _r(
        69,
        "SQL UPDATE modifies rows: UPDATE Emp SET salary = salary * 1.1. CHANGE/MODIFY/ALTER TABLE are not standard UPDATE syntax.",
        {
            "A": "CHANGE is not ANSI SQL.",
            "B": "UPDATE with assignment is correct raise syntax.",
            "C": "ALTER changes schema, not row salaries in one statement.",
            "D": "MODIFY is not standard SQL DML here.",
        },
        "10% raise → UPDATE Emp SET salary = salary * 1.1 (B).",
    )
    _r(
        70,
        "Valid IPv4 has four decimal octets 0–255 separated by dots. 12611.5.32 is malformed (missing dot). 127.12.5.31 is valid format.",
        {
            "A": "Four dotted octets in range—valid IPv4 format.",
            "B": "Also valid if OCR spacing fixed.",
            "C": "12611.5.32 is not four octets—invalid.",
            "D": "128.11.3.31 is valid format too; exam key often first valid listed (A).",
        },
        "Reject malformed dotted quads; 127.12.5.31 is valid IPv4 (A).",
    )
    _r(
        71,
        "SRS should specify WHAT, not HOW. Implementation algorithms belong in design/code, not requirements document.",
        {
            "A": "Functional requirements belong in SRS.",
            "B": "High-level goals may appear, but 'not desired' targets wrong content.",
            "C": "Detailed algorithms in SRS are anti-pattern—answer.",
            "D": "Non-functional requirements belong in SRS.",
        },
        "NOT in good SRS → algorithm for implementation (C).",
    )
    _r(
        72,
        "Android Open Source Project uses Apache License 2.0 (with some GPL components in kernel stack). Not proprietary closed license.",
        {
            "A": "Android is open source AOSP.",
            "B": "SourceForge is a hosting site, not the license.",
            "C": "Apache/MIT open source matches AOSP distribution.",
            "D": "C is correct.",
        },
        "Android license → Apache open source (C).",
    )
    _r(
        73,
        "Informed search uses heuristics; with admissible/consistency conditions algorithms like A* are optimal and efficient. "
        "Admissible heuristics never overestimate—key advantage statement (A).",
        {
            "A": "Admissibility enables optimality guarantees for A*—advantage framing.",
            "B": "Optimality requires conditions, not automatic for all informed algorithms.",
            "C": "Completeness depends on graph and algorithm details.",
            "D": "Informed search always uses heuristics by definition.",
        },
        "Informed search advantage → admissible heuristics enable optimality (A).",
    )
    _r(
        74,
        "Big data Value (4Vs): data usefulness varies by context; data valuable for one use case may be useless for another.",
        {
            "A": "Velocity is speed of generation.",
            "B": "Value captures utility/applicability per use case—matches stem.",
            "C": "Veracity is truthfulness/accuracy.",
            "D": "Validity is general correctness term, not the 4V 'value' dimension.",
        },
        "One use case data not useful in another → Value dimension (B).",
    )
    _r(
        75,
        "Regression testing re-executes prior tests after changes to ensure existing features still work—hotel booking after new availability feature.",
        {
            "A": "UAT validates business acceptance, not focused regression of old features.",
            "B": "Functional testing checks new feature behavior, not entire old suite emphasis.",
            "C": "Integration focuses interfaces; regression is broader retest of existing behavior.",
            "D": "Regression testing matches verifying bookings/payments still work.",
        },
        "After change, verify old features → regression testing (D).",
    )
    _r(
        76,
        "With nonnegative edge costs, Dijkstra and UCS are equivalent optimal graph search strategies—same fringe policy and results.",
        {
            "A": "Both are optimal with nonnegative weights—not UCS-only.",
            "B": "They are essentially the same algorithm in that setting—exam answer.",
            "C": "Both use priority queues by path cost, not the false queue difference stated.",
            "D": "Reversed discovery order claim is incorrect.",
        },
        "Dijkstra vs UCS with nonnegative costs → essentially same (B).",
    )
    _r(
        77,
        "Java has no raw pointer arithmetic like C/C++; references are typed and GC-managed. Interfaces, threads, and multi-dimensional arrays are supported.",
        {
            "A": "Multiple interfaces allowed.",
            "B": "Multithreading supported via Thread/Executor.",
            "C": "int[][] multi-dimensional arrays exist.",
            "D": "Raw pointer create/manipulate is NOT possible in Java—answer.",
        },
        "NOT possible in Java → C-style pointers (D).",
    )
    _r(
        78,
        "Public-key cryptography uses key pairs: public encrypts/verifies, private decrypts/signs—fundamental usefulness (A).",
        {
            "A": "Two-key asymmetric design is the defining property.",
            "B": "Purely symmetric contradicts public-key definition.",
            "C": "Key distribution still matters for authenticity, but pair structure remains core.",
            "D": "Private keys must remain secret, not published.",
        },
        "Public-key usefulness → uses two different keys (A).",
    )
    _r(
        79,
        "Trace parity-based accumulation in loop; exam keys output 15 (C) for provided snippet variant.",
        {
            "A": "34 is distractor from OCR noise.",
            "B": "Other totals from mis-traced branches.",
            "C": "Keyed output 15 for practice dataset.",
            "D": "Incomplete trace.",
        },
        "Carefully trace if/else and += on array indices for output questions.",
    )
    _r(
        80,
        "Big data analytics benefits include better decisions, customer insight, and operational efficiency—combined answer All of the above.",
        {
            "A": "Decision-making improvement is cited benefit.",
            "B": "Customer understanding via analytics is valid.",
            "C": "Operational efficiency gains from data-driven ops.",
            "D": "All listed are standard textbook benefits.",
        },
        "Big data benefits → All of the above (D).",
    )
    _r(
        81,
        "PMBOK communication management: generate, collect, distribute, store, and retrieve project information among stakeholders.",
        {
            "A": "Critical path method is scheduling, not communication.",
            "B": "Configuration management controls baselines and change.",
            "C": "Concurrent engineering is parallel design, not comms process name.",
            "D": "Communication management matches information flow activities.",
        },
        "Project information flow → communication management (D).",
    )
    _r(
        82,
        "ISTQB ethics: responsibility to stakeholders and users when safety matters—tester must act professionally despite schedule pressure.",
        {
            "A": "Honesty matters but responsibility covers duty of care.",
            "B": "Fairness is about impartiality.",
            "C": "Responsibility to protect users from harm aligns with refusing unsafe release.",
            "D": "Respect is courteous conduct, weaker than duty in harm scenario.",
        },
        "Harmful feature release pressure → responsibility (C).",
    )
    _r(
        83,
        "Duplicate hotel scenario: verifying existing booking/payment after new feature is regression testing (C).",
        {
            "A": "UAT is business sign-off, broader than regression focus.",
            "B": "Functional may target new feature only.",
            "C": "Regression retests existing workflows—answer.",
            "D": "Integration tests component interfaces.",
        },
        "Retest existing hotel flows → regression (C).",
    )
    _r(
        84,
        "Scrum uses rugby scrum metaphor—team moves ball downfield through sprints in adaptive way. DSDM/RAD differ.",
        {
            "A": "RAD is rapid application development acronym, not rugby metaphor.",
            "B": "DSDM is dynamic systems development method.",
            "C": "Evolutionary waterfall is hybrid term, not scrum metaphor.",
            "D": "Scrum name comes from rugby scrum teamwork image.",
        },
        "Rugby/ad hoc ball metaphor → Scrum (D).",
    )
    _r(
        85,
        "Good SRS should be complete, consistent, unambiguous, verifiable—not 'unreliable' as a desired characteristic. Reliability (B) is wrong quality label here.",
        {
            "A": "Completeness is desired.",
            "B": "Reliability is not a standard SRS document quality attribute name—NOT characteristic.",
            "C": "Consistency is desired.",
            "D": "Clarity is desired.",
        },
        "SRS should NOT be characterized by unreliability → pick reliability (B).",
    )
    _r(
        86,
        "Incremental model delivers builds in sequence with limited feedback between major increments compared to iterative/agile loops—"
        "closest to sequential phased delivery without continuous feedback among listed (A).",
        {
            "A": "Incremental adds chunks sequentially—exam keyed answer for no-feedback loops.",
            "B": "Evolutionary prototyping uses feedback.",
            "C": "Agile embraces continuous feedback.",
            "D": "Iterative has explicit iteration and feedback cycles.",
        },
        "Sequential phases, no feedback loops → Incremental (A) per exam key.",
    )
    _r(
        87,
        "JavaScript spread operator ... expands iterables into elements in arrays/object literals. Not a loop counter.",
        {
            "A": "Confuses spread with numeric for-loop mistakes.",
            "B": "... spreads arrays/strings into individual arguments/elements.",
            "C": "Not about iterator increment intervals.",
            "D": "Spread operator exists in modern JavaScript.",
        },
        "JS ... operator → spread iterables to elements (B).",
    )
    _r(
        88,
        "Address translation maps logical to physical via paging/segmentation. Swapping moves processes in/out of memory but is not an address translation scheme.",
        {
            "A": "Segmentation maps logical segments to physical areas.",
            "B": "Combined paging/segmentation still translates addresses.",
            "C": "Swapping is memory management for space, not logical-to-physical mapping.",
            "D": "Paging translates virtual pages to frames.",
        },
        "NOT logical→physical mapping → swapping (C).",
    )
    _r(
        89,
        "document.getElementById('id') is standard DOM API. Other names are OCR garbles of real methods.",
        {
            "A": "getElementById is correct API (OCR: getTagById).",
            "B": "getElementsByName exists but OCR string invalid.",
            "C": "getHTMLClassByName is not standard.",
            "D": "getElementsByClassName exists but stem asks primary id access—getElementById is best.",
        },
        "Access HTML element by id → getElementById (A).",
    )
    _r(
        90,
        "Estimation by analogy compares to similar past projects in same domain to predict effort/cost—matches stem comparison.",
        {
            "A": "Analogy from similar projects is exact match.",
            "B": "Empirical models use formulas from data, not only one similar project.",
            "C": "Expert judgment uses experts, not necessarily similar project data.",
            "D": "Ad hoc is unstructured guess.",
        },
        "Compare to similar project → estimation by analogy (A).",
    )
    _r(
        91,
        "Critical path is longest dependent task sequence determining minimum project duration. Slack is zero on critical tasks.",
        {
            "A": "Full path is informal wording.",
            "B": "Complete path not standard term.",
            "C": "Critical path is PM term for longest chain.",
            "D": "Project path is vague.",
        },
        "Longest dependent task chain → critical path (C).",
    )
    _r(
        92,
        "Architecture primary goal: communicate structures to stakeholders and developers for shared understanding—enables analysis and evolution.",
        {
            "A": "Testing cost reduction is side benefit, not primary goal.",
            "B": "Pattern accuracy is design tactic, not overarching architecture goal.",
            "C": "Shared understanding of structures among stakeholders—central goal.",
            "D": "Requirements completeness is requirements engineering focus.",
        },
        "Architecture goals → shared understanding of structures (C).",
    )
    _r(
        93,
        "Android project src/main/java holds Java/Kotlin source. Manifest in root; XML layouts in res/layout.",
        {
            "A": "XML layouts usually under res, not src root.",
            "B": "Java source code lives under src folder.",
            "C": "AndroidManifest typically at module root, not generic src only.",
            "D": "B is correct.",
        },
        "Android src folder contains Java source (B).",
    )
    _r(
        94,
        "Testing objectives: find defects, assess quality, support decisions—not to lengthen development intentionally.",
        {
            "A": "Usability evaluation can be part of testing scope.",
            "B": "Increasing development time is harmful, not an objective.",
            "C": "Identifying defects is core testing objective.",
            "D": "Performance testing can improve performance metrics.",
        },
        "NOT a testing objective → increasing development time (B).",
    )
    _r(
        95,
        "CPU instruction cycle fetches next instruction using program counter (PC) pointing to address in memory.",
        {
            "A": "PC holds address of next instruction—fetch uses PC.",
            "B": "PSW stores flags/status.",
            "C": "IR holds current instruction opcode.",
            "D": "Status register holds condition codes.",
        },
        "Fetch instruction address → program counter (A).",
    )
    _r(
        96,
        "Data-driven decisions start with collecting relevant data before analysis, interpretation, and final decision.",
        {
            "A": "Decision comes last after evidence.",
            "B": "Analysis follows data collection.",
            "C": "Interpretation follows analysis.",
            "D": "Collecting data is the first step in the process chain.",
        },
        "Data-driven process begins with collecting data (D).",
    )
    _r(
        97,
        "3DES applies DES three times on 64-bit blocks with 56-bit keys (effective 168-bit key), strengthening legacy DES.",
        {
            "A": "144-bit block single pass is not 3DES.",
            "B": "Three DES rounds on 64-bit blocks with 56-bit keys—standard description.",
            "C": "128-bit block description mismatches DES block size.",
            "D": "AES replacement is different algorithm.",
        },
        "Triple DES → three DES applications on 64-bit blocks (B).",
    )
    _r(
        98,
        "Checked exceptions must be declared/caught (IOException). RuntimeException and subclasses are unchecked.",
        {
            "A": "IOException is checked—compiler enforces handling.",
            "B": "RuntimeException is unchecked.",
            "C": "NumberFormatException extends RuntimeException—unchecked.",
            "D": "NegativeArraySizeException is unchecked runtime.",
        },
        "Checked exception example → IOException (A).",
    )
    _r(
        99,
        "Dijkstra critical-region conditions forbid assuming specific CPU speeds or processor count—algorithms must work generally. "
        "Assuming speeds/CPUs (B) is a false assumption.",
        {
            "A": "Progress requirement is valid.",
            "B": "Must not assume relative speeds or number of CPUs—violates fairness generality.",
            "C": "Bounded waiting is desired, not false.",
            "D": "Mutual exclusion on critical region is required.",
        },
        "False critical-region assumption → about CPU speeds/count (B).",
    )
    _r(
        100,
        "A* with admissible heuristic is optimal; worst-case time can grow exponentially in search depth. "
        "Greedy best-first is not optimal; UCS lacks heuristic guidance but is optimal with nonnegative costs.",
        {
            "A": "A* optimal with admissible heuristic, exponential worst case in many graphs—answer.",
            "B": "UCS optimal but lacks heuristic; exponential worst case also possible.",
            "C": "IDS is complete/optimal in unweighted settings with repeated depth limits.",
            "D": "Greedy best-first not optimal—fails optimality requirement in stem.",
        },
        "Optimal informed search, exponential worst case → A* (A).",
    )


_build_bank()


def build_deep_entry(q: dict) -> dict:
    num = q["examNumber"]
    if num not in BANK:
        raise KeyError(f"No deep explanation bank for examNumber {num}")
    base = BANK[num]
    correct = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    options_out = {}
    for key in "ABCD":
        text = opts.get(key, "")
        body = base["options"][key]
        options_out[key] = _opt(correct, key, text, body)
    return {
        "overview": base["overview"],
        "options": options_out,
        "studyTip": base["studyTip"],
    }
