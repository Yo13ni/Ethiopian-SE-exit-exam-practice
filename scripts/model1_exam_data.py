"""Manual overrides and focus guide for MoEE Model Exam 1."""

from __future__ import annotations

FOCUS_GUIDE: dict[str, str] = {
    "Operating Systems": "Scheduling levels, boot process, memory management, and file systems.",
    "Java / OOP": "Inheritance, polymorphism, access modifiers, interfaces, and trace small code outputs.",
    "Data Structures": "Trees, queues, hash tables, and time-complexity analysis.",
    "Database": "Keys, CASCADE actions, SQL joins, views, and ER participation.",
    "Networking": "OSI layers, switches, IPv4, ACLs, and encapsulation.",
    "Web Development": "HTML forms, CSS properties, and JavaScript APIs.",
    "Android": "Lifecycle, layouts, APK, Dalvik/ART, and UI components.",
    "Software Testing": "Coverage types, integration testing, precision/recall, and test principles.",
    "Software Engineering": "SDLC, requirements, CASE tools, validation vs verification.",
    "Project Management": "Project definition, org structures, affinity diagrams, and Pareto.",
    "AI / ML": "Agents, search algorithms, ensemble methods, overfitting, and preprocessing.",
    "Security": "CIA triad, digital signatures, and professional ethics.",
    "Software Architecture": "Styles, notation, performance tactics, and architectural decisions.",
    "C++": "Headers, I/O streams, and control-flow behavior.",
    "General": "Review lecture notes for any remaining topics.",
}

MANUAL_OVERRIDES: dict[int, dict] = {
    4: {
        "text": (
            "Class A is abstract with abstract method `String welcome()` (no parameters). "
            "Which definition of Class B extending Class A will NOT cause a compiler error?"
        ),
        "options": [
            {
                "key": "A",
                "text": "Class B extends A but only defines whatObjectAmI() — does not implement welcome()",
            },
            {
                "key": "B",
                "text": "Class B defines void welcome(String str) — wrong return type and parameters",
            },
            {
                "key": "C",
                "text": "Class B extends A with only whatObjectAmI() — same issue as A",
            },
            {
                "key": "D",
                "text": "Class B defines void welcome(String str) — same issue as B",
            },
        ],
        "answer": "A",
        "topic": "Java / OOP",
    },
    9: {
        "options": [
            {"key": "A", "text": "parseJson()"},
            {"key": "B", "text": "toJson()"},
            {"key": "C", "text": "JSON.stringify()"},
            {"key": "D", "text": "JSON.parse()"},
        ],
        "answer": "C",
    },
    11: {
        "text": (
            "Given nested if-statements comparing width, length, and height, "
            "how many test cases are required for 100% decision coverage?"
        ),
    },
    22: {
        "text": (
            "What is printed? int[] arr = {3,4,5,6,7}; "
            "for (int i = 0; i < arr.length - 2; ++i) System.out.print(arr[i] + \" \");"
        ),
    },
    66: {
        "options": [
            {"key": "A", "text": "onRestart()"},
            {"key": "B", "text": "onCreate()"},
            {"key": "C", "text": "onClick()"},
            {"key": "D", "text": "onStart()"},
        ],
        "answer": "B",
    },
    94: {
        "options": [
            {"key": "A", "text": "public class Invoice extends Payable { ... } — interfaces use implements, not extends"},
            {"key": "B", "text": "Missing return type double on getPaymentAmount()"},
            {"key": "C", "text": "public class Invoice implements Payable { public double getPaymentAmount(){ return getQuantity() * getPricePerItem(); } }"},
            {"key": "D", "text": "abstract class unnecessarily used when concrete implementation suffices"},
        ],
        "answer": "C",
    },
    23: {"topic": "AI / ML"},
    24: {"topic": "Software Testing"},
    29: {"topic": "AI / ML"},
    48: {"topic": "Security"},
    67: {"topic": "Android"},
    78: {"topic": "Software Architecture"},
    79: {"topic": "AI / ML"},
    82: {"topic": "Software Architecture"},
    91: {"topic": "AI / ML"},
}
