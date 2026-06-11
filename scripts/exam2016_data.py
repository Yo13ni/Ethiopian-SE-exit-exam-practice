"""2016 Software Engineering Exit Exam — OCR fixes and extra questions (91–100)."""

from __future__ import annotations

FOCUS_GUIDE: dict[str, str] = {
    "Networking": "Review OSI/TCP-IP layers, subnetting, switches vs hubs, HTTP, and network security basics.",
    "Project Management": "Study agile vs waterfall, WBS, stakeholder management, Tuckman model, and ROI.",
    "Database": "Practice normalization (1NF–3NF), SQL INSERT/FOREIGN KEY, and ER-to-relational mapping.",
    "Web Development": "Review HTML/CSS selectors, HTTP methods (GET/POST), and JavaScript fundamentals.",
    "Java / OOP": "Focus on interfaces, abstract classes, inheritance, try-catch, and correct Java syntax.",
    "Android": "Study Activity, Intent, Manifest.xml, layout hierarchy (ViewGroup), and APK.",
    "Operating Systems": "Review process states, deadlock/banker's algorithm, paging, and CPU scheduling.",
    "AI / ML": "Study search algorithms (A*, UCS), agent types, and data mining CRISP-DM phases.",
    "Software Testing": "Review test planning, coverage types, traceability, and fundamental test process activities.",
    "Software Architecture": "Study layered architecture, microservices/API gateway, quality attributes, and architecture documentation.",
    "Security": "Focus on CIA triad, ACLs, risk management, and common attack mitigations.",
    "Data Structures": "Practice time complexity, linear vs non-linear structures, and queue/stack use cases.",
    "C++": "Review for-loop syntax, valid identifiers, and basic I/O.",
    "General": "Re-read missed questions and verify concepts in your course notes.",
}

