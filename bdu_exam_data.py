"""Manual OCR fixes and focus guide for BDU Model Exit Exam."""

FOCUS_GUIDE = {
    "Data Structures": "Master asymptotic notation, sorting/search complexity, and trace small algorithms by hand.",
    "Java / OOP": "Review constructors, interfaces, exceptions, GC, and Java language restrictions.",
    "Database": "Practice normalization, keys, FDs, ER diagrams, and SQL semantics.",
    "Networking": "Know OSI/TCP layers, protocols, subnetting, and topology tradeoffs.",
    "Security": "Study Saltzer-Schroeder principles, CIA triad, PKI, and malware types.",
    "Project Management": "Learn lifecycle models, risk strategies, WBS, and critical path.",
    "AI / ML": "Classify learning types and search algorithms (BFS, DFS, UCS, A*, greedy).",
    "Software Engineering": "SRS properties, requirements engineering, maintenance, and testing process.",
    "Operating Systems": "Process/thread lifecycle, scheduling, memory management, deadlock.",
    "Web Development": "CSS selectors, HTTP methods/status codes, DOM, and JavaScript basics.",
    "Android": "Activity/Intent/Service rules, manifest, lifecycle, and APK structure.",
    "C++": "Trace loops for complexity, valid syntax, compilation stages.",
    "Software Architecture": "Quality attributes, layered architecture, coupling, ATAM scenarios.",
    "Software Testing": "Test levels, coverage, traceability, and defect lifecycle.",
    "General": "Review lecture notes for any remaining topics.",
}

MANUAL_OVERRIDES: dict[int, dict] = {
    1: {
        "text": "Which asymptotic notation is used to represent algorithm complexity in the worst possible set of inputs?",
        "options": [
            {"key": "A", "text": "Theta notation"},
            {"key": "B", "text": "Big-Oh notation"},
            {"key": "C", "text": "Big-Omega notation"},
            {"key": "D", "text": "All"},
        ],
        "answer": "B",
        "topic": "Data Structures",
    },
    2: {
        "text": "What is the algorithm complexity of Binary search algorithm?",
        "options": [
            {"key": "A", "text": "O(n)"},
            {"key": "B", "text": "O(n^2)"},
            {"key": "C", "text": "O(1)"},
            {"key": "D", "text": "O(log n)"},
        ],
        "answer": "D",
        "topic": "Data Structures",
    },
    3: {
        "text": "Assume you have an algorithm which has time function 2n + 3n^2 + log n + n log n + n, then complexity order of your algorithm is?",
        "options": [
            {"key": "A", "text": "O(n)"},
            {"key": "B", "text": "O(n^2)"},
            {"key": "C", "text": "O(log n)"},
            {"key": "D", "text": "O(n log n)"},
        ],
        "answer": "B",
        "topic": "Data Structures",
    },
    4: {
        "text": "What would be the Algorithm complexity to add a node at the end of singly linked list, if the pointer is initially pointing to the head of the list?",
        "options": [
            {"key": "A", "text": "O(1)"},
            {"key": "B", "text": "O(n)"},
            {"key": "C", "text": "O(log n)"},
            {"key": "D", "text": "O(n^2)"},
        ],
        "answer": "B",
        "topic": "Data Structures",
    },
    9: {
        "text": "Which one is a valid identifier in C++?",
        "options": [
            {"key": "A", "text": "int"},
            {"key": "B", "text": "_count"},
            {"key": "C", "text": "2value"},
            {"key": "D", "text": "class"},
        ],
        "answer": "B",
        "topic": "C++",
    },
    10: {
        "text": "What is the output of the program using continue in a loop?",
        "options": [
            {"key": "A", "text": "0"},
            {"key": "B", "text": "1"},
            {"key": "C", "text": "1.0"},
            {"key": "D", "text": "1.2"},
        ],
        "answer": "D",
        "topic": "C++",
    },
    11: {
        "text": "What will be the output of the following code with a reference parameter multiplying by 5?",
        "options": [
            {"key": "A", "text": "5"},
            {"key": "B", "text": "25"},
            {"key": "C", "text": "10"},
            {"key": "D", "text": "20"},
        ],
        "answer": "B",
        "topic": "C++",
    },
    20: {
        "text": "Which HTML tag is used to create a hyperlink?",
        "options": [
            {"key": "A", "text": "<link>"},
            {"key": "B", "text": "<a>"},
            {"key": "C", "text": "<href>"},
            {"key": "D", "text": "<url>"},
        ],
        "answer": "B",
        "topic": "Web Development",
    },
    27: {
        "text": "Which JavaScript syntax is used to enclose multi-line comments?",
        "options": [
            {"key": "A", "text": "// comment"},
            {"key": "B", "text": "# comment"},
            {"key": "C", "text": "<!-- comment -->"},
            {"key": "D", "text": "/* comment */"},
        ],
        "answer": "D",
        "topic": "Web Development",
    },
    41: {
        "text": "Which IPv4 address class does this address belong to: 6.142.3.5?",
        "options": [
            {"key": "A", "text": "Class A"},
            {"key": "B", "text": "Class B"},
            {"key": "C", "text": "Class C"},
            {"key": "D", "text": "Class D"},
        ],
        "answer": "A",
        "topic": "Networking",
    },
    42: {
        "text": "A threat is:",
        "options": [
            {"key": "A", "text": "All of the above"},
            {"key": "B", "text": "The potential danger to information or systems"},
            {"key": "C", "text": "Illegal access to electronic data"},
            {"key": "D", "text": "Flaws that weaken security of a system"},
        ],
        "answer": "B",
        "topic": "Security",
    },
    44: {
        "text": "Which of the following describes a set of elements and relationships among them for a domain?",
        "options": [
            {"key": "A", "text": "Reference Architecture"},
            {"key": "B", "text": "Software architecture"},
            {"key": "C", "text": "Architectural pattern"},
            {"key": "D", "text": "Reference model"},
        ],
        "answer": "D",
        "topic": "Software Architecture",
    },
    45: {
        "text": "Which option best defines Artificial Intelligence?",
        "options": [
            {"key": "A", "text": "All of the above"},
            {"key": "B", "text": "Programs producing output reflecting human-like intelligence"},
            {"key": "C", "text": "Embodiment of human intellectual capabilities in a computer"},
            {"key": "D", "text": "Study of mental faculties with computer models"},
        ],
        "answer": "A",
        "topic": "AI / ML",
    },
    46: {
        "text": "Which project management phase includes defining project scope and obtaining authorization to start?",
        "options": [
            {"key": "A", "text": "Planning"},
            {"key": "B", "text": "Execution"},
            {"key": "C", "text": "Initiation"},
            {"key": "D", "text": "Closure"},
        ],
        "answer": "C",
        "topic": "Project Management",
    },
    51: {
        "text": "During project execution, a team member is not sure of what work to accomplish. Which document contains detailed descriptions of work packages?",
        "options": [
            {"key": "A", "text": "Project scope statement"},
            {"key": "B", "text": "Activity list"},
            {"key": "C", "text": "WBS"},
            {"key": "D", "text": "Scope management plan"},
        ],
        "answer": "C",
        "topic": "Project Management",
    },
}

EXPLICIT_ANSWERS: dict[int, str] = {}
