"""2017 Software Engineering Exit Exam — manual fixes, answers, focus guide."""

from __future__ import annotations

FOCUS_GUIDE: dict[str, str] = {
    "Fundamentals of Programming": "Loops, operators, formulas, variable rules, and basic C/C++/Python syntax.",
    "Data Structures": "Stacks, queues, trees, graphs, BFS/DFS, hash tables, and Big-O reasoning.",
    "Java / OOP": "Inheritance, interfaces, encapsulation, polymorphism, and Java keywords.",
    "Web Development": "HTML/CSS/JS, HTTP methods, AJAX, and client-server roles.",
    "Android": "Activity, Intent, Service, Manifest permissions, and APK components.",
    "Database": "Keys, normalization, SQL, ER mapping, and ACID properties.",
    "Operating Systems": "Process states, deadlock conditions, scheduling, paging, and memory.",
    "Software Engineering": "SDLC, requirements, refactoring, code smells, and maintenance.",
    "Software Architecture": "Styles (monolithic, microservices, event-driven), quality attributes.",
    "Project Management": "WBS, Gantt, critical path, scope, and planning activities.",
    "Software Testing": "Test levels, white/black box, QA goals, and traceability.",
    "Networking": "Topologies, OSI/TCP, routing, and protocol behavior.",
    "Security": "CIA triad, XSS, firewalls, authentication (PKI/MFA), and risk.",
    "AI / ML": "Search algorithms, agents, supervised learning, and heuristics.",
    "C++": "User-defined types, pointers, syntax, and valid identifiers.",
    "General": "Re-read missed questions and verify definitions in course notes.",
}

MANUAL_ANSWERS: dict[int, str] = {
    2: "B",    # Fragments — reusable UI in Activity
    5: "C",    # Integration Testing
    8: "C",    # Corrective maintenance (fault repair)
    9: "C",    # Flow control
    10: "B",   # NFRs: performance, security, usability
    11: "C",   # Requirements should be testable/measurable
    12: "D",   # Classification for spam detection
    14: "C",   # Package managers for install/config
    19: "A",   # switch(day) case 1 -> Monday (typical exam)
    20: "B",   # Semantic network for entity relations
    26: "B",   # Risk management
    27: "C",   # Event-Driven Architecture
    29: "D",   # Hash table for real-time insert/delete
    33: "C",   # Stateful Inspection Firewall
    36: "B",   # Encapsulation restricts direct access
    37: "A",   # Inspection (static testing)
    40: "C",   # Function Points for size estimation
    42: "C",   # Function Points (FP)
    45: "A",   # If-else for prime check
    47: "C",   # Training for policy compliance
    48: "A",   # Hold and Wait
    49: "C",   # AI rapidly evolving field
    50: "C",   # Axios for HTTP requests in React stack
    52: "A",
    53: "D",
    54: "D",
    55: "C",
    56: "A",
    57: "D",
    58: "B",
    59: "D",
    62: "B",
    63: "D",
    64: "B",
    66: "C",   # AJAX asynchronous requests
    67: "D",   # Critical risk priority
    68: "C",
    70: "D",
    71: "B",
    72: "D",
    74: "C",
    77: "A",   # GDPR — inform users about data use
    83: "B",   # Improved maintainability (KISS)
    84: "A",   # Merge Sort — divide and conquer
    85: "B",   # WebSocket real-time communication
    90: "B",   # IDE primary purpose: write/debug code
    91: "C",   # Regression testing after changes
    92: "D",   # Analyzing requirements first
    93: "B",   # White-box testing
    94: "B",   # do-while executes at least once
    95: "C",   # ALTER TABLE ADD COLUMN
    96: "D",   # Stakeholder requirements (requirement engineering)
    97: "D",   # Define/manage stakeholder requirements
    98: "D",   # Debugging: identify and fix errors
    99: "B",   # Open/Closed Principle
    100: "C",  # PKI certificates
}