# Keyed by question id (1–100). Only questions with bad OCR from exam.json.
QUESTION_FIXES: dict[int, dict] = {
    4: {
        "text": (
            "The following UML design shows a Student class. Assume that the attributes are "
            "declared as private and the methods as public. The get methods return the value of "
            "the attributes and calculateAge() returns the student's age.\n\n"
            "Student\n  - name : String\n  - department : String\n  - phone : String\n  - age : int\n"
            "  + Student(String, String, String, int)\n  + setDept(String)\n  + getName() : String\n"
            "  + getDept() : String\n  + getYearOfBirth() : int\n  + calculateAge() : int\n\n"
            "Which of the following would not raise an error when you run this program?"
        ),
        "options": [
            {"key": "A", "text": 'Student st1 = new Student("John", "CS", 2000);'},
            {"key": "B", "text": 'Student st1 = new Student("John", "CS", "0911223344", "2000");'},
            {"key": "C", "text": 'Student st1 = new Student("John", 23, "CS", 2000);'},
            {"key": "D", "text": 'Student st1 = new Student("John", "CS", "0911223344", 2000);'},
        ],
        "answer": "D",
        "topic": "Java / OOP",
    },
    5: {
        "text": "Which of the following is not a valid host address within the network 172.17.128.0/21?",
        "options": [
            {"key": "A", "text": "172.17.128.1/21"},
            {"key": "B", "text": "172.17.135.255/21"},
            {"key": "C", "text": "172.17.135.0/21"},
            {"key": "D", "text": "172.17.128.255/21"},
        ],
        "answer": "B",
        "topic": "Networking",
    },
    6: {
        "text": "The permission -rwxr-xr-x represented in octal expression will be:",
        "options": [
            {"key": "A", "text": "744"},
            {"key": "B", "text": "700"},
            {"key": "C", "text": "755"},
            {"key": "D", "text": "766"},
        ],
        "answer": "C",
        "topic": "Operating Systems",
    },
    8: {
        "text": "An HTTP request message always contains:",
        "options": [
            {"key": "A", "text": "A header only"},
            {"key": "B", "text": "A header and a body"},
            {"key": "C", "text": "A status line, a header, and a body"},
            {"key": "D", "text": "A request line and a header"},
        ],
        "answer": "D",
        "topic": "Networking",
    },
    14: {
        "text": (
            "A memory management policy in which decisions must be made as to which page or "
            "pages are to be replaced when memory is full is known as:"
        ),
        "options": [
            {"key": "A", "text": "Cleaning policy"},
            {"key": "B", "text": "Fetch policy"},
            {"key": "C", "text": "Load policy"},
            {"key": "D", "text": "Replacement policy"},
        ],
        "answer": "D",
        "topic": "Operating Systems",
    },
    19: {
        "text": "Within OAuth, what component validates the user's identity?",
        "options": [
            {"key": "A", "text": "Authorization Server"},
            {"key": "B", "text": "Resource Server"},
            {"key": "C", "text": "Client"},
            {"key": "D", "text": "Browser"},
        ],
        "answer": "A",
        "topic": "Security",
    },
    20: {
        "text": (
            "If the estimate for total discounted benefits for a project is Birr 120,000 and "
            "total discounted cost is Birr 100,000, what is the estimated return on investment "
            "(ROI) percentage?"
        ),
        "options": [
            {"key": "A", "text": "20%"},
            {"key": "B", "text": "10%"},
            {"key": "C", "text": "12%"},
            {"key": "D", "text": "16.67%"},
        ],
        "answer": "A",
        "topic": "Project Management",
    },
    21: {
        "text": (
            "Given the following layered architecture, which ordering relation is correct and "
            "does not encounter architectural erosion? Assume there are four layers: A, B, C, and D."
        ),
        "options": [
            {"key": "A", "text": "Layer A may call layer B; layer B may call layer C; layer C may call layer D"},
            {"key": "B", "text": "Layer A may call layer C directly; layer B may call layer D"},
            {"key": "C", "text": "Layer D may call layer A; layer C may call layer B"},
            {"key": "D", "text": "Layer A may call any lower layer without restriction"},
        ],
        "answer": "A",
        "topic": "Software Engineering",
    },
    23: {
        "text": (
            "What is the time complexity of the following function?\n\n"
            "public void function(int n) {\n"
            "    for (int i = 0; i < n; i++)\n"
            "        for (int j = i; j < n; j++)\n"
            "            for (int k = 0; k < j; k++)\n"
            "                printf(\"*\");\n"
            "}"
        ),
        "options": [
            {"key": "A", "text": "O(n^5)"},
            {"key": "B", "text": "O(n^7)"},
            {"key": "C", "text": "O(n^3)"},
            {"key": "D", "text": "O(n log n)"},
        ],
        "answer": "C",
        "topic": "Data Structures",
    },
    26: {
        "text": "All layout classes are subclasses of which of the following?",
        "options": [
            {"key": "A", "text": "android.view.Layout"},
            {"key": "B", "text": "android.view.RelativeLayout"},
            {"key": "C", "text": "android.view.ViewGroup"},
            {"key": "D", "text": "android.view.Widget"},
        ],
        "answer": "C",
        "topic": "Android",
    },
    27: {
        "text": "Which one of the following is not true regarding algorithm development during problem solving?",
        "options": [
            {"key": "A", "text": "It is a step-wise logical description of how to solve the problem"},
            {"key": "B", "text": "It is equivalent to the programming language code"},
            {"key": "C", "text": "It should be developed by considering the platforms on which it runs"},
            {"key": "D", "text": "It is developed considering the details of the programming language"},
        ],
        "answer": "D",
        "topic": "Data Structures",
    },
    35: {
        "text": "What is an activity in Android?",
        "options": [
            {"key": "A", "text": "A single screen in an application with supporting Java code"},
            {"key": "B", "text": "An Android class used to configure the Android application"},
            {"key": "C", "text": "It is an Intent"},
            {"key": "D", "text": "An Android package file holding all the packages used"},
        ],
        "answer": "A",
        "topic": "Android",
    },
    37: {
        "text": (
            "What will be the output of the following code snippet?\n\n"
            '<script type="text/javascript">\n'
            '  var a = "exitexam";\n'
            "  var result = a.substring(2, 6);\n"
            "  document.write(result);\n"
            "</script>"
        ),
        "options": [
            {"key": "A", "text": "xitex"},
            {"key": "B", "text": "texam"},
            {"key": "C", "text": "itex"},
            {"key": "D", "text": "xite"},
        ],
        "answer": "C",
        "topic": "Web Development",
    },
    38: {
        "text": (
            "What is the time complexity for the following code snippet?\n\n"
            "function someFunction(n) {\n"
            "  for (var i = n; i >= 1; i = i / 2) {\n"
            "    console.log(n);\n"
            "  }\n"
            "}"
        ),
        "options": [
            {"key": "A", "text": "O(n)"},
            {"key": "B", "text": "O(log n)"},
            {"key": "C", "text": "O(n log n)"},
            {"key": "D", "text": "O(1)"},
        ],
        "answer": "B",
        "topic": "Data Structures",
    },
    39: {
        "text": (
            "While optimizing our relation, if we found that no multivalued attributes and no "
            "partial dependencies exist in a relation, then the relation is in what normal form?"
        ),
        "options": [
            {"key": "A", "text": "2NF"},
            {"key": "B", "text": "4NF"},
            {"key": "C", "text": "1NF"},
            {"key": "D", "text": "3NF"},
        ],
        "answer": "A",
        "topic": "Database",
    },
    45: {
        "text": (
            "Select the fundamental issue that must be considered by software architects during "
            "the architectural design process."
        ),
        "options": [
            {"key": "A", "text": "Which architectural organization is best for delivering the functional requirements?"},
            {"key": "B", "text": "How the system will be distributed across a number of cores or processors"},
            {"key": "C", "text": "How to decompose structural components into sub-components"},
            {"key": "D", "text": "Which architectural patterns or styles to use"},
        ],
        "answer": "A",
        "topic": "Software Engineering",
    },
    47: {
        "text": (
            "Assume that there is a Pet family from which pets like Dog and Cat share behavior. "
            "Every pet family has a name. However, pet families have some specific behaviors that "
            "are exhibited by only particular pets. For instance, only dogs can fetch something while "
            "both cats and dogs can speak. Which object-oriented design principle would be suitable "
            "for this case?"
        ),
        "options": [
            {"key": "A", "text": "Polymorphism"},
            {"key": "B", "text": "Encapsulation"},
            {"key": "C", "text": "Inheritance"},
            {"key": "D", "text": "Information hiding"},
        ],
        "answer": "C",
        "topic": "Java / OOP",
    },
    52: {
        "text": "A TCP/IP layer which is responsible for addressing, path selection, and routing refers to:",
        "options": [
            {"key": "A", "text": "Transport Layer"},
            {"key": "B", "text": "Network Access Layer"},
            {"key": "C", "text": "Application Layer"},
            {"key": "D", "text": "Internet Layer"},
        ],
        "answer": "D",
        "topic": "Networking",
    },
    53: {
        "text": (
            '"Database is a logically coherent collection of data with some inherent meaning" '
            "describes that:"
        ),
        "options": [
            {"key": "A", "text": "The entity should be a physical object"},
            {"key": "B", "text": "The number of attributes should be limited"},
            {"key": "C", "text": "There should be one primary key attribute"},
            {"key": "D", "text": "All attributes of the entity should be related"},
        ],
        "answer": "D",
        "topic": "Database",
    },
    54: {
        "text": (
            "Given the following fragment of code, how many tests are required for 100% decision coverage?\n\n"
            "if width > length then\n"
            "    biggest_dimension = width\n"
            "    if height > width then\n"
            "        biggest_dimension = height\n"
            "    end if\n"
            "else\n"
            "    biggest_dimension = length\n"
            "    if height > length then\n"
            "        biggest_dimension = height\n"
            "    end if\n"
            "end if"
        ),
        "options": [
            {"key": "A", "text": "2"},
            {"key": "B", "text": "3"},
            {"key": "C", "text": "4"},
            {"key": "D", "text": "6"},
        ],
        "answer": "D",
        "topic": "Software Engineering",
    },
    55: {
        "text": "Which of the following statements is not true regarding project life cycle?",
        "options": [
            {
                "key": "A",
                "text": (
                    "In agile life cycles the project scope cannot be outlined and agreed before "
                    "the start of iteration"
                ),
            },
            {
                "key": "B",
                "text": (
                    "In a waterfall life cycle the project scope, time, and cost are determined "
                    "in the early phases of the life cycle"
                ),
            },
            {
                "key": "C",
                "text": (
                    "In agile life cycle the project scope is generally determined early in the "
                    "project life cycle, but time and cost estimates are routinely modified"
                ),
            },
            {
                "key": "D",
                "text": (
                    "In an incremental life cycle, the deliverable is produced through a series of "
                    "iterations that successively add functionality within a predetermined time frame"
                ),
            },
        ],
        "answer": "A",
        "topic": "Project Management",
    },
    58: {
        "text": (
            "Which of the following is among benefits provided with access control lists (ACLs) "
            "implementation for software security based applications?"
        ),
        "options": [
            {"key": "A", "text": "Virus detection"},
            {"key": "B", "text": "ACLs provide high network availability"},
            {"key": "C", "text": "ACLs classify and organize network traffic"},
            {"key": "D", "text": "ACLs monitor the number of bytes and packets"},
        ],
        "answer": "C",
        "topic": "Security",
    },
    59: {
        "text": (
            "Which of the following shows the five stages in Tuckman's model of team development, "
            "in sequential order?"
        ),
        "options": [
            {"key": "A", "text": "Forming, storming, performing, norming, and adjourning"},
            {"key": "B", "text": "Forming, storming, norming, performing, and adjourning"},
            {"key": "C", "text": "Norming, forming, storming, performing, and adjourning"},
            {"key": "D", "text": "Storming, forming, norming, performing, and adjourning"},
        ],
        "answer": "B",
        "topic": "Project Management",
    },
    63: {
        "text": (
            '"The system architecture should be designed using fine-grain, self-contained '
            "components. Producers of data should be separated from consumers and shared data "
            'structures should be avoided." For which requirement does this architecture description apply?'
        ),
        "options": [
            {"key": "A", "text": "Performance"},
            {"key": "B", "text": "Availability"},
            {"key": "C", "text": "Maintainability"},
            {"key": "D", "text": "Security"},
        ],
        "answer": "C",
        "topic": "Software Engineering",
    },
    64: {
        "text": (
            "For the schema HOTEL (Hotel_id: integer, Hotel_Name: string, Sub_city: string), "
            "which SQL statement correctly inserts tuples into the HOTEL relation? "
            "(Assume Hotel_id is the primary key.)"
        ),
        "options": [
            {"key": "A", "text": "INSERT INTO HOTEL VALUES('Hilton','Yeka');"},
            {"key": "B", "text": "INSERT INTO HOTEL VALUES;"},
            {"key": "C", "text": "INSERT VALUES INTO HOTEL(Hotel_id, Hotel_Name, Sub_city);"},
            {
                "key": "D",
                "text": (
                    "INSERT INTO HOTEL(Hotel_id, Hotel_Name, Sub_city) "
                    "VALUES(1, 'Hilton', 'Yeka');"
                ),
            },
        ],
        "answer": "D",
        "topic": "Database",
    },
    66: {
        "text": (
            "Which of the following is a process of selecting program paths in such a manner that "
            "certain branches (i.e., outgoing edges of nodes) of a control flow graph are covered "
            "by the execution of those paths?"
        ),
        "options": [
            {"key": "A", "text": "Branch boundary"},
            {"key": "B", "text": "Branch coverage"},
            {"key": "C", "text": "Branch control"},
            {"key": "D", "text": "Branch expansion"},
        ],
        "answer": "B",
        "topic": "Software Engineering",
    },
    71: {
        "text": "Which method has the same name as that of its class?",
        "options": [
            {"key": "A", "text": "Constructor"},
            {"key": "B", "text": "Class"},
            {"key": "C", "text": "Delete"},
            {"key": "D", "text": "Finalize"},
        ],
        "answer": "A",
        "topic": "Java / OOP",
    },
    73: {
        "text": (
            "You are required to write a program that iteratively takes 50 numbers from user input "
            "and adds them up only if the numbers are positive and skips if not. Which control "
            "structure best fits this scenario?"
        ),
        "options": [
            {"key": "A", "text": "for"},
            {"key": "B", "text": "break"},
            {"key": "C", "text": "jump"},
            {"key": "D", "text": "continue"},
        ],
        "answer": "D",
        "topic": "General",
    },
    79: {
        "text": (
            "The result of the following program after running will be:\n\n"
            "class PrintResult {\n"
            "    public static void main(String[] args) {\n"
            "        int[] g = {3, 4, 5, 6, 7};\n"
            "        for (int i = 0; i < g.length - 1; i++)\n"
            "            System.out.print(g[i]);\n"
            "    }\n"
            "}"
        ),
        "options": [
            {"key": "A", "text": "34567"},
            {"key": "B", "text": "3456"},
            {"key": "C", "text": "34"},
            {"key": "D", "text": "345"},
        ],
        "answer": "B",
        "topic": "Java / OOP",
    },
    84: {
        "text": (
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
            "            default: System.out.println(\"Goodbye\");\n"
            "        }\n"
            "    }\n"
            "}\n\n"
            "If you run the above program and enter 1 as your choice, what will be the output?"
        ),
        "options": [
            {"key": "A", "text": "Hello"},
            {"key": "B", "text": "Hello You welcome"},
            {"key": "C", "text": "Hello You Welcome Goodbye"},
            {"key": "D", "text": "Hello Goodbye"},
        ],
        "answer": "B",
        "topic": "Java / OOP",
    },
    85: {
        "text": "The correct structure of the for loop statement in C++ is:",
        "options": [
            {"key": "A", "text": "for(initialization; condition; increment/decrement)"},
            {"key": "B", "text": "for(condition, initialization, increment/decrement)"},
            {"key": "C", "text": "for[initialization; condition]"},
            {"key": "D", "text": "for(increment/decrement; initialization; condition)"},
        ],
        "answer": "A",
        "topic": "C++",
    },
    86: {
        "text": "Which one of the following is the correct identifier in C++?",
        "options": [
            {"key": "A", "text": "7variable"},
            {"key": "B", "text": "7VARIABLE"},
            {"key": "C", "text": "Svariable"},
            {"key": "D", "text": "variable_1234"},
        ],
        "answer": "D",
        "topic": "C++",
    },
    96: {
        "text": "Identify the design principle that does not apply to software systems.",
        "options": [
            {"key": "A", "text": "Design should be structured to accommodate change"},
            {"key": "B", "text": "Design should exhibit uniformity and integration"},
            {"key": "C", "text": "Design should be reinventing the wheel from scratch"},
            {"key": "D", "text": "Design should be traceable to the analysis model"},
        ],
        "answer": "C",
        "topic": "Software Engineering",
    },
}

