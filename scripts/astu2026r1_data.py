"""ASTU 1st Round Model Exit Exam 2026 — question bank."""

from __future__ import annotations

FOCUS_GUIDE: dict[str, str] = {
    "C++": "Headers, pointers, arrays, recursion traces, file I/O, and scope rules.",
    "Data Structures": "Sorting stability, heaps, graphs, Big-O, and stack-based iteration.",
    "Java / OOP": "Encapsulation, aggregation, message passing, and Swing/BorderLayout behavior.",
    "Web Development": "HTML/CSS/JS, MVC, PWA, SOA, accessibility, and web security threats.",
    "Android": "Activities, resources, Profiler, layout_weight, sandboxing, and user consent.",
    "Database": "Three-schema architecture, EER, weak entities, conceptual/logical design, relations.",
    "Operating Systems": "Deadlock, fork(), microkernel vs hybrid, semaphores, and file metadata.",
    "Software Engineering": "Waterfall, architecture, design strategy, state machines, and quality metrics.",
    "Software Engineering (Requirements)": "RE purpose, scope, emergent properties, ambiguity, and scope creep.",
    "Software Architecture": "High-level structure, styles, availability, blackboard, and Strategy pattern.",
    "Project Management": "Triple constraint/CCB, risk vs incident, scope, float, and integration testing.",
    "Software Testing": "Testing goals, automation, model-based testing, re-testing, and state transitions.",
    "Software Maintenance": "Code smells, technical debt, regression testing, and servicing-stage changes.",
    "Networking": "OSI layers, subnetting, routers, HTTPS, UDP, and repeaters.",
    "Security": "SQL injection, honeypots, IDS features, hash integrity, and business continuity.",
    "AI / ML": "Rule-based limits, Turing Test, linear separability, regression, accuracy, and search.",
}


def TOPIC_BY_NUM(n: int) -> str:
    """Map question number (1–100) to topic based on PDF section headers."""
    if 1 <= n <= 11:
        return "C++"
    if 12 <= n <= 17:
        return "Data Structures"
    if 18 <= n <= 22:
        return "Java / OOP"
    if 23 <= n <= 31:
        return "Web Development"
    if 32 <= n <= 36:
        return "Android"
    if 37 <= n <= 42:
        return "Database"
    if 43 <= n <= 48:
        return "Operating Systems"
    if 49 <= n <= 54:
        return "Software Engineering"
    if 55 <= n <= 59:
        return "Software Engineering (Requirements)"
    if 60 <= n <= 64:
        return "Software Architecture"
    if 65 <= n <= 69:
        return "Project Management"
    if 70 <= n <= 74:
        return "Software Testing"
    if 75 <= n <= 79:
        return "Software Maintenance"
    if 80 <= n <= 85:
        return "Networking"
    if 86 <= n <= 90:
        return "Security"
    if 91 <= n <= 100:
        return "AI / ML"
    raise ValueError(f"Question number out of range: {n}")


