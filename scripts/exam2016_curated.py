"""Curated 2016 Software Engineering Exit Exam question bank (100 items).

Each question follows:
{
    "id": int,
    "text": str,
    "options": [{"key": "A"|"B"|"C"|"D", "text": str}, ...],
    "answer": "A"|"B"|"C"|"D",
    "topic": str,
}
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

try:
    from exam2016_data import EXTRA_QUESTIONS, QUESTION_FIXES
except ModuleNotFoundError:  # pragma: no cover - allows `python -m` from repo root
    from scripts.exam2016_data import EXTRA_QUESTIONS, QUESTION_FIXES

_ROOT = Path(__file__).resolve().parent.parent
_BASE_QUESTIONS = _ROOT / "data" / "exams" / "2016" / "questions.json"

_TOPIC_MAP = {
    "Java/OOP": "Java / OOP",
    "AI/ML": "AI / ML",
    "General": "Software Engineering",
}


def _normalize_topic(topic: str) -> str:
    if topic in _TOPIC_MAP:
        return _TOPIC_MAP[topic]
    return topic


def _as_question(qid: int, text: str, options: list[dict], answer: str, topic: str) -> dict:
    clean_options = [{"key": o["key"], "text": str(o["text"]).strip()} for o in options]
    return {
        "id": qid,
        "text": str(text).strip(),
        "options": clean_options,
        "answer": answer.strip().upper(),
        "topic": _normalize_topic(topic.strip()),
    }


def _load_initial_questions() -> dict[int, dict]:
    """Seed only from hand-curated QUESTION_FIXES — never from scrambled questions.json."""
    out: dict[int, dict] = {}
    for qid, fix in QUESTION_FIXES.items():
        if qid > 97:
            continue
        out[qid] = _as_question(
            qid=qid,
            text=fix["text"],
            options=fix["options"],
            answer=fix["answer"],
            topic=fix["topic"],
        )
    return out


def _apply_required_corrections(questions: dict[int, dict]) -> None:
    # Q7: Iterative Deepening A* Search (correct), not plain A*.
    questions[7] = _as_question(
        7,
        "An informed search algorithm that provides exponential time complexity in the worst-case scenario "
        "and guarantees optimality when searching a solution refers to:",
        [
            {"key": "A", "text": "Iterative Deepening A* Search"},
            {"key": "B", "text": "Greedy Best-First Search"},
            {"key": "C", "text": "Uniform Cost Search"},
            {"key": "D", "text": "A* Search"},
        ],
        "A",
        "AI / ML",
    )

    # Q9: split merged options and keep source wording intent.
    questions[9] = _as_question(
        9,
        "Which one of the following can be among possible sources of unstructured data?",
        [
            {"key": "A", "text": "Google search engine"},
            {"key": "B", "text": "RDBMS systems"},
            {"key": "C", "text": "Employee database"},
            {"key": "D", "text": "Registrar student database"},
        ],
        "A",
        "Database",
    )

    questions[11] = _as_question(
        11,
        "What is used to pass data between activities in Android?",
        [
            {"key": "A", "text": "Broadcast receiver"},
            {"key": "B", "text": "PostgreSQL database"},
            {"key": "C", "text": "Intent"},
            {"key": "D", "text": "Content provider"},
        ],
        "C",
        "Android",
    )

    questions[16] = _as_question(
        16,
        "Assume you have an interface Payable:\n"
        "public interface Payable {\n"
        "    double getPaymentAmount();\n"
        "}\n"
        "You have class Invoice with getQuantity() and getPricePerItem(). "
        "Which implementation is correct?",
        [
            {
                "key": "A",
                "text": "public abstract class Invoice implements Payable { public double getPaymentAmount(){ return getQuantity()*getPricePerItem(); } }",
            },
            {
                "key": "B",
                "text": "public class Invoice implements Payable { public double getPaymentAmount(){ return getQuantity()*getPricePerItem(); } }",
            },
            {
                "key": "C",
                "text": "public class Invoice extends Payable { public double getPaymentAmount(){ return getQuantity()*getPricePerItem(); } }",
            },
            {
                "key": "D",
                "text": "public class Invoice implements Payable { public int getPaymentAmount(){ return getQuantity()*getPricePerItem(); } }",
            },
        ],
        "B",
        "Java / OOP",
    )

    questions[17] = _as_question(
        17,
        "A firewall is used in systems connected to wide area networks to:",
        [
            {"key": "A", "text": "Stop unauthorized access by hackers"},
            {"key": "B", "text": "Scan files for viruses"},
            {"key": "C", "text": "Prevent physical fire spread in network cables"},
            {"key": "D", "text": "Increase network bandwidth"},
        ],
        "A",
        "Security",
    )
    questions[24] = _as_question(
        24,
        "Which one of the following statements is wrong regarding try-catch construct?",
        [
            {"key": "A", "text": "Execution control moves to catch block after exception in try block"},
            {"key": "B", "text": "When exception occurs, execution of try block is interrupted"},
            {"key": "C", "text": "The catch block is executed once regardless of exceptions in try block"},
            {"key": "D", "text": "The catch block handles exceptions that occur in try block"},
        ],
        "C",
        "Java / OOP",
    )
    questions[25] = _as_question(
        25,
        "Assume Class_A is abstract and contains abstract method welcome() returning String. "
        "Which Class_B definition will NOT cause compiler error?",
        [
            {"key": "A", "text": 'public class Class_B extends Class_A { public int welcome(){ return 10; } }'},
            {"key": "B", "text": 'public class Class_B extends Class_A { public void welcome(String s){ } }'},
            {"key": "C", "text": 'public class Class_B extends Class_A { public String welcome(){ return "I am class B"; } }'},
            {"key": "D", "text": "public class Class_B extends Class_A { }"},
        ],
        "C",
        "Java / OOP",
    )

    questions[28] = _as_question(
        28,
        "Which of the following is true about abstract class?",
        [
            {"key": "A", "text": "Cannot be instantiated"},
            {"key": "B", "text": "Is a mechanism of encapsulation"},
            {"key": "C", "text": "Can contain both abstract and non-abstract methods"},
            {"key": "D", "text": "Cannot be inherited"},
        ],
        "A",
        "Java / OOP",
    )
    questions[29] = _as_question(
        29,
        "Which of the following is not a principal event that causes processes to be created?",
        [
            {"key": "A", "text": "Multiple execution of processes"},
            {"key": "B", "text": "Execution of a process-creation system call by a running process"},
            {"key": "C", "text": "System initialization"},
            {"key": "D", "text": "A user request to create a new process"},
        ],
        "A",
        "Operating Systems",
    )
    questions[30] = _as_question(
        30,
        (
            "A salesperson at Markato shop noticed people who buy shoes also buy socks with high probability. "
            "Which big data analytics technique best supports this pattern?"
        ),
        [
            {"key": "A", "text": "Clustering algorithm"},
            {"key": "B", "text": "Predictive modeling"},
            {"key": "C", "text": "Regression modeling"},
            {"key": "D", "text": "Association rule"},
        ],
        "D",
        "AI / ML",
    )
    questions[34] = _as_question(
        34,
        "Select the one that is not correct related to generalization in system modeling:",
        [
            {
                "key": "A",
                "text": "In generalization, attributes and operations of higher-level classes are associated with lower-level classes",
            },
            {"key": "B", "text": "Facilitate easy modification of data"},
            {
                "key": "C",
                "text": "Higher-level classes are more specific than lower-level classes by adding attributes and operations",
            },
            {"key": "D", "text": "Common information will be maintained in one place"},
        ],
        "C",
        "Software Engineering",
    )
    questions[39] = _as_question(
        39,
        (
            "What is the time complexity for the following code snippet?\n\n"
            "function someFunction(n) {\n"
            "  for (var i = 0; i < n * 10; i++) {\n"
            "    console.log(n);\n"
            "  }\n"
            "}"
        ),
        [
            {"key": "A", "text": "O(n)"},
            {"key": "B", "text": "O(n^2)"},
            {"key": "C", "text": "O(n log n)"},
            {"key": "D", "text": "O(log n)"},
        ],
        "A",
        "Data Structures",
    )
    questions[40] = _as_question(
        40,
        "While optimizing our relation, if we found that no multivalued attributes and no partial dependencies "
        "exist in a relation, then the relation is in what normal form?",
        [
            {"key": "A", "text": "2NF"},
            {"key": "B", "text": "4NF"},
            {"key": "C", "text": "1NF"},
            {"key": "D", "text": "3NF"},
        ],
        "A",
        "Database",
    )
    questions[41] = _as_question(
        41,
        "Which of the following is true regarding the use of switches and hubs for network connectivity?",
        [
            {"key": "A", "text": "Switches increase the number of collision domains in the network"},
            {"key": "B", "text": "Switches take less time to process frames than hubs take"},
            {"key": "C", "text": "Switches do not forward broadcasts"},
            {"key": "D", "text": "Hubs can filter frames"},
        ],
        "A",
        "Networking",
    )
    questions[42] = _as_question(
        42,
        "Which statement describes the main goal of software testing as part of the quality assurance process?",
        [
            {"key": "A", "text": "To achieve project timelines and deadlines"},
            {"key": "B", "text": "To monitor the entire SDLC"},
            {"key": "C", "text": "To generate software requirement and design documentation"},
            {"key": "D", "text": "To guarantee that the software meets the specified requirements"},
        ],
        "D",
        "Software Testing",
    )
    questions[43] = _as_question(
        43,
        "Which of the following describes a set of standards and an associated network protocol that allow "
        "establishing a secure channel between a local and a remote computer?",
        [
            {"key": "A", "text": "Authentication, Authorization and Accounting (AAA)"},
            {"key": "B", "text": "Simple Network Management Protocol (SNMP)"},
            {"key": "C", "text": "Secure Shell (SSH)"},
            {"key": "D", "text": "Secure Socket Layer (SSL)"},
        ],
        "C",
        "Security",
    )
    questions[44] = _as_question(
        44,
        "What component hides the distinction or boundaries between various microservices from end-client application?",
        [
            {"key": "A", "text": "A layered system"},
            {"key": "B", "text": "API gateway"},
            {"key": "C", "text": "API logging"},
            {"key": "D", "text": "API proxy"},
        ],
        "B",
        "Software Architecture",
    )
    questions[56] = _as_question(
        56,
        "Which of the following is one of the indirect applications of queues?",
        [
            {"key": "A", "text": "Operating systems schedule jobs in order of arrival (e.g., a print queue)"},
            {"key": "B", "text": "Simulation of real-world first-come first-served scenarios"},
            {"key": "C", "text": "Auxiliary data structure for algorithms"},
            {"key": "D", "text": "Multiprogramming"},
        ],
        "D",
        "Data Structures",
    )
    questions[58] = _as_question(
        58,
        "Which design pattern is used to restore the state of an object to its previous state?",
        [
            {"key": "A", "text": "Iterator pattern"},
            {"key": "B", "text": "Observer pattern"},
            {"key": "C", "text": "Memento pattern"},
            {"key": "D", "text": "Visitor pattern"},
        ],
        "C",
        "Software Engineering",
    )
    questions[60] = _as_question(
        60,
        "Which of the following shows the five stages in Tuckman's model of team development, in sequential order?",
        [
            {"key": "A", "text": "Forming, storming, performing, norming, and adjourning"},
            {"key": "B", "text": "Forming, storming, norming, performing, and adjourning"},
            {"key": "C", "text": "Norming, forming, storming, performing, and adjourning"},
            {"key": "D", "text": "Storming, forming, norming, performing, and adjourning"},
        ],
        "D",
        "Project Management",
    )
    questions[61] = _as_question(
        61,
        "Which one of the following is not among the purposes of software testing?",
        [
            {"key": "A", "text": "Requesting more design and implementation time"},
            {"key": "B", "text": "Identifying shortcomings"},
            {"key": "C", "text": "Improving product acceptance"},
            {"key": "D", "text": "Enhancing reliability"},
        ],
        "A",
        "Software Testing",
    )
    questions[63] = _as_question(
        63,
        '"The system architecture should be designed using fine-grain, self-contained components. '
        "Producers of data should be separated from consumers and shared data structures should be avoided.\" "
        "For which requirement does this architecture description apply?",
        [
            {"key": "A", "text": "Performance"},
            {"key": "B", "text": "Availability"},
            {"key": "C", "text": "Maintainability"},
            {"key": "D", "text": "Security"},
        ],
        "C",
        "Software Engineering",
    )
    questions[65] = _as_question(
        65,
        "A queue in which the item most recently added is always the first one out refers to:",
        [
            {"key": "A", "text": "FIFO queue"},
            {"key": "B", "text": "Real time queue"},
            {"key": "C", "text": "Priority queue"},
            {"key": "D", "text": "LIFO queue"},
        ],
        "D",
        "Data Structures",
    )
    questions[68] = _as_question(
        68,
        "Which of the following is the correct sequence that will be followed during software evolution process?",
        [
            {"key": "A", "text": "Change request, release planning, change implementation, impact analysis, system release"},
            {"key": "B", "text": "Change request, impact analysis, release planning, change implementation, system release"},
            {"key": "C", "text": "Impact analysis, change request, change implementation, release planning, system release"},
            {"key": "D", "text": "Change request, impact analysis, change implementation, release planning, system release"},
        ],
        "B",
        "Software Engineering",
    )
    questions[69] = _as_question(
        69,
        "Which of the following UML element is wrongly applied?",
        [
            {"key": "A", "text": "Use case diagram represents an interaction with the system"},
            {"key": "B", "text": "Sequence diagram shows the sequence of interactions required to complete an operation"},
            {"key": "C", "text": "Activity diagram shows how the system reacts to internal and external events"},
            {"key": "D", "text": "Class diagram shows the object classes in a system and their relation"},
        ],
        "C",
        "Software Engineering",
    )
    questions[70] = _as_question(
        70,
        "Select the wrong statement regarding traceability in software development projects:",
        [
            {"key": "A", "text": "Traceability shows the dependency among two or more requirements if any"},
            {"key": "B", "text": "Requirements should be linked to the respective stakeholder who generated them"},
            {"key": "C", "text": "Traceability traces the overall cost and schedule of every activity in the requirement"},
            {"key": "D", "text": "Every design element (component) should be linked back to the requirement"},
        ],
        "C",
        "Software Engineering",
    )
    questions[71] = _as_question(
        71,
        "Which principle states that 80% of the problems can be fixed with 20% of the entire effort?",
        [
            {"key": "A", "text": "Pareto principle"},
            {"key": "B", "text": "Pairwise principle"},
            {"key": "C", "text": "Partition principle"},
            {"key": "D", "text": "Parametric principle"},
        ],
        "A",
        "Project Management",
    )
    questions[72] = _as_question(
        72,
        "Which method has the same name as that of its class?",
        [
            {"key": "A", "text": "Constructor"},
            {"key": "B", "text": "Class"},
            {"key": "C", "text": "Delete"},
            {"key": "D", "text": "Finalize"},
        ],
        "A",
        "Java / OOP",
    )
    questions[74] = _as_question(
        74,
        "You are required to write a program that iteratively takes 50 numbers from user input and adds them up "
        "only if the numbers are positive and skips if not. Which control structure best fits this scenario?",
        [
            {"key": "A", "text": "for"},
            {"key": "B", "text": "break"},
            {"key": "C", "text": "jump"},
            {"key": "D", "text": "continue"},
        ],
        "D",
        "C++",
    )
    questions[75] = _as_question(
        75,
        "Which statement is correct about the differences between functional and non-functional requirements?",
        [
            {
                "key": "A",
                "text": "Functional requirements are services the system provides; non-functional requirements are constraints on those services",
            },
            {"key": "B", "text": "Functional requirements are decided by customer; non-functional by developers"},
            {"key": "C", "text": "Both are the same most of the time"},
            {"key": "D", "text": "Unlike functional requirements, non-functional requirements are stable"},
        ],
        "A",
        "Software Engineering",
    )
    questions[76] = _as_question(
        76,
        "Select an activity that suits the fundamental test process which includes evaluation of the testability "
        "of the requirements and system:",
        [
            {"key": "A", "text": "Test analysis and requirements"},
            {"key": "B", "text": "Test analysis and design"},
            {"key": "C", "text": "Test analysis and planning"},
            {"key": "D", "text": "Test analysis and implementation"},
        ],
        "B",
        "Software Testing",
    )
    questions[77] = _as_question(
        77,
        "What is the correct order of protocol data units in the OSI model from bottom to top?",
        [
            {"key": "A", "text": "Segment, packet, frame, bit"},
            {"key": "B", "text": "Segment, frame, packet, bit"},
            {"key": "C", "text": "Bit, packet, frame, segment"},
            {"key": "D", "text": "Bit, frame, packet, segment"},
        ],
        "D",
        "Networking",
    )
    questions[78] = _as_question(
        78,
        "Which learning algorithm is usually applied to data that does not contain any label information?",
        [
            {"key": "A", "text": "Reinforcement learning"},
            {"key": "B", "text": "Unsupervised learning"},
            {"key": "C", "text": "Transfer learning"},
            {"key": "D", "text": "Supervised learning"},
        ],
        "B",
        "AI / ML",
    )
    questions[79] = _as_question(
        79,
        (
            "Assume you are designing a dormitory management database. DORM(DormID, FloorNumber) has DormID as "
            "primary key. STUDENT(IDNo, Name, Department) has IDNo as primary key. Which SQL statement correctly "
            "establishes the relationship when DormID is a foreign key in STUDENT?"
        ),
        [
            {"key": "A", "text": "ALTER TABLE DORM ADD FOREIGN KEY (DormID) REFERENCES STUDENT(IDNo)"},
            {"key": "B", "text": "ALTER TABLE STUDENT ADD FOREIGN KEY (DormID) REFERENCES DORM(DormID)"},
            {"key": "C", "text": "ALTER TABLE STUDENT ADD PRIMARY KEY (DormID) REFERENCES DORM(DormID)"},
            {"key": "D", "text": "ALTER TABLE DORM ADD CONSTRAINT DormID REFERENCES STUDENT(IDNo)"},
        ],
        "B",
        "Database",
    )
    questions[80] = _as_question(
        80,
        (
            "The result of the following program after running will be:\n\n"
            "class PrintResult {\n"
            "    public static void main(String[] args) {\n"
            "        int[] arr = {3, 4, 5, 6, 7};\n"
            "        for (int i = 0; i < arr.length - 1; i++)\n"
            "            System.out.print(arr[i]);\n"
            "    }\n"
            "}"
        ),
        [
            {"key": "A", "text": "34567"},
            {"key": "B", "text": "3456"},
            {"key": "C", "text": "34"},
            {"key": "D", "text": "345"},
        ],
        "B",
        "Java / OOP",
    )
    questions[81] = _as_question(
        81,
        "Which parameter is used to assess and evaluate software architectures?",
        [
            {"key": "A", "text": "Number of components in the architecture"},
            {"key": "B", "text": "Durability of the architecture"},
            {"key": "C", "text": "Responsiveness of the architecture"},
            {"key": "D", "text": "Architectural quality attributes"},
        ],
        "D",
        "Software Architecture",
    )
    questions[82] = _as_question(
        82,
        "Which statement is correct about Artificial Intelligence (AI)?",
        [
            {"key": "A", "text": "It refers to machines that perform tasks only in a controlled laboratory setting"},
            {"key": "B", "text": "It refers to machines that can only perform simple, repetitive tasks"},
            {"key": "C", "text": "It refers to machines that can only perform physical tasks"},
            {
                "key": "D",
                "text": "It refers to machines that can perform tasks that typically require human intelligence",
            },
        ],
        "D",
        "AI / ML",
    )
    questions[83] = _as_question(
        83,
        "In software risk management, accepting that a risk may happen without taking action is known as:",
        [
            {"key": "A", "text": "Risk transfer"},
            {"key": "B", "text": "Risk retention"},
            {"key": "C", "text": "Risk reduction"},
            {"key": "D", "text": "Risk avoidance"},
        ],
        "B",
        "Security",
    )
    questions[84] = _as_question(
        84,
        "Which activity comes last in fundamental program development in C++?",
        [
            {"key": "A", "text": "Compiling program"},
            {"key": "B", "text": "Writing program"},
            {"key": "C", "text": "Memory allocation for variables"},
            {"key": "D", "text": "Linking"},
        ],
        "D",
        "C++",
    )
    questions[88] = _as_question(
        88,
        "Default method while submitting a form is:",
        [
            {"key": "A", "text": "Get method"},
            {"key": "B", "text": "Set method"},
            {"key": "C", "text": "Post method"},
            {"key": "D", "text": "Put method"},
        ],
        "A",
        "Web Development",
    )
    questions[89] = _as_question(
        89,
        "Which software process model will you use if you want to deliver different functionalities (modules) "
        "of the software product that have different priority at different times?",
        [
            {"key": "A", "text": "Waterfall model"},
            {"key": "B", "text": "Spiral model"},
            {"key": "C", "text": "Incremental model"},
            {"key": "D", "text": "Linear model"},
        ],
        "C",
        "Software Engineering",
    )
    questions[90] = _as_question(
        90,
        "Identify the lowest layer of Android architecture.",
        [
            {"key": "A", "text": "Application"},
            {"key": "B", "text": "Application Framework"},
            {"key": "C", "text": "Database"},
            {"key": "D", "text": "Linux Kernel"},
        ],
        "D",
        "Android",
    )
    questions[91] = _as_question(
        91,
        "Which of the following is a resource optimization technique in which start and finish dates are adjusted "
        "based on resource constraints with the goal of balancing demand for resources with available supply?",
        [
            {"key": "A", "text": "Resource smoothing"},
            {"key": "B", "text": "Responsibility assignment matrix"},
            {"key": "C", "text": "Resource leveling"},
            {"key": "D", "text": "Resource grouping"},
        ],
        "C",
        "Project Management",
    )
    questions[92] = _as_question(
        92,
        "Which of the following is not an approach used by IT security specialists to enhance the security level of the network?",
        [
            {"key": "A", "text": "Use of Intrusion Detection System"},
            {"key": "B", "text": "Use of Intrusion Prevention System"},
            {"key": "C", "text": "Use of WannaCry protocol"},
            {"key": "D", "text": "Use of physical security"},
        ],
        "C",
        "Security",
    )
    questions[93] = _as_question(
        93,
        "APK stands for:",
        [
            {"key": "A", "text": "Android Phone Kit"},
            {"key": "B", "text": "Android Page Kit"},
            {"key": "C", "text": "Android Platform Kit"},
            {"key": "D", "text": "Android Package Kit"},
        ],
        "D",
        "Android",
    )
    questions[94] = _as_question(
        94,
        "A technique for generating plans with conditionals and loops that is almost identical to those for "
        "generating programs from logical specifications is called:",
        [
            {"key": "A", "text": "Automatic learning"},
            {"key": "B", "text": "Automatic recursive"},
            {"key": "C", "text": "Automatic monitoring"},
            {"key": "D", "text": "Automatic programming"},
        ],
        "D",
        "AI / ML",
    )
    questions[95] = _as_question(
        95,
        "Identify the one that comes first in the data mining process.",
        [
            {"key": "A", "text": "Business understanding"},
            {"key": "B", "text": "Data integration"},
            {"key": "C", "text": "Data cleaning"},
            {"key": "D", "text": "Data selection"},
        ],
        "A",
        "AI / ML",
    )
    questions[96] = _as_question(
        96,
        "Which one of the following is an appropriate sequence of database design processes?",
        [
            {"key": "A", "text": "Logical database design, Enterprise data modeling, Physical database design, Database implementation"},
            {"key": "B", "text": "Enterprise data modeling, Logical database design, Database implementation, Physical database design"},
            {"key": "C", "text": "Physical database design, Logical database design, Enterprise data modeling, Database implementation"},
            {"key": "D", "text": "Enterprise data modeling, Logical database design, Physical database design, Database implementation"},
        ],
        "D",
        "Database",
    )
    questions[97] = _as_question(
        97,
        "Identify the design principle that does not apply to software systems.",
        [
            {"key": "A", "text": "Design should be structured to accommodate change"},
            {"key": "B", "text": "Design should exhibit uniformity and integration"},
            {"key": "C", "text": "Design should be reinventing the wheel from scratch"},
            {"key": "D", "text": "Design should be traceable to the analysis model"},
        ],
        "C",
        "Software Engineering",
    )

    questions[35] = _as_question(
        35,
        "Which of the following specifies divergence between Dijkstra's Algorithm (DA) and Uniform Cost Search (UCS)?",
        [
            {"key": "A", "text": "DA first collects nodes into a queue; UCS discovers them as they come"},
            {"key": "B", "text": "DA is optimal, but UCS is not"},
            {"key": "C", "text": "DA discovers nodes as they come, while UCS first collects them in a queue"},
            {"key": "D", "text": "UCS finds the optimal solution while DA does not"},
        ],
        "C",
        "AI / ML",
    )
    questions[36] = _as_question(
        36,
        "What is an activity in Android?",
        [
            {"key": "A", "text": "A single screen in an application with supporting Java code"},
            {"key": "B", "text": "An Android class used to configure the Android application"},
            {"key": "C", "text": "It is an Intent"},
            {"key": "D", "text": "An Android package file holding all the packages used"},
        ],
        "A",
        "Android",
    )
    questions[3] = _as_question(
        3,
        "The process that generates activities such as project schedule, cost estimations and work breakdown structures is described as:",
        [
            {"key": "A", "text": "Project Executing"},
            {"key": "B", "text": "Project Initiating"},
            {"key": "C", "text": "Project Closing"},
            {"key": "D", "text": "Project Planning"},
        ],
        "D",
        "Project Management",
    )
    questions[33] = _as_question(
        33,
        "Given a situation where two hosts attempt on a half-duplex Ethernet LAN to send data concurrently, "
        "resulting in a collision, what will the hosts do subsequently?",
        [
            {"key": "A", "text": "An electrical pulse indicates that the collision has cleared"},
            {"key": "B", "text": "The router on the segment will signal that the collision has cleared"},
            {"key": "C", "text": "The jam signal indicates that the collision has been cleared"},
            {"key": "D", "text": "The hosts will attempt to resume transmission after a time delay has expired"},
        ],
        "D",
        "Networking",
    )

    questions[46] = _as_question(
        46,
        "Select the fundamental issue that may not be considered by software architects during the architectural design process:",
        [
            {"key": "A", "text": "Which architectural organization is best for delivering the functional requirements?"},
            {"key": "B", "text": "How the system will be distributed across a number of cores or processors"},
            {"key": "C", "text": "How to decompose structural components into sub-components"},
            {"key": "D", "text": "Which architectural patterns or styles to use"},
        ],
        "B",
        "Software Architecture",
    )
    questions[47] = _as_question(
        47,
        "Assume there is a Pet family from which pets like Dog and Cat share behavior. Every pet has a name. "
        "Only dogs can fetch while both cats and dogs can speak. Which OOP principle fits this case?",
        [
            {"key": "A", "text": "Polymorphism"},
            {"key": "B", "text": "Encapsulation"},
            {"key": "C", "text": "Inheritance"},
            {"key": "D", "text": "Information hiding"},
        ],
        "C",
        "Java / OOP",
    )
    questions[48] = _as_question(
        48,
        "Which of the following analysis mechanisms defines the input for which the algorithm takes the least time?",
        [
            {"key": "A", "text": "Standard case"},
            {"key": "B", "text": "Average case"},
            {"key": "C", "text": "Worst case"},
            {"key": "D", "text": "Best case"},
        ],
        "D",
        "Data Structures",
    )
    questions[49] = _as_question(
        49,
        "Which one of the following is not among the characterizing features of the database approach?",
        [
            {"key": "A", "text": "Sharing of data"},
            {"key": "B", "text": "Application-data dependency"},
            {"key": "C", "text": "Self-describing"},
            {"key": "D", "text": "Data abstraction"},
        ],
        "B",
        "Database",
    )
    questions[55] = _as_question(
        55,
        "Which of the following statements is not true regarding project life cycle?",
        [
            {
                "key": "A",
                "text": "In agile life cycles the project scope cannot be outlined and agreed before the start of iteration",
            },
            {
                "key": "B",
                "text": "In a waterfall life cycle the project scope, time, and cost are determined in the early phases",
            },
            {
                "key": "C",
                "text": "In agile life cycle the project scope is generally determined early but time and cost estimates are routinely modified",
            },
            {
                "key": "D",
                "text": "In an incremental life cycle, deliverables are produced through iterations that successively add functionality",
            },
        ],
        "A",
        "Project Management",
    )
    questions[85] = _as_question(
        85,
        (
            "Consider the following program:\n\n"
            "import java.util.Scanner;\n"
            "public class Test {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            '        System.out.println("Enter choice");\n'
            "        int choice = scanner.nextInt();\n"
            "        switch (choice) {\n"
            '            case 1: System.out.println("Hello");\n'
            '            case 2: System.out.println("You");\n'
            '                      System.out.println("welcome");\n'
            "                      break;\n"
            '            default: System.out.println("Goodbye");\n'
            "        }\n"
            "    }\n"
            "}\n\n"
            "If you enter 1 as your choice, what will be the output?"
        ),
        [
            {"key": "A", "text": "Hello"},
            {"key": "B", "text": "Hello You welcome"},
            {"key": "C", "text": "Hello You welcome Goodbye"},
            {"key": "D", "text": "Hello Goodbye"},
        ],
        "B",
        "Java / OOP",
    )
    questions[86] = _as_question(
        86,
        "The correct structure of the for loop statement in C++ is:",
        [
            {"key": "A", "text": "for(initialization; condition; increment/decrement)"},
            {"key": "B", "text": "for(condition, initialization, increment/decrement)"},
            {"key": "C", "text": "for[initialization; condition]"},
            {"key": "D", "text": "for(increment/decrement; initialization; condition)"},
        ],
        "D",
        "C++",
    )
    questions[87] = _as_question(
        87,
        "Which one of the following is the correct identifier in C++?",
        [
            {"key": "A", "text": "7variable"},
            {"key": "B", "text": "7VARIABLE"},
            {"key": "C", "text": "$variable"},
            {"key": "D", "text": "variable_1234"},
        ],
        "D",
        "C++",
    )

    questions[1] = _as_question(
        1,
        "Which of the following is wrong regarding interface?",
        [
            {"key": "A", "text": "Interface abstract methods are accessed using interface instances"},
            {"key": "B", "text": "Like a class, an interface is a reference data type"},
            {"key": "C", "text": "Interface includes abstract methods"},
            {"key": "D", "text": "One class can implement multiple interfaces"},
        ],
        "A",
        "Java / OOP",
    )
    questions[2] = _as_question(
        2,
        "How can we select an element with a specific class in CSS?",
        [
            {"key": "A", "text": ".classname"},
            {"key": "B", "text": "#classname"},
            {"key": "C", "text": "element.class"},
            {"key": "D", "text": "class: element"},
        ],
        "A",
        "Web Development",
    )
    questions[10] = _as_question(
        10,
        "Which slogan is against the agile method philosophy?",
        [
            {"key": "A", "text": "Working software over comprehensive documentation"},
            {"key": "B", "text": "Following a plan over responding to changes"},
            {"key": "C", "text": "Individuals and interactions over processes and tools"},
            {"key": "D", "text": "Customer collaboration over contract negotiation"},
        ],
        "B",
        "Project Management",
    )
    questions[12] = _as_question(
        12,
        "What would be the most likely consequence if every software stakeholder were rushing to be approved "
        "for their requirements without discussing with other stakeholders?",
        [
            {"key": "A", "text": "Results in excess requirement"},
            {"key": "B", "text": "Attains the project schedule"},
            {"key": "C", "text": "Requirements become unambiguous"},
            {"key": "D", "text": "Leads to conflicting requirement"},
        ],
        "D",
        "Project Management",
    )
    questions[13] = _as_question(
        13,
        'When a process is in a "Blocked" state waiting for some Input-Output services and after the service '
        "is completed, it will go to a state known as:",
        [
            {"key": "A", "text": "Terminated"},
            {"key": "B", "text": "Suspended"},
            {"key": "C", "text": "Ready"},
            {"key": "D", "text": "Running"},
        ],
        "C",
        "Operating Systems",
    )
    questions[15] = _as_question(
        15,
        "What is Manifest.xml in Android?",
        [
            {"key": "A", "text": "It has the information about activities in an application"},
            {"key": "B", "text": "It is an executable file of the application"},
            {"key": "C", "text": "It has information about layout in an application"},
            {"key": "D", "text": "It has all the information about an application"},
        ],
        "D",
        "Android",
    )
    questions[18] = _as_question(
        18,
        "Which of the following is not the function of Cross-over UTP cable?",
        [
            {"key": "A", "text": "To connect router to pc"},
            {"key": "B", "text": "To connect switch to switch"},
            {"key": "C", "text": "To connect switch to pc"},
            {"key": "D", "text": "To connect pc to pc"},
        ],
        "C",
        "Networking",
    )
    questions[22] = _as_question(
        22,
        "Depending on the organization of the elements, which of the following is a non-linear data structure?",
        [
            {"key": "A", "text": "Queues"},
            {"key": "B", "text": "Linked-list"},
            {"key": "C", "text": "Tree"},
            {"key": "D", "text": "Stack"},
        ],
        "C",
        "Data Structures",
    )
    questions[31] = _as_question(
        31,
        "Who is responsible for documenting faults found during the software development process?",
        [
            {"key": "A", "text": "Tester"},
            {"key": "B", "text": "Requirement engineer"},
            {"key": "C", "text": "Developer"},
            {"key": "D", "text": "Scrum master"},
        ],
        "A",
        "Software Testing",
    )
    questions[32] = _as_question(
        32,
        "Which of the following statements is not addressing the banker's algorithm?",
        [
            {"key": "A", "text": "It is a scheduling algorithm"},
            {"key": "B", "text": "It is modeled on how a banker deals with customers granted lines of credit"},
            {"key": "C", "text": "It is an extension of the deadlock detection algorithm"},
            {"key": "D", "text": "The banker's algorithm considers each request before it occurs"},
        ],
        "A",
        "Operating Systems",
    )
    questions[37] = _as_question(
        37,
        "Which is the appropriate sequence in model development process in data mining?",
        [
            {"key": "A", "text": "Model Training, Model Evaluation, Model Testing, Model Deployment"},
            {"key": "B", "text": "Model Training, Model Testing, Model Deployment, Model Evaluation"},
            {"key": "C", "text": "Model Training, Model Testing, Model Evaluation, Model Deployment"},
            {"key": "D", "text": "Model Evaluation, Model Training, Model Testing, Model Deployment"},
        ],
        "C",
        "AI / ML",
    )
    questions[38] = _as_question(
        38,
        "What will be the output of the following code snippet?\n\n"
        '<script type="text/javascript">\n'
        '  var a = "exitexam";\n'
        "  var result = a.substring(2, 6);\n"
        "  document.write(result);\n"
        "</script>",
        [
            {"key": "A", "text": "xitex"},
            {"key": "B", "text": "texam"},
            {"key": "C", "text": "itex"},
            {"key": "D", "text": "xite"},
        ],
        "C",
        "Web Development",
    )
    questions[45] = _as_question(
        45,
        "A set of processes waiting for a resource that is owned by another process refers to:",
        [
            {"key": "A", "text": "Deadlock"},
            {"key": "B", "text": "Queuing"},
            {"key": "C", "text": "Preemption"},
            {"key": "D", "text": "Overloading"},
        ],
        "A",
        "Operating Systems",
    )
    questions[50] = _as_question(
        50,
        "Anything that can perceive its environment through sensors and acts upon the environment through effectors is:",
        [
            {"key": "A", "text": "API"},
            {"key": "B", "text": "Expert System"},
            {"key": "C", "text": "Intelligence"},
            {"key": "D", "text": "Agent"},
        ],
        "D",
        "AI / ML",
    )
    questions[51] = _as_question(
        51,
        "Select the one that is not related with the purpose of properly documenting software architectures:",
        [
            {"key": "A", "text": "To know how the system is organized and interoperates"},
            {"key": "B", "text": "For stakeholder communication"},
            {"key": "C", "text": "For critical system design decisions"},
            {"key": "D", "text": "To easily figure out the source code flow"},
        ],
        "D",
        "Software Architecture",
    )
    questions[57] = _as_question(
        57,
        "Which of the following refers to unauthorized disclosure of information?",
        [
            {"key": "A", "text": "Integrity"},
            {"key": "B", "text": "Authorization"},
            {"key": "C", "text": "Confidentiality"},
            {"key": "D", "text": "Authentication"},
        ],
        "C",
        "Security",
    )
    questions[59] = _as_question(
        59,
        "Which of the following is among benefits provided with access control lists (ACLs) implementation "
        "for software security based applications?",
        [
            {"key": "A", "text": "Virus detection"},
            {"key": "B", "text": "ACLs classify and organize network traffic"},
            {"key": "C", "text": "ACLs provide high network availability"},
            {"key": "D", "text": "ACLs monitor the number of bytes and packets"},
        ],
        "C",
        "Security",
    )
    questions[62] = _as_question(
        62,
        "As a software tester, when do you implement configuration management procedures?",
        [
            {"key": "A", "text": "During test execution"},
            {"key": "B", "text": "During test closing"},
            {"key": "C", "text": "During test initiation"},
            {"key": "D", "text": "During test planning"},
        ],
        "D",
        "Software Testing",
    )
    questions[67] = _as_question(
        67,
        "What will be the output for the following code if you enter 4 and 3 for b and e respectively?\n\n"
        "#include <iostream>\n"
        "using namespace std;\n"
        "int main() {\n"
        "    int b, e, r = 1;\n"
        '    cout << "Enter b and e";\n'
        "    cin >> b >> e;\n"
        "    for (int i = 1; i <= e; i++)\n"
        "        r = r * b;\n"
        "    cout << r;\n"
        "    return 0;\n"
        "}",
        [
            {"key": "A", "text": "81"},
            {"key": "B", "text": "256"},
            {"key": "C", "text": "12"},
            {"key": "D", "text": "64"},
        ],
        "D",
        "C++",
    )
    questions[73] = _as_question(
        73,
        "Which software development model best fits environments where requirements change frequently?",
        [
            {"key": "A", "text": "Code-and-run model"},
            {"key": "B", "text": "Spiral model"},
            {"key": "C", "text": "Agile development method"},
            {"key": "D", "text": "Waterfall model"},
        ],
        "C",
        "Project Management",
    )

    missing = [i for i in range(1, 98) if i not in questions]
    if missing:
        raise ValueError(f"Missing curated definitions for questions: {missing}")


def build_exam2016_curated() -> list[dict]:
    questions = _load_initial_questions()
    _apply_required_corrections(questions)
    ordered = [questions[i] for i in range(1, 98)]

    if len(ordered) != 97:
        raise ValueError(f"Expected 97 questions, got {len(ordered)}")
    if [q["id"] for q in ordered] != list(range(1, 98)):
        raise ValueError("Question ids must be exactly 1..97")

    return ordered


QUESTIONS_2016_CURATED = build_exam2016_curated()


if __name__ == "__main__":
    print(json.dumps(QUESTIONS_2016_CURATED, indent=2, ensure_ascii=False))