QUESTION_FIXES: dict[int, dict] = {
    19: {
        "text": (
            "What will the output of the following code?\n\n"
            "#include <iostream>\n"
            "using namespace std;\n"
            "int main() {\n"
            "    int day = 1;\n"
            "    switch (day) {\n"
            "        case 1: cout << \"Monday\"; break;\n"
            "        case 2: cout << \"Tuesday\"; break;\n"
            "        case 3: cout << \"Wednesday\"; break;\n"
            "        default: cout << \"Invalid day\"; break;\n"
            "    }\n"
            "    return 0;\n"
            "}"
        ),
        "options": [
            {"key": "A", "text": "Monday"},
            {"key": "B", "text": "Tuesday"},
            {"key": "C", "text": "Wednesday"},
            {"key": "D", "text": "Invalid day"},
        ],
        "answer": "A",
        "topic": "C++",
    },
    52: {
        "text": "Which one of the following deadlock condition occurs when a process holding at least one resource is waiting to acquire additional resources held by other processes?",
        "options": [
            {"key": "A", "text": "Hold and Wait"},
            {"key": "B", "text": "No Preemption"},
            {"key": "C", "text": "Mutual Exclusion"},
            {"key": "D", "text": "Circular Wait"},
        ],
        "answer": "A",
        "topic": "Operating Systems",
    },
    53: {
        "text": "Among the listed components of an Android application, which one helps declare permissions such as accessing sensitive data (GPS, Camera, and Storage)?",
        "options": [
            {"key": "A", "text": "Views and ViewGroups"},
            {"key": "B", "text": "Content Provider"},
            {"key": "C", "text": "Intents"},
            {"key": "D", "text": "AndroidManifest.xml"},
        ],
        "answer": "D",
        "topic": "Android",
    },
    54: {
        "text": "Which one of the following is a code smell in software?",
        "options": [
            {"key": "A", "text": "Frequent code reviews"},
            {"key": "B", "text": "Consistent naming conventions"},
            {"key": "C", "text": "High code test coverage"},
            {"key": "D", "text": "Long method length"},
        ],
        "answer": "D",
        "topic": "Software Engineering",
    },
    55: {
        "text": "In which of the following topologies does a central server provide connectivity for all pairs of nodes willing to communicate with each other?",
        "options": [
            {"key": "A", "text": "Bus"},
            {"key": "B", "text": "Mesh"},
            {"key": "C", "text": "Star"},
            {"key": "D", "text": "Ring"},
        ],
        "answer": "C",
        "topic": "Networking",
    },
    56: {
        "text": "Write a program to find the sum of the first n natural numbers (1 to n). What is the correct formula to calculate this sum?",
        "options": [
            {"key": "A", "text": "n * (n + 1) / 2"},
            {"key": "B", "text": "n * (n + 2) / 2"},
            {"key": "C", "text": "n * (n - 1) / 2"},
            {"key": "D", "text": "n + (n - 1) / 2"},
        ],
        "answer": "A",
        "topic": "Fundamentals of Programming",
    },
    57: {
        "text": "Which of the following is not a user-defined data type?",
        "options": [
            {"key": "A", "text": "Structure"},
            {"key": "B", "text": "Union"},
            {"key": "C", "text": "Enumeration"},
            {"key": "D", "text": "Integer"},
        ],
        "answer": "D",
        "topic": "C++",
    },
    58: {
        "text": "Which of the following is correct regarding the difference between breadth-first search and depth-first search?",
        "options": [
            {"key": "A", "text": "Breadth-first search requires less memory compared to depth-first search"},
            {"key": "B", "text": "Breadth-first search is slower than depth-first search"},
            {"key": "C", "text": "Breadth-first search is faster than depth-first search"},
            {"key": "D", "text": "Depth-first search is useful in finding shortest path, while breadth-first search is not"},
        ],
        "answer": "B",
        "topic": "AI / ML",
    },
    59: {
        "text": "What is the primary focus of refactoring in software development?",
        "options": [
            {"key": "A", "text": "Rewriting the entire software to improve its performance"},
            {"key": "B", "text": "Enhancing the external user interface"},
            {"key": "C", "text": "Adding new functionalities"},
            {"key": "D", "text": "Improving internal code structure without changing external behavior"},
        ],
        "answer": "D",
        "topic": "Software Engineering",
    },
    62: {
        "text": "Which of the following models is NOT considered a state-of-the-art software process model?",
        "options": [
            {"key": "A", "text": "Extreme Programming (XP)"},
            {"key": "B", "text": "Waterfall model"},
            {"key": "C", "text": "Agile Model"},
            {"key": "D", "text": "Spiral model"},
        ],
        "answer": "B",
        "topic": "Software Engineering",
    },
    63: {
        "text": "Which of the following project management tools is used for scope management?",
        "options": [
            {"key": "A", "text": "Critical path analysis"},
            {"key": "B", "text": "Gantt Chart"},
            {"key": "C", "text": "Net present value"},
            {"key": "D", "text": "Work breakdown structures"},
        ],
        "answer": "D",
        "topic": "Project Management",
    },
    64: {
        "text": "Which of the following activities is not conducted in software planning?",
        "options": [
            {"key": "A", "text": "Organizational and Resource Planning"},
            {"key": "B", "text": "Managing Stage Boundaries"},
            {"key": "C", "text": "Cost Estimation and Budgeting"},
            {"key": "D", "text": "Project Plan Development and Execution"},
        ],
        "answer": "B",
        "topic": "Project Management",
    },
    68: {
        "text": "Which one of the following types of firewall tracks active connections and allows only legitimate traffic?",
        "options": [
            {"key": "A", "text": "Proxy Firewall"},
            {"key": "B", "text": "Cloud-Based Firewall"},
            {"key": "C", "text": "Stateful Inspection Firewall"},
            {"key": "D", "text": "Packet Filtering Firewall"},
        ],
        "answer": "C",
        "topic": "Security",
    },
    70: {
        "text": "What is the first step in developing a medium-scale application that solves real-world problems?",
        "options": [
            {"key": "A", "text": "Writing code immediately"},
            {"key": "B", "text": "Choosing a programming language randomly"},
            {"key": "C", "text": "Copying code from online sources"},
            {"key": "D", "text": "Analyzing requirements and designing system architecture"},
        ],
        "answer": "D",
        "topic": "Software Engineering",
    },
    71: {
        "text": "Which one of the following vulnerabilities injects JavaScript to steal user data?",
        "options": [
            {"key": "A", "text": "Insecure Deserialization"},
            {"key": "B", "text": "Cross-Site Scripting (XSS)"},
            {"key": "C", "text": "Spyware"},
            {"key": "D", "text": "Buffer Overflow"},
        ],
        "answer": "B",
        "topic": "Security",
    },
    26: {
        "text": "Which software engineering practice focuses on identifying and mitigating potential risks during the development process?",
        "options": [
            {"key": "A", "text": "Deployment planning"},
            {"key": "B", "text": "Risk management"},
            {"key": "C", "text": "Version control"},
            {"key": "D", "text": "User interface design"},
        ],
        "answer": "B",
        "topic": "Software Engineering",
    },
    28: {
        "text": "Which one of the following is a critical feature when designing for system scalability in a large-scale software system?",
        "options": [
            {"key": "A", "text": "Using a monolithic codebase for simplicity"},
            {"key": "B", "text": "Limiting API access to avoid traffic"},
            {"key": "C", "text": "Horizontal scaling through independent services"},
            {"key": "D", "text": "Using a single database for all services"},
        ],
        "answer": "C",
        "topic": "Software Architecture",
    },
    73: {
        "text": "Which one of the following Process Scheduling Algorithms executes processes in order of arrival?",
        "options": [
            {"key": "A", "text": "Round Robin (RR)"},
            {"key": "B", "text": "First-Come, First-Served (FCFS)"},
            {"key": "C", "text": "Priority Scheduling"},
            {"key": "D", "text": "Shortest Job Next (SJN)"},
        ],
        "answer": "B",
        "topic": "Operating Systems",
    },
    29: {
        "text": "Suppose you are developing an application that involves real-time data analysis and requires efficient insertion and deletion of data. Which of the following data structures would be best suited for this application?",
        "options": [
            {"key": "A", "text": "Stack"},
            {"key": "B", "text": "Queue"},
            {"key": "C", "text": "Binary tree"},
            {"key": "D", "text": "Hash table"},
        ],
        "answer": "D",
        "topic": "Data Structures",
    },
    74: {
        "text": "Which of the following software architectural styles is typically used in systems where high responsiveness and real-time processing are needed?",
        "options": [
            {"key": "A", "text": "Monolithic Architecture"},
            {"key": "B", "text": "Microservices Architecture"},
            {"key": "C", "text": "Event-Driven Architecture"},
            {"key": "D", "text": "Serverless Architecture"},
        ],
        "answer": "C",
        "topic": "Software Architecture",
    },
    47: {
        "text": "A software company wants to implement a new data security policy for a newly developed system. The most effective way to ensure employee awareness and compliance is to:",
        "options": [
            {"key": "A", "text": "Rely on employees to read and understand the policy on their own time"},
            {"key": "B", "text": "Delegate responsibility for policy enforcement to IT security personnel"},
            {"key": "C", "text": "Provide comprehensive training on the policy and its importance"},
            {"key": "D", "text": "Distribute the policy document via email and require a signature for receipt"},
        ],
        "answer": "C",
        "topic": "Security",
    },
    100: {
        "text": "Which one of the following authentication methods uses cryptographic certificates for secure authentication?",
        "options": [
            {"key": "A", "text": "Multi-Factor Authentication (MFA)"},
            {"key": "B", "text": "OTP"},
            {"key": "C", "text": "Public Key Infrastructure (PKI)"},
            {"key": "D", "text": "Biometric Authentication"},
        ],
        "answer": "C",
        "topic": "Security",
    },
}