# Each entry: (text, [(A,text), (B,text), (C,text), (D,text)], answer, topic)
RAW: list[tuple] = [
    (
        "Which one of the following is the correct syntax for including a user defined header "
        "files in C++?",
        [
            ("A", "#include (filename)"),
            ("B", "#include <filename.h>"),
            ("C", "#include <filename.h>"),
            ("D", '#include "filename"'),
        ],
        "D",
        "C++",
    ),
    (
        "At which phase of problem-solving life cycle are input data needed, "
        "procedure(process) and expected output requirements identified (determined) while "
        "solving a computational problem?",
        [
            ("A", "Analysis phase"),
            ("B", "Algorithm design phase"),
            ("C", "Testing phase"),
            ("D", "Implementation or coding phase"),
        ],
        "A",
        "C++",
    ),
    (
        "Which one of the following is the correct way of declaring a pointer p to the given array A?\n"
        "int A[]={12,-8,9,56};",
        [
            ("A", "int *p=&A;"),
            ("B", "int *p =A;"),
            ("C", "int &p=A;"),
            ("D", "double *p=A;"),
        ],
        "B",
        "C++",
    ),
    (
        "Choose the correct statement regarding class and object in C++.",
        [
            ("A", "An object is an instance of its class."),
            ("B", "A class is an instance of its object."),
            ("C", "An object is a blueprint of a class."),
            ("D", "A class is instantiated from its object."),
        ],
        "A",
        "C++",
    ),
    (
        "What would be the output of the following C++ code snippet?\n"
        "int x = 10;\n"
        "void test() {int x = 20; }\n"
        "int main(){test(); cout << x; }",
        [
            ("A", "10"),
            ("B", "20"),
            ("C", "Garbage"),
            ("D", "Error"),
        ],
        "A",
        "C++",
    ),
    (
        "Which of the following will correctly declare a constant symbolic value for PI in C++?",
        [
            ("A", "#define PI = 3.14"),
            ("B", "const float PI = 3.14;"),
            ("C", "constant PI = 3.14;"),
            ("D", "final float PI = 3.14;"),
        ],
        "B",
        "C++",
    ),
    (
        "What is the main difference between passing an array to a function by value vs. by pointer?",
        [
            ("A", "Arrays can only be passed by pointer, not by value"),
            ("B", "Passing by value creates a copy; passing by pointer does not"),
            ("C", "There is no difference in C++"),
            ("D", "Passing by pointer is slower than passing by value"),
        ],
        "B",
        "C++",
    ),
    (
        "What is the output of the following recursive function?\n"
        "int func(int n) {\n"
        "if(n == 0) return 0;\n"
        "if(n == 1) return 1;\n"
        "if(n % 2 == 0)\n"
        "return func(n/2);\n"
        "else\n"
        "return func(n/2) + func(n/2 + 1);\n"
        "}\n"
        "cout << func(7);",
        [
            ("A", "1"),
            ("B", "2"),
            ("C", "3"),
            ("D", "4"),
        ],
        "C",
        "C++",
    ),
    (
        "Consider this file pointer positioning:\n"
        'ofstream file("test.txt");\n'
        'file << "Hello World";\n'
        "file.seekp(6);\n"
        'file << "C++";\n'
        "file.close();\n"
        "What will be the content of test.txt?",
        [
            ("A", "Hello C++"),
            ("B", "Hello WorldC++"),
            ("C", "C++ World"),
            ("D", "Hello C++ld"),
        ],
        "D",
        "C++",
    ),
    (
        "Which of the following is NOT a correct initialization of an array?",
        [
            ("A", "int A[2][3]={1,2,3,4,5,6};"),
            ("B", "int A[2][3]={3,4,8,9};"),
            ("C", "int A[][]={1,2,3,4,5,6};"),
            ("D", "int array_name[2][3]={{1,2,3},{4,5,6}};"),
        ],
        "C",
        "C++",
    ),
    (
        "What does the following code output?\n"
        "#include <iostream>\n"
        "using namespace std;\n"
        "void increment(int arr[], int size) {\n"
        "for(int i=0;i<size;i++)\n"
        "(*(arr+i))++;\n"
        "}\n"
        "int main() {\n"
        "int data[3] = {2,4,6};\n"
        "increment(data,3);\n"
        "cout << data[0] << \" \" << data[1] << \" \" << data[2];\n"
        "return 0;\n"
        "}",
        [
            ("A", "2 4 6"),
            ("B", "3 5 7"),
            ("C", "1 3 5"),
            ("D", "Compiler error"),
        ],
        "B",
        "C++",
    ),
    (
        "Which of the following is not a stable sorting algorithm?",
        [
            ("A", "Merge Sort"),
            ("B", "Bubble Sort"),
            ("C", "Quick Sort"),
            ("D", "Insertion Sort"),
        ],
        "C",
        "Data Structures",
    ),
    (
        "Which of the following is the best-case time complexity of insertion sort?",
        [
            ("A", "O(n)"),
            ("B", "O(n log n)"),
            ("C", "O(n^2)"),
            ("D", "O(log n)"),
        ],
        "A",
        "Data Structures",
    ),
    (
        "Which of the following is used to find the shortest path in a weighted graph?",
        [
            ("A", "Depth First Search (DFS)"),
            ("B", "Breadth First Search (BFS)"),
            ("C", "Dijkstra's Algorithm"),
            ("D", "Bellman–Ford Algorithm"),
        ],
        "C",
        "Data Structures",
    ),
    (
        "Which of the following is not a property of a min-heap?",
        [
            ("A", "Complete binary tree"),
            ("B", "Parent is less than children"),
            ("C", "Root is the maximum"),
            ("D", "Efficient for priority queue"),
        ],
        "C",
        "Data Structures",
    ),
    (
        "Which of the following best describes the time complexity of a binary search algorithm "
        "in the worst-case scenario?",
        [
            ("A", "O(1)"),
            ("B", "O(n)"),
            ("C", "O(n^2)"),
            ("D", "O(log n)"),
        ],
        "D",
        "Data Structures",
    ),
    (
        "A recursive function is designed to perform a task, and you need to convert it into an "
        "iterative one. Which data structure is most commonly used to manage the function calls "
        "and local variables when transforming recursive algorithms into iterative ones?",
        [
            ("A", "Queue"),
            ("B", "Stack"),
            ("C", "Linked list"),
            ("D", "Priority queue"),
        ],
        "B",
        "Data Structures",
    ),
    (
        "Representing real-world entities (like students and courses) as classes that combine data "
        "(attributes) and behavior (methods) is an application of which principle?",
        [
            ("A", "Procedural abstraction"),
            ("B", "Functional decomposition"),
            ("C", "Object-oriented modeling"),
            ("D", "Algorithmic optimization"),
        ],
        "C",
        "Java / OOP",
    ),
    (
        "In an object-oriented system, an object sends a request to another object to perform a "
        "specific operation without knowing how that operation is implemented internally. This "
        "interaction helps reduce dependency between objects. Which concept best describes this "
        "form of interaction?",
        [
            ("A", "Data hiding"),
            ("B", "Message passing"),
            ("C", "Static binding"),
            ("D", "Direct data access"),
        ],
        "B",
        "Java / OOP",
    ),
    (
        "To improve the design of the Account class shown below, the developer wants to allow "
        "controlled access to the balance while still preserving data integrity.\n"
        "class Account { private double balance;}\n"
        "Which modification best supports this goal?",
        [
            ("A", "Remove the private keyword"),
            ("B", "Declare the variable as protected"),
            ("C", "Add public getter and setter methods with validation"),
            ("D", "Make the class abstract"),
        ],
        "C",
        "Java / OOP",
    ),
    (
        'Which of the following represents the "Has-a" relationship (Aggregation) in Java?',
        [
            ("A", "class Student extends Person { ... }"),
            ("B", "class Classroom { Student s1; }"),
            ("C", "interface Flyable { void fly(); }"),
            ("D", "abstract class Shape { ... }"),
        ],
        "B",
        "Java / OOP",
    ),
    (
        "What happens if this code is executed?\n"
        "JFrame frame = new JFrame();\n"
        "frame.setLayout(new BorderLayout());\n"
        'frame.add(new JButton("A"), BorderLayout.NORTH);\n'
        'frame.add(new JButton("B"), BorderLayout.NORTH);\n'
        "frame.setVisible(true);",
        [
            ("A", "Both buttons A and B are visible in the North."),
            ("B", "Only button B is visible."),
            ("C", "Only button A is visible."),
            ("D", "The program crashes."),
        ],
        "B",
        "Java / OOP",
    ),
    (
        "Which of the following HTML practices best supports accessibility and SEO?",
        [
            ("A", "Using <div> for all content"),
            ("B", "Ignoring heading order"),
            ("C", "Embedding all styles inline"),
            ("D", "Using proper heading hierarchy (<h1> to <h6>)"),
        ],
        "D",
        "Web Development",
    ),
    (
        "Which HTML tag is used to include internal (embedded) CSS?",
        [
            ("A", "<style>"),
            ("B", "<link>"),
            ("C", "<css>"),
            ("D", "<script>"),
        ],
        "A",
        "Web Development",
    ),
    (
        "Which component of MVC is responsible for presentation?",
        [
            ("A", "Model"),
            ("B", "Controller"),
            ("C", "View"),
            ("D", "Router"),
        ],
        "C",
        "Web Development",
    ),
    (
        "Which of the following is a common web security threat?",
        [
            ("A", "DNS resolution"),
            ("B", "SQL Injection"),
            ("C", "URL routing"),
            ("D", "Load balancing"),
        ],
        "B",
        "Web Development",
    ),
    (
        "You want to center a div both vertically and horizontally within its parent. Which "
        "CSS approach is MOST reliable for modern browsers?",
        [
            ("A", "Using margins with exact pixel calculations"),
            ("B", "position: absolute; top: 50%; left: 50%;"),
            ("C", "display: flex; justify-content: center; align-items: center; on parent"),
            ("D", "text-align: center; on parent and margin: auto; on child"),
        ],
        "C",
        "Web Development",
    ),
    (
        "Which statement about JavaScript event delegation is CORRECT?",
        [
            ("A", "Event delegation uses event bubbling to handle events at a parent level"),
            ("B", "Event delegation increases memory usage by adding listeners to each child"),
            ("C", "Event delegation only works with click events"),
            ("D", "Event delegation requires stopping event propagation"),
        ],
        "A",
        "Web Development",
    ),
    (
        "When implementing Progressive Web App (PWA) features, which combination provides "
        "the BEST offline experience?",
        [
            ("A", "Service Worker + Cache API"),
            ("B", "Service Worker + Web App Manifest"),
            ("C", "Local Storage + Cache API"),
            ("D", "IndexedDB + Cookies"),
        ],
        "A",
        "Web Development",
    ),
    (
        "Which data format is widely used in SOA-based services?",
        [
            ("A", "PDF"),
            ("B", "JSON"),
            ("C", "DOCX"),
            ("D", "PNG"),
        ],
        "B",
        "Web Development",
    ),
    (
        "Which Android component is responsible for providing a screen with which users can interact?",
        [
            ("A", "Service"),
            ("B", "Broadcast Receiver"),
            ("C", "Activity"),
            ("D", "Content Provider"),
        ],
        "C",
        "Web Development",
    ),
    (
        "Which folder is used to store high-resolution images/bitmaps in an Android project?",
        [
            ("A", "res/drawable"),
            ("B", "res/values"),
            ("C", "res/layout"),
            ("D", "res/menu"),
        ],
        "A",
        "Android",
    ),
    (
        "In Android Studio, which tool is used to monitor memory usage, CPU, and network "
        "performance in real-time?",
        [
            ("A", "Logcat"),
            ("B", "Profiler"),
            ("C", "Debugger"),
            ("D", "Device File Explorer"),
        ],
        "B",
        "Android",
    ),
    (
        "Which View attribute is used to make a component take up all remaining space in a LinearLayout?",
        [
            ("A", "android:layout_weight"),
            ("B", "android:padding"),
            ("C", "android:layout_gravity"),
            ("D", "android:layout_margin"),
        ],
        "A",
        "Android",
    ),
    (
        'Why is "App Sandboxing" considered a fundamental security feature in mobile OS?',
        [
            ("A", "It allows apps to share all data by default to improve speed"),
            ("B", "It ensures that each app runs in its own process with limited access to other apps' data"),
            ("C", "It creates a backup of the app in the cloud"),
            ("D", "It prevents the user from uninstalling system apps"),
        ],
        "B",
        "Android",
    ),
    (
        'How does a professional mobile developer ethically handle "User Consent" for location tracking?',
        [
            ("A", "Request consent clearly at the moment the feature is needed and explain why it is used"),
            ("B", 'Hide the consent in a long "Terms and Conditions" document'),
            ("C", "Track the location in the background and notify the user after one month"),
            ("D", "Assume consent is given if the user installs the app"),
        ],
        "A",
        "Android",
    ),
    (
        "What is the goal of the three-schema database architecture?",
        [
            ("A", "To introduce a decentralized data handling method."),
            ("B", "To separate the user applications from the physical database."),
            ("C", "To disallow concurrent data access for security reasons"),
            ("D", "To avoid insertion and deletion anomalies on the database"),
        ],
        "B",
        "Database",
    ),
    (
        "What is the main reason to use Extended Entity Relation Model (EER)?",
        [
            ("A", "Some attributes may not be useful in superclass entity but applicable to subclass"),
            ("B", "Effectively map many to many relationships between subclasses and superclass"),
            ("C", "To represent the entity type or relationship type that has a multivalued attribute"),
            ("D", "Effectively maps the existence of weak entity with the owner entity type"),
        ],
        "D",
        "Database",
    ),
    (
        "Which of the following statement is not true regrading a weak entity type?",
        [
            ("A", "A weak entity has a partial participation constraint with respect to its identifying relationship"),
            ("B", "Weak Entity does not have their own key attributes to identified from database"),
            ("C", "A weak entity type has a partial key to be identified and ensure database consistency"),
            ("D", "Weak entity type may have more than one identifying entity type in a relationship"),
        ],
        "A",
        "Database",
    ),
    (
        "During database design, the team models real-world entities and their relationships. Why "
        "is a conceptual model important?",
        [
            ("A", "Conceptual modeling automatically generates indexes"),
            ("B", "Conceptual modeling is helpful to enforces ACID rules."),
            ("C", "Conceptual modeling defines physical storage to improve query speed"),
            ("D", "Conceptual modeling provides an abstract view of entities and relationships."),
        ],
        "D",
        "Database",
    ),
    (
        "In database design, logical model mainly focuses on",
        [
            ("A", "Integration and sharing of data among multiple tables with specific DBMS software"),
            ("B", "Mapping of the high-level conceptual model into the implementation data model"),
            ("C", "Mapping subclass and supper class relationship in EER model"),
            ("D", "Creating macro level representation of real-world concept and entities"),
        ],
        "B",
        "Database",
    ),
    (
        "Which of the following is not characteristics of a relational?",
        [
            ("A", "The order of the rows is immaterial"),
            ("B", "All values in a column hold the same data type"),
            ("C", "Each column should have a unique name"),
            ("D", "Ordering of the columns name is important"),
        ],
        "D",
        "Database",
    ),
    (
        "Three processes share four resource units that can be reserved and released only one at a "
        "time. Each process needs a maximum of two units. Then",
        [
            ("A", "there is a possibility of deadlock"),
            ("B", "no deadlock will occur"),
            ("C", "there will be a circular wait"),
            ("D", "Nothing can be predicted about deadlock."),
        ],
        "B",
        "Operating Systems",
    ),
    (
        "Which system call creates a new process in UNIX/Linux?",
        [
            ("A", "exec()"),
            ("B", "wait()"),
            ("C", "exit()"),
            ("D", "fork()"),
        ],
        "D",
        "Operating Systems",
    ),
    (
        "Which operating system is a good example of a Microkernel-based OS?",
        [
            ("A", "MS-DOS"),
            ("B", "UNIX"),
            ("C", "MINIX"),
            ("D", "Windows XP"),
        ],
        "C",
        "Operating Systems",
    ),
    (
        "Windows and macOS are examples of:",
        [
            ("A", "Monolithic kernel"),
            ("B", "Microkernel"),
            ("C", "Batch OS"),
            ("D", "Hybrid kernel"),
        ],
        "D",
        "Operating Systems",
    ),
    (
        "Which mechanism is commonly used to implement synchronization?",
        [
            ("A", "Semaphore"),
            ("B", "Cache"),
            ("C", "Paging"),
            ("D", "Scheduling"),
        ],
        "A",
        "Operating Systems",
    ),
    (
        "Which structure stores file metadata?",
        [
            ("A", "File control block (FCB / inode)"),
            ("B", "Directory"),
            ("C", "FAT"),
            ("D", "Cache"),
        ],
        "A",
        "Operating Systems",
    ),
    (
        "What characterizes the waterfall life-cycle model?",
        [
            ("A", "Software developed in a waterfall-like manner"),
            ("B", "A process model where each phase must be completed before the next begins"),
            ("C", "A process model where phases overlap"),
            ("D", "A cyclic process model"),
        ],
        "B",
        "Software Engineering",
    ),
    (
        '"The user shall be able to search either the entire patient database or a selected subset." '
        "What type of requirement is this?",
        [
            ("A", "Functional Requirement"),
            ("B", "Non-Functional Requirement"),
            ("C", "Product Requirement"),
            ("D", "External Requirement"),
        ],
        "A",
        "Software Engineering",
    ),
    (
        "What is software architecture?",
        [
            ("A", "The software within a building"),
            ("B", "The structure of a client/server system"),
            ("C", "The overall structure of a software system"),
            ("D", "Software classes and their relationships"),
        ],
        "C",
        "Software Engineering",
    ),
    (
        "What is a software design strategy?",
        [
            ("A", "A systematic approach to design production"),
            ("B", "A graphical or textual software description"),
            ("C", "A fundamental concept applicable to system design"),
            ("D", "An overall development plan and direction"),
        ],
        "A",
        "Software Engineering",
    ),
    (
        "What is a state-dependent control object?",
        [
            ("A", "An object dependent on a state machine"),
            ("B", "An object communicating with a state machine"),
            ("C", "An object controlling a state machine"),
            ("D", "An object executing a state machine"),
        ],
        "C",
        "Software Engineering",
    ),
    (
        "Which software quality metrics improve development and maintenance activities?",
        [
            ("A", "Process metrics"),
            ("B", "Project metrics"),
            ("C", "Product metrics"),
            ("D", "User metrics"),
        ],
        "C",
        "Software Engineering",
    ),
    (
        "What is the primary purpose of Requirements Engineering (RE)?",
        [
            ("A", "Writing source code"),
            ("B", "Defining and managing stakeholder needs"),
            ("C", "Designing system architecture"),
            ("D", "Testing software modules"),
        ],
        "B",
        "Software Engineering (Requirements)",
    ),
    (
        "well-executed Requirements Engineering process ensures____________.",
        [
            ("A", "More code reuse"),
            ("B", "Clear scope definition"),
            ("C", "Faster compilation"),
            ("D", "Automated deployment"),
        ],
        "B",
        "Software Engineering (Requirements)",
    ),
    (
        "During integration, a system that works correctly in isolated modules fails to meet overall "
        "performance goals. Which concept best explains why this occurred?",
        [
            ("A", "Functional decomposition"),
            ("B", "Poor elicitation"),
            ("C", "Emergent properties"),
            ("D", "Incorrect validation"),
        ],
        "C",
        "Software Engineering (Requirements)",
    ),
    (
        "Unambiguous requirements:",
        [
            ("A", "Allow multiple interpretations"),
            ("B", "Are informal"),
            ("C", "Have only one clear meaning"),
            ("D", "Are incomplete"),
        ],
        "C",
        "Software Engineering (Requirements)",
    ),
    (
        "Uncontrolled changes to requirements often result in_____________?",
        [
            ("A", "Better systems"),
            ("B", "Scope creep"),
            ("C", "Faster delivery"),
            ("D", "Improved quality"),
        ],
        "B",
        "Software Engineering (Requirements)",
    ),
    (
        "Software architecture primarily focuses on:",
        [
            ("A", "High-level system structure"),
            ("B", "Algorithms"),
            ("C", "Coding standards"),
            ("D", "Debugging"),
        ],
        "A",
        "Software Architecture",
    ),
    (
        "Architectural styles primarily guide:",
        [
            ("A", "Variable scope"),
            ("B", "Component interaction"),
            ("C", "Code indentation"),
            ("D", "Syntax rules"),
        ],
        "B",
        "Software Architecture",
    ),
    (
        "Replication is mainly used to improve:",
        [
            ("A", "Modifiability"),
            ("B", "Security"),
            ("C", "Availability"),
            ("D", "Testability"),
        ],
        "C",
        "Software Architecture",
    ),
    (
        "Blackboard architecture is often used in:",
        [
            ("A", "Compilers"),
            ("B", "AI problem solving"),
            ("C", "Web apps"),
            ("D", "Mobile apps"),
        ],
        "B",
        "Software Architecture",
    ),
    (
        "Strategy pattern allows:",
        [
            ("A", "Object cloning"),
            ("B", "Interface adaptation"),
            ("C", "Object aggregation"),
            ("D", "Runtime algorithm selection"),
        ],
        "D",
        "Software Architecture",
    ),
    (
        'Which strategy should the Project Manager use to address this change while maintaining '
        'the "Triple Constraint"?',
        [
            ("A", "Use the Change Control Board (CCB) to evaluate the impact on time and cost before approval."),
            ("B", 'Defer the feature to the Maintenance phase as "Perfective Maintenance."'),
            ("C", "Reduce the testing phase to accommodate the new development time."),
            ("D", "Increase the team's working hours to 60 hours/week (Crashing)."),
        ],
        "A",
        "Project Management",
    ),
    (
        'What is the difference between a "Risk" and an "Incident?"',
        [
            ("A", "A risk is a potential future event; an incident is a risk that has already occurred."),
            ("B", "A risk is certain, an incident is uncertain."),
            ("C", "Risks are managed by the PM; incidents by the SQA."),
            ("D", "There is no difference."),
        ],
        "A",
        "Project Management",
    ),
    (
        "What is the main objective of Project Scope Management?",
        [
            ("A", "Monitoring the project budget"),
            ("B", "Defining and controlling what is and is not included in the project"),
            ("C", "Managing the project team's performance"),
            ("D", "Scheduling project activities"),
        ],
        "B",
        "Project Management",
    ),
    (
        'In a network diagram, "Total Float" refers to:',
        [
            ("A", "The amount of time an activity can be delayed without delaying the project finish date"),
            ("B", "The time between the early start and late start of the project"),
            ("C", "The time required to complete the critical path"),
            ("D", "The buffer added to the end of the project"),
        ],
        "A",
        "Project Management",
    ),
    (
        "Which testing level focuses on the interaction between integrated modules?",
        [
            ("A", "Unit Testing"),
            ("B", "Integration Testing"),
            ("C", "System Testing"),
            ("D", "Acceptance Testing"),
        ],
        "B",
        "Project Management",
    ),
    (
        "Which of the following best describes software testing?",
        [
            ("A", "The process of executing a program to detect bugs"),
            ("B", "A technique used to ensure software meets specified requirements"),
            ("C", "A method for evaluating system performance"),
            ("D", "A phase in software development where defects are fixed"),
        ],
        "A",
        "Software Testing",
    ),
    (
        "Which scenario would best require automated testing?",
        [
            ("A", "A one-time test for a simple feature"),
            ("B", "A feature that changes frequently"),
            ("C", "A repetitive regression test that must be executed frequently"),
            ("D", "A usability test for a new interface"),
        ],
        "C",
        "Software Testing",
    ),
    (
        "A social media company is testing an AI-driven content recommendation system. The "
        "system should personalize content based on user behavior. What testing technique is most "
        "suitable?",
        [
            ("A", "Model-Based Testing"),
            ("B", "Black-Box Testing"),
            ("C", "Functional Testing"),
            ("D", "Exploratory Testing"),
        ],
        "A",
        "Software Testing",
    ),
    (
        "What is the main purpose of Confirmation Testing (Re-testing)?",
        [
            ("A", "To ensure that fixed defects do not reappear after a change."),
            ("B", "To ensure the change has successfully fixed the defect it was intended to fix."),
            ("C", "To test unchanged parts of the system."),
            ("D", "To test the overall performance of the system"),
        ],
        "B",
        "Software Testing",
    ),
    (
        'A software tester is verifying the behavior of an ATM. The system allows a user to '
        '"Enter PIN," "View Balance," and "Withdraw Cash." If the PIN is entered incorrectly '
        "three times, the card is blocked. Which testing technique is most effective for visualizing "
        "and testing this sequential flow of events?",
        [
            ("A", "State Transition Testing"),
            ("B", "Equivalence Partitioning"),
            ("C", "Decision Table Testing"),
            ("D", "Use Case Testing"),
        ],
        "A",
        "Software Testing",
    ),
    (
        'Which of the following evaluations best describes the "God Object" code well?',
        [
            ("A", "A class that lacks sufficient documentation for maintenance."),
            ("B", "A class that has grown too large and taken on too many responsibilities."),
            ("C", "A class that is never instantiated during the system's execution."),
            ("D", "A class that contains only private methods and no public interface."),
        ],
        "B",
        "Software Maintenance",
    ),
    (
        'Which evaluation explains why "Primitive Obsession" is considered a defect in long-term evolution?',
        [
            ("A", "Primitive types use more memory than complex objects in modern JVMs."),
            ("B", "It makes the code incompatible with older versions of the compiler."),
            ("C", "It hides the domain logic that should be encapsulated within small objects."),
            ("D", "It prevents the use of standard math libraries."),
        ],
        "C",
        "Software Maintenance",
    ),
    (
        'In maintenance estimation, what does "Technical Debt Interest" represent?',
        [
            ("A", "The recurring extra effort required to maintain poorly structured code."),
            ("B", "The cost of the initial development of the feature."),
            ("C", "The tax paid to software vendors for licenses."),
            ("D", "The bonus paid to developers for working overtime."),
        ],
        "A",
        "Software Maintenance",
    ),
    (
        'Applying the principle of "Regression Testing" during maintenance is intended to:',
        [
            ("A", "Ensure that changes have not introduced new bugs into existing functionality."),
            ("B", "Ensure that new features are working correctly."),
            ("C", "Check if the code meets the latest coding style standards."),
            ("D", "Validate the user interface's aesthetic appeal."),
        ],
        "A",
        "Software Maintenance",
    ),
    (
        'When a system is in the "Servicing" stage of the evolution model, what kind of changes '
        "are typically made?",
        [
            ("A", "Migration to a completely new platform."),
            ("B", "Architectural overhauls."),
            ("C", "Total redesign of the user interface."),
            ("D", "Only small patches and bug fixes."),
        ],
        "D",
        "Software Maintenance",
    ),
    (
        "Which layer of the OSI model is responsible for error detection and correction?",
        [
            ("A", "Physical Layer"),
            ("B", "Data Link Layer"),
            ("C", "Network Layer"),
            ("D", "Transport Layer"),
        ],
        "B",
        "Networking",
    ),
    (
        "How many usable host addresses are available in a /27 subnet?",
        [
            ("A", "30"),
            ("B", "32"),
            ("C", "64"),
            ("D", "128"),
        ],
        "A",
        "Networking",
    ),
    (
        "What is the primary function of a router in a network?",
        [
            ("A", "To connect devices within the same LAN"),
            ("B", "To forward data packets between different networks"),
            ("C", "To filter network traffic based on MAC addresses"),
            ("D", "To assign IP addresses to devices"),
        ],
        "B",
        "Networking",
    ),
    (
        "Which protocol is used for secure communication over a network?",
        [
            ("A", "HTTP"),
            ("B", "FTP"),
            ("C", "HTTPS"),
            ("D", "SMTP"),
        ],
        "C",
        "Networking",
    ),
    (
        "Which of the following is an example of a connectionless protocol?",
        [
            ("A", "UDP"),
            ("B", "TCP"),
            ("C", "FTP"),
            ("D", "HTTP"),
        ],
        "A",
        "Networking",
    ),
    (
        "Which device amplifies signals to extend network reach?",
        [
            ("A", "Switch"),
            ("B", "Firewall"),
            ("C", "Router"),
            ("D", "Repeater"),
        ],
        "D",
        "Networking",
    ),
    (
        "Which of the following attacks exploits a vulnerability in SQL-based applications?",
        [
            ("A", "Cross-site scripting (XSS)"),
            ("B", "SQL injection"),
            ("C", "Denial-of-Service (DoS)"),
            ("D", "Phishing"),
        ],
        "B",
        "Security",
    ),
    (
        "What is the role of a honeypot in cybersecurity?",
        [
            ("A", "To detect, deflect, or study hacking attempts"),
            ("B", "To encrypt all data on a network"),
            ("C", "To replace antivirus software"),
            ("D", "To block all external connections"),
        ],
        "A",
        "Security",
    ),
    (
        "Which of the following is NOT a common feature of an Intrusion Detection System (IDS)?",
        [
            ("A", "Monitoring network traffic"),
            ("B", "Logging security incidents"),
            ("C", "Automatically blocking threats"),
            ("D", "Detecting abnormal activities"),
        ],
        "C",
        "Security",
    ),
    (
        'What is a "hash function" used for in digital forensics?',
        [
            ("A", "Ensuring the integrity of digital evidence"),
            ("B", "Encrypting files"),
            ("C", "Compressing data"),
            ("D", "Creating backup copies of files"),
        ],
        "A",
        "Security",
    ),
    (
        "What is the purpose of a Business Continuity Plan (BCP) in cybersecurity?",
        [
            ("A", "To increase the speed of internet connections"),
            ("B", "To ensure business operations can continue during and after security incidents"),
            ("C", "To block all cybersecurity threats before they happen"),
            ("D", "To automatically detect and remove malware"),
        ],
        "B",
        "Security",
    ),
    (
        "Which of the following is a limitation of using rule-based systems for knowledge representation?",
        [
            ("A", "They are too complex"),
            ("B", "They require large databases"),
            ("C", "They are easy to maintain"),
            ("D", "They cannot handle uncertainty"),
        ],
        "D",
        "AI / ML",
    ),
    (
        "The Turing Test is used to measure:",
        [
            ("A", "Computer speed"),
            ("B", "Human intelligence"),
            ("C", "Machine intelligence"),
            ("D", "Algorithm efficiency"),
        ],
        "C",
        "AI / ML",
    ),
    (
        "A classification is considered linearly separable if:",
        [
            ("A", "A hyperplane exists where the classification is true on one side and false on the other."),
            ("B", "It can only be represented by a decision tree."),
            ("C", "The data can be fit by a high-degree polynomial."),
            ("D", "There are no missing features in the training examples."),
        ],
        "A",
        "AI / ML",
    ),
    (
        "Training data is used to:",
        [
            ("A", "Test the final model"),
            ("B", "Improve network speed"),
            ("C", "Teach the model patterns"),
            ("D", "Store results"),
        ],
        "C",
        "AI / ML",
    ),
    (
        "Which component is essential for an AI agent?",
        [
            ("A", "Monitor"),
            ("B", "Environment"),
            ("C", "Printer"),
            ("D", "Keyboard"),
        ],
        "B",
        "AI / ML",
    ),
    (
        "Which algorithm is mainly used for regression problems?",
        [
            ("A", "K-means"),
            ("B", "Naïve Bayes"),
            ("C", "Linear regression"),
            ("D", "Apriori"),
        ],
        "C",
        "AI / ML",
    ),
    (
        "Accuracy is calculated as:",
        [
            ("A", "Correct predictions /Total predictions"),
            ("B", "Incorrect predictions /Total predictions"),
            ("C", "True positives / False positives"),
            ("D", "Errors / Data size"),
        ],
        "A",
        "AI / ML",
    ),
    (
        "In supervised learning, the training data consists of :",
        [
            ("A", "Only inputs"),
            ("B", "Only outputs"),
            ("C", "Inputs without labels"),
            ("D", "Inputs with corresponding labels?"),
        ],
        "D",
        "AI / ML",
    ),
    (
        "Which search strategy will select the lowest expansion node at first for evaluation?",
        [
            ("A", "Greedy best-first search"),
            ("B", "Breadth first search"),
            ("C", "Depth first search"),
            ("D", "First depth search"),
        ],
        "A",
        "AI / ML",
    ),
    (
        'What was originally called the "imitation game" by its creator?',
        [
            ("A", "LISP"),
            ("B", "The logic Theorist"),
            ("C", "The Turing Test"),
            ("D", "Cybernetics"),
        ],
        "C",
        "AI / ML",
    ),
]

assert len(RAW) == 100, f"Expected 100 questions, got {len(RAW)}"

for i, (_, _, answer, topic) in enumerate(RAW, start=1):
    assert TOPIC_BY_NUM(i) == topic, f"Q{i}: topic mismatch {topic!r} vs {TOPIC_BY_NUM(i)!r}"
    assert answer in "ABCD", f"Q{i}: invalid answer {answer!r}"