# Questions 91–100 from PDF pages 91–100 (not in the 90-question exam.json set).
# Each tuple: (text, [(A, text), (B, text), (C, text), (D, text)], answer, topic)
EXTRA_QUESTIONS: list[tuple] = [
    (
        "Default method while submitting a form is:",
        [
            ("A", "Get method"),
            ("B", "Set method"),
            ("C", "Post method"),
            ("D", "Put method"),
        ],
        "A",
        "Web Development",
    ),
    (
        "Which software process model will you use if you want to deliver different functionalities "
        "(modules) of the software product that have different priority at different times?",
        [
            ("A", "Waterfall model"),
            ("B", "Spiral model"),
            ("C", "Incremental model"),
            ("D", "Linear model"),
        ],
        "C",
        "Software Engineering",
    ),
    (
        "Identify the lowest layer of Android architecture.",
        [
            ("A", "Application"),
            ("B", "Application Framework"),
            ("C", "Database"),
            ("D", "Linux Kernel"),
        ],
        "D",
        "Android",
    ),
    (
        "Which of the following is a resource optimization technique in which start and finish dates "
        "are adjusted based on resource constraints with the goal of balancing the demand for "
        "resources with the available supply?",
        [
            ("A", "Resource smoothing"),
            ("B", "Responsibility assignment matrix"),
            ("C", "Resource leveling"),
            ("D", "Resource grouping"),
        ],
        "C",
        "Project Management",
    ),
    (
        "Which of the following is not an approach used by IT security specialists to enhance the "
        "security level of the network?",
        [
            ("A", "Use of Intrusion Detection System"),
            ("B", "Use of Intrusion Prevention System"),
            ("C", "Use of WannaCry protocol"),
            ("D", "Use of physical security"),
        ],
        "C",
        "Security",
    ),
    (
        "APK stands for:",
        [
            ("A", "Android Phone Kit"),
            ("B", "Android Page Kit"),
            ("C", "Android Platform Kit"),
            ("D", "Android Package Kit"),
        ],
        "D",
        "Android",
    ),
    (
        "A technique for generating plans with conditionals and loops that is almost identical to "
        "those for generating programs from logical specifications is called:",
        [
            ("A", "Automatic learning"),
            ("B", "Automatic recursive"),
            ("C", "Automatic monitoring"),
            ("D", "Automatic programming"),
        ],
        "D",
        "AI / ML",
    ),
    (
        "Identify the one that comes first in the data mining process.",
        [
            ("A", "Business understanding"),
            ("B", "Data integration"),
            ("C", "Data cleaning"),
            ("D", "Data selection"),
        ],
        "A",
        "AI / ML",
    ),
    (
        "Which one of the following is an appropriate sequence of database design processes?",
        [
            ("A", "Logical database design, Enterprise data modeling, Physical database design, Database implementation"),
            ("B", "Enterprise data modeling, Logical database design, Database implementation, Physical database design"),
            ("C", "Physical database design, Logical database design, Enterprise data modeling, Database implementation"),
            (
                "D",
                "Enterprise data modeling, Logical database design, Physical database design, Database implementation",
            ),
        ],
        "D",
        "Database",
    ),
    (
        "Identify the design principle that does not apply to software systems.",
        [
            ("A", "Design should be structured to accommodate change"),
            ("B", "Design should exhibit uniformity and integration"),
            ("C", "Design should be reinventing the wheel from scratch"),
            ("D", "Design should be traceable to the analysis model"),
        ],
        "C",
        "Software Engineering",
    ),
]