TOPIC_RULES: list[tuple[str, str]] = [
    ("Database", r"relation|functional dependency|foreign key|ER diagram|SQL|entity|attribute|null|cardinality|normal|ACID"),
    ("Java / OOP", r"java|polymorph|interface|package scope|exception|garbage|inheritance|abstract class"),
    ("Networking", r"OSI|TCP|ICMP|layer|port|IPv4|wireless|topology|star|bus|mesh|ring|subnet|gateway|HTTP"),
    ("Android", r"android|activity|service|content provider|manifest|intent|lifecycle|APK|permission"),
    ("Security", r"security|cyber|risk|firewall|XSS|encryption|authentication|PKI|MFA|vulnerability|virus"),
    ("Project Management", r"spiral|critical path|scrum|agile|waterfall|WBS|Gantt|scope|planning|stage boundary"),
    ("AI / ML", r"supervised|search algorithm|BFS|DFS|UCS|Dijkstra|A\*|uninformed|informed|heuristic|agent"),
    ("Software Engineering", r"SRS|requirement|testing|maintenance|refactor|code smell|SDLC|feasibility|UML"),
    ("Operating Systems", r"operating system|process|thread|deadlock|memory management|swapping|paging|scheduling"),
    ("C++", r"C\+\+|structure|union|enumeration|user.?defined|cout|pointer"),
    ("Web Development", r"CSS|javascript|HTTP|HTML|AJAX|async|Django|PHP"),
    ("Data Structures", r"queue|stack|sort|binary tree|hash table|graph|linked list|data structure|Big.?O"),
    ("Software Architecture", r"architecture|microservice|monolithic|event.?driven|serverless|quality attribute"),
    ("Software Testing", r"unit test|white.?box|black.?box|test case|QA|regression"),
    ("Fundamentals of Programming", r"loop|variable|printf|formula|natural number|operator|Python|complexity"),
]
