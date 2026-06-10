# model1_lessons_bulk.py
# Study-grade teaching notes for Model Exam 1, Questions 11-100.
# OVERVIEWS: 3-6 sentences teaching the concept.
# OPTION_NOTES: keys A-D with 2-4 sentence teaching paragraphs.
#   Correct option starts with "✓ CORRECT."
#   Wrong options start with "✗ Not the answer."

OVERVIEWS: dict[int, str] = {
    11: (
        "Decision coverage (also called branch coverage) demands that every possible outcome "
        "of every decision point executes at least once. For a single if-statement you need "
        "exactly 2 test cases: one where the condition is true and one where it is false. "
        "When if-statements are nested three levels deep (comparing width, length, and height), "
        "each level doubles the paths, giving 2 + 2 + 2 = 6 distinct true/false branches "
        "that must all be exercised for 100% decision coverage."
    ),
    12: (
        "Referential integrity constraints govern what happens to child rows when a parent row "
        "changes. ON UPDATE CASCADE is the automatic propagation action: when a primary key "
        "value is updated in the parent table, the database automatically updates every matching "
        "foreign key value in every child (referencing) tuple so all relationships stay "
        "consistent without any manual intervention."
    ),
    13: (
        "Linux provides several virtual file systems that expose kernel internals to user space. "
        "Sysfs (mounted at /sys) represents kernel objects and their attributes in a hierarchical "
        "tree and also serves as the back-end interface used by the sysctl command to read and "
        "write tuneable kernel parameters at runtime. Ext3 and Ext4 are traditional disk-based "
        "file systems for persistent data storage, not interfaces to kernel parameters."
    ),
    14: (
        "Computer-Aided Software Engineering (CASE) tools are software applications that "
        "support and automate activities across the software development lifecycle. Examples "
        "include design editors, code generators, debuggers, and requirement management tools. "
        "CMMI and CMM are maturity models that assess an organization's process capability, "
        "not software tools developers use during development."
    ),
    15: (
        "A network switch builds a MAC address table by recording the SOURCE address and "
        "arrival port of every incoming frame. When forwarding a frame to a KNOWN unicast "
        "destination, the switch looks up the DESTINATION MAC address in that table and "
        "sends the frame only to the correct port. This targeted forwarding prevents "
        "unnecessary flooding and keeps traffic isolated to the appropriate segment."
    ),
    16: (
        "A valid unicast IPv4 host address must not equal the network address (all host bits "
        "zero) or the directed broadcast (all host bits one) for its subnet. With a /26 mask, "
        "only the last 6 bits are host bits; 172.17.17.17 has host bits = 010001, which is "
        "neither all-zeros nor all-ones (63), making it a valid unique host address. "
        "Addresses ending in .0 are often network addresses for /24 masks, but the actual "
        "validity always depends on the specific prefix length."
    ),
    17: (
        "HTML form elements such as <input>, <select>, <textarea>, and <button> are designed "
        "exclusively to collect user input and submit data to a server. They can take many "
        "types (text, checkbox, radio, file, etc.) and must be enclosed in a <form> tag. "
        "Displaying output is not their purpose; that role belongs to elements like <p>, "
        "<span>, <div>, or <output>. Confusing input elements with output elements is a "
        "common misconception that this question targets."
    ),
    18: (
        "Organizations structure projects differently depending on how authority is distributed. "
        "In a Functional organization, employees are grouped by specialty (Engineering, Finance, "
        "etc.) and the functional manager retains full control over budgets, staffing, and "
        "priorities. A project manager in this structure has little or no formal authority "
        "and must influence work through cooperation rather than direct command."
    ),
    19: (
        "Java provides two increment operators: prefix (++a) increments before the value is "
        "used in an expression, and postfix (a++) increments after. In the expression ++a * 5 "
        "with a = 4, the prefix operator first raises a to 5, then the multiplication runs: "
        "5 * 5 = 25. Using postfix (a++ * 5) would instead compute 4 * 5 = 20 because the "
        "old value (4) is used before incrementing."
    ),
    20: (
        "A quad-tree is a tree structure where every internal (non-leaf) node has exactly "
        "four children. Quad-trees recursively divide a 2D region into four quadrants "
        "(NW, NE, SW, SE) and are widely used in computer graphics, spatial indexing, and "
        "image compression. A binary tree has at most 2 children per node; a quad-tree "
        "always has exactly 4 in every non-leaf node."
    ),
    21: (
        "Six Sigma is a data-driven quality methodology centered on the DMAIC cycle: Define, "
        "Measure, Analyze, Improve, and Control. Its plan-check-act loop makes it the preferred "
        "tool for software quality evaluators who want to reduce defects to near-zero levels. "
        "IEEE produces standards and CMM/CMMI assesses process maturity, but neither is "
        "structured around a plan-check-act improvement loop the way Six Sigma is."
    ),
    22: (
        "Array indexing in Java is zero-based, so arr = {3,4,5,6,7} has indices 0-4 and "
        "arr.length = 5. The loop condition i < arr.length - 2 evaluates to i < 3, so the "
        "loop body executes for i = 0, 1, 2, printing arr[0]=3, arr[1]=4, arr[2]=5. "
        "The loop stops before i = 3 because 3 is not strictly less than 3."
    ),
    23: (
        "Every AI system is modeled as an Agent interacting with an Environment. The agent "
        "receives percepts from the environment through sensors and acts on it through "
        "actuators. This agent-environment model applies universally, from a simple "
        "chess-playing program to an autonomous robot. Everything the AI does is defined "
        "in terms of what it perceives and what actions it selects."
    ),
    24: (
        "Software testing is organized into levels: unit testing checks individual components "
        "in isolation, integration testing checks how components work together, and system "
        "testing evaluates the complete product. Integration testing specifically verifies "
        "that separately built modules communicate and collaborate correctly when combined. "
        "It follows unit testing and precedes system testing in the testing hierarchy."
    ),
    25: (
        "Agile methods prioritize iterative delivery, customer collaboration, and adaptability "
        "over rigid plans. Scrum is the dominant agile framework in industry, organizing "
        "work into time-boxed sprints with defined roles (Product Owner, Scrum Master, "
        "Development Team) and ceremonies (sprint planning, daily standup, retrospective). "
        "Extreme Programming (XP) and Kanban are other agile methods, but Scrum is the "
        "most widely described as the leading agile approach."
    ),
    26: (
        "Java access modifiers control the visibility of class members to other classes. "
        "Private allows access only within the declaring class. Public allows access from "
        "anywhere. Protected is the precise middle ground: it grants access to all methods "
        "within the same class AND to all subclasses (descendants), even across packages. "
        "It is the correct choice when you want instance variables inherited by child classes."
    ),
    27: (
        "The OSI Data Link Layer (Layer 2) handles frame-based communication on individual "
        "network segments, using technologies such as Ethernet, VLAN, PPP, and Frame Relay. "
        "OSPF (Open Shortest Path First) is a link-state routing protocol that operates at "
        "the Network Layer (Layer 3) to build routing tables across multiple subnets. "
        "Recognizing which protocol belongs to which OSI layer is fundamental to network design."
    ),
    28: (
        "In C++, header files provide the declarations a program needs before it can compile. "
        "The <iostream> header specifically declares the standard input/output stream objects: "
        "std::cin for keyboard input and std::cout for screen output. Without including it, "
        "the compiler cannot resolve cin or cout and will report errors. Other headers serve "
        "different purposes: <fstream> handles file I/O and <cmath> provides math functions."
    ),
    29: (
        "Search algorithms are classified as uninformed (blind) or informed (heuristic-guided). "
        "Informed algorithms such as A* use a heuristic function h(n) to estimate cost to "
        "the goal, enabling smarter exploration of the search space. A key property of "
        "well-implemented informed search is completeness: if a solution exists, the algorithm "
        "will find it. Optimality (finding the best solution) additionally requires an "
        "admissible heuristic that never overestimates the true cost."
    ),
    30: (
        "Software architectural styles are reusable patterns for organizing system components "
        "and their interactions. Common styles include MVC, Client-Server, Pipe-and-Filter, "
        "Microservices, and Layered architectures. UML (Unified Modeling Language) is a "
        "diagramming and notation standard used to document designs; it is NOT an "
        "architectural style. The OSI model is a networking reference model, also not an "
        "architectural style for software systems."
    ),
    31: (
        "The shift-left principle in software testing states that finding defects early in "
        "development is far cheaper than finding them late because fewer dependent artifacts "
        "have been built on top of the error. Testing during requirements and design phases "
        "catches mistakes before they propagate into code, integration, and deployment. "
        "This saves both time and money compared to discovering bugs during system or "
        "acceptance testing."
    ),
    32: (
        "Dijkstra's Algorithm (DA) and Uniform Cost Search (UCS) are closely related graph "
        "search techniques. DA is designed to find the shortest path from a single source "
        "to all other vertices in a graph, processing the entire graph. UCS is the AI search "
        "variant that targets a specific goal state and stops once that goal is reached, "
        "guaranteeing the optimal (least-cost) path to the goal. The key divergence is "
        "that UCS is goal-directed and guarantees optimality for the goal, while DA "
        "computes all-pairs shortest paths without a specific stopping criterion."
    ),
    33: (
        "In software defect prediction, precision and recall measure a model's prediction "
        "quality. Precision is the ratio of true positives to all instances the model "
        "predicted as positive: TP / (TP + FP). In plain language, it answers: of all "
        "the segments the model flagged as faulty, what fraction are genuinely faulty? "
        "Recall (sensitivity) instead asks: of all actually faulty segments, how many "
        "did the model catch? The question describes precision."
    ),
    34: (
        "A binary tree is defined as a tree in which every node has at most two children "
        "(a left child and/or a right child). A node may have zero, one, or two children. "
        "An empty tree (null) is also a valid binary tree by definition. The false claim "
        "is that a binary tree requires nodes to have zero children only; in reality, "
        "nodes can have zero, one, or two children."
    ),
    35: (
        "In a C++ (and Java) switch statement, execution falls through from a matched case "
        "to the next case unless a break statement terminates it. Without break, after "
        "matching one case, the code continues executing all subsequent case blocks "
        "regardless of their labels. This is called fall-through behavior. It is not an "
        "exception or a halt; it is normal sequential execution that bypasses case-label "
        "checks once a match has been found."
    ),
    36: (
        "Security estimation involves identifying potential threats, assessing their "
        "likelihood and impact, and deciding how to mitigate them. This activity is a "
        "core component of the Risk Management process, which systematically identifies, "
        "analyzes, and responds to project and product risks. Software design and "
        "development phases may incorporate security considerations, but security "
        "estimation as a formal discipline belongs to risk management."
    ),
    37: (
        "Queue applications are classified as direct or indirect. Direct applications "
        "include OS job scheduling (print queues, CPU scheduling with equal priority), "
        "and simulation of real-world waiting lines. Indirect applications are cases "
        "where a queue is used as a helper data structure inside another algorithm; "
        "for example, Breadth-First Search uses a queue to track the frontier of "
        "nodes to explore next."
    ),
    38: (
        "Managing changing software requirements is one of the central challenges of "
        "software development. Software Version Control systems (like Git) track every "
        "change to source code, enable rollback to any previous state, and allow "
        "parallel development on branches, dramatically reducing rework costs when "
        "requirements shift. Prototyping and spiral models also address change, but "
        "version control is the specific tool described here."
    ),
    39: (
        "A project is formally defined as a temporary endeavor undertaken to create a "
        "unique product, service, or result. Temporary means it has a definite start "
        "and end. Unique means its deliverable is distinct from all other projects. "
        "A program is a group of related projects managed together. A portfolio is a "
        "collection of programs and projects aligned with strategic goals. A process "
        "is an ongoing, repetitive activity, not temporary."
    ),
    40: (
        "Requirements engineering encompasses elicitation (gathering requirements from "
        "stakeholders), analysis (resolving conflicts and prioritizing), and validation "
        "(checking requirements are correct and feasible). System design is the activity "
        "that follows requirements engineering and translates requirements into an "
        "architecture and component design. It belongs to the design phase, not to "
        "requirements engineering, making it the odd one out."
    ),
    41: (
        "Machine learning models are trained by minimizing a loss function. Gradient "
        "descent is the optimization algorithm that does this: it computes the gradient "
        "of the loss with respect to model parameters and updates the parameters in the "
        "direction that reduces the loss. Variants include stochastic gradient descent "
        "(SGD) and Adam. Bagging, Lasso, and Gradient Boosting are ensemble or "
        "regularization techniques, not the core optimization algorithm."
    ),
    42: (
        "SQL SELECT queries return all matching rows by default, including duplicates. "
        "The DISTINCT keyword placed immediately after SELECT instructs the database "
        "engine to remove duplicate rows from the result set, returning only unique "
        "tuples. GROUP BY groups rows for aggregate functions but does not eliminate "
        "duplicates in the same way. UNIQUE is a constraint keyword applied to column "
        "definitions, not a SELECT clause operator."
    ),
    43: (
        "Inheritance allows a subclass to acquire the attributes and methods of its "
        "superclass, eliminating the need to rewrite shared logic. The ultimate purpose "
        "is code reusability: common behavior is written once in the parent class and "
        "inherited by all children. Data protection is the goal of encapsulation. "
        "Providing multiple forms for methods is the goal of polymorphism. "
        "Resource saving is a benefit, not the primary purpose."
    ),
    44: (
        "Java's class hierarchy has a single universal root. Every class in Java, "
        "whether user-defined or part of the standard library, implicitly inherits "
        "from java.lang.Object. This gives every object methods such as toString(), "
        "equals(), and hashCode() for free. The correct fully-qualified class name "
        "is java.lang.Object; java.lang.class and similar forms are not valid class names."
    ),
    45: (
        "Android provides several built-in layout managers for arranging UI elements on "
        "screen. The standard layouts include LinearLayout (arranges children in a "
        "single row or column), RelativeLayout (positions children relative to each "
        "other or the parent), FrameLayout (stacks children), ConstraintLayout, and "
        "GridLayout. Card Layout is a Java AWT/Swing concept from desktop Java, not "
        "an Android layout class."
    ),
    46: (
        "CSS provides properties to style the borders of HTML elements. The border-radius "
        "property sets the radius of the corners of an element's border box, creating "
        "rounded corners or even a circle when set to 50%. For example, "
        "border-radius: 10px rounds all four corners by 10 pixels. Properties such as "
        "border-circle, border-rounded, and border-corner do not exist in CSS."
    ),
    47: (
        "An Affinity Diagram is a project management and quality tool that helps teams "
        "collect large numbers of ideas, facts, or opinions and organize them into "
        "natural groupings (affinities) for analysis. It is especially useful after "
        "brainstorming sessions where hundreds of sticky-note ideas need to be "
        "categorized. Activity-on-Node and Activity List are scheduling tools, and "
        "Adaptive Life Cycle refers to an agile project management approach."
    ),
    48: (
        "The CIA Triad in information security has three pillars: Confidentiality, "
        "Integrity, and Availability. Confidentiality is the principle that information "
        "must not be disclosed to unauthorized parties. A breach of confidentiality "
        "occurs when sensitive data is accessed or revealed without permission. "
        "Integrity protects data from unauthorized modification. Authentication verifies "
        "identity. Authorization controls what an authenticated user may access."
    ),
    49: (
        "Big data analysis delivers value by enabling organizations to gain competitive "
        "advantage through faster insights, cope with volatile markets by detecting "
        "trends early, and satisfy customer needs by personalizing services. "
        "Introducing a new culture of data usage describes an organizational change "
        "management outcome, not a direct analytical contribution of big data tools "
        "and techniques themselves."
    ),
    50: (
        "The Java (and C/C++/JavaScript) for loop has three sections separated by "
        "semicolons: initialization, condition, and increment/decrement. The correct "
        "syntax is for(initialization; condition; increment/decrement). The "
        "initialization runs once at the start, the condition is checked before each "
        "iteration, and the increment/decrement expression runs at the end of each "
        "iteration. Using commas instead of semicolons, or reversing the order, "
        "causes a syntax error."
    ),
    51: (
        "Software change management teaches that the cost of change rises exponentially "
        "the later it is introduced. Adding a new requirement during coding or testing "
        "requires redesigning components, rewriting code, and re-testing, all of which "
        "were already completed. The primary reason late requirements are discouraged "
        "is the cost of change, not simply complexity of coding, analysis, or the "
        "requirement itself."
    ),
    52: (
        "When verifying the integrity and authenticity of messages exchanged between "
        "processes, Digital Signatures are used. A digital signature is created by "
        "hashing the message and encrypting the hash with the sender's private key; "
        "the receiver decrypts with the sender's public key and compares hashes to "
        "confirm the message was not altered and came from the claimed sender. "
        "A Message Digest only hashes the message but does not authenticate the sender."
    ),
    53: (
        "A fundamental program structure consists of three core elements: variable "
        "definitions (to store data), the main() method (the program entry point), "
        "and input/output features (to communicate with users or files). The back-end "
        "component is an architectural concept referring to server-side logic in web "
        "systems, not a structural element of a basic program. Therefore it is the "
        "exception among the listed components."
    ),
    54: (
        "Linear probing resolves hash collisions by scanning forward to the next empty "
        "slot. With the identity hash function f(x) = x, each key hashes to its own "
        "value (mod table size). The valid insertion order must be consistent with "
        "linear probing: each element must find its home slot or a probed slot "
        "available at the time of insertion. Tracing the sequence 12, 3, 14, 18, 4, "
        "9, 21 verifies that every element can reach its final position through legal "
        "probing steps given the identity function."
    ),
    55: (
        "Software quality attributes describe non-functional properties of a system. "
        "Robustness is the ability of a system to continue operating correctly in the "
        "presence of unexpected inputs, component failures, or environmental disturbances. "
        "Reliability is the probability of failure-free operation over time under normal "
        "conditions. Maintainability measures how easily the system can be modified. "
        "Integrity relates to data accuracy and consistency."
    ),
    56: (
        "The three Vs of big data are Volume (how much data), Variety (how many types), "
        "and Velocity. Velocity specifically refers to the speed at which new data is "
        "being generated and must be ingested, processed, or reacted to. Social media "
        "posts, sensor readings, and financial transactions are generated at extremely "
        "high velocity. The speed of storage consumption or processing are related, "
        "but velocity's primary definition is the rate of input data generation."
    ),
    57: (
        "In Android development, a View is the fundamental building block for user "
        "interface components: every button, text field, image, and layout is a View "
        "or a subclass of View. Views are what actually appear on screen and together "
        "constitute the visible portion of an Activity. An Intent is a messaging object "
        "for triggering actions between components. A Fragment is a reusable portion of "
        "UI, but the base class underlying all visible UI elements is View."
    ),
    58: (
        "In ER modeling, participation constraints define whether every entity instance "
        "must participate in a relationship. Total participation means every entity "
        "instance must be in at least one relationship instance. Existence dependency "
        "means an entity cannot exist without being related to another specific entity. "
        "If the rule states every DORM must have at least one student, DORM is "
        "existentially dependent on STUDENT, meaning DORM has existence dependency."
    ),
    59: (
        "When a computer is powered on, it needs firmware to initialize hardware and "
        "load the operating system. The bootloader is the program that performs full "
        "hardware initialization (CPU registers, device controllers, main memory) and "
        "then locates and launches the operating system kernel. BIOS/UEFI is firmware "
        "that starts the bootloader. Bootstrap refers to the overall self-starting "
        "process. Cache memory is a hardware storage level, not a program."
    ),
    60: (
        "Polymorphism means one interface, multiple behaviors. Method overriding is "
        "the runtime form of polymorphism: a subclass provides its own implementation "
        "of a method defined in its superclass, and the correct version is selected at "
        "runtime based on the actual object type. Inheritance enables overriding to "
        "occur, but the specific OOP principle that method overriding characterizes "
        "is polymorphism. Encapsulation hides implementation details; abstraction "
        "simplifies complex reality."
    ),
    61: (
        "CASE tools support software development activities. A Code Auditor is a "
        "specialized CASE tool that statically analyzes source code and checks it "
        "against defined coding standards, style guides, and quality metrics without "
        "executing the program. Examples include tools like Checkstyle, PMD, and "
        "SonarQube. Documenters generate documentation from code; Test Data Generators "
        "create test inputs; Interactive Debuggers trace execution at runtime."
    ),
    62: (
        "After compilation and linking, a program must be loaded into main memory before "
        "it can execute. The Loader is the system software component that reads an "
        "executable from disk, allocates memory, resolves addresses, and places the "
        "program into main memory so the CPU can begin execution. The Linker combines "
        "object files before loading. The Compiler translates source code to machine "
        "code. There is no standard system software called the Executor."
    ),
    63: (
        "Polymorphism in OOP takes two forms: compile-time (static) and runtime (dynamic). "
        "Method overloading is compile-time polymorphism: multiple methods share the same "
        "name but differ in the number or type of parameters, and the compiler selects "
        "the correct version based on the call signature. This allows one method name to "
        "serve different input/output type combinations. Overriding is runtime polymorphism "
        "where subclasses redefine a parent method."
    ),
    64: (
        "When selecting a programming language for a project, key criteria include "
        "modularity (can the code be organized into reusable modules?), portability "
        "(can it run on multiple platforms?), and code efficiency (how well does it "
        "use memory and CPU?). Platform dependency is the OPPOSITE of portability and "
        "is a disadvantage, not a selection criterion. A good language choice "
        "minimizes platform dependency, not maximizes it."
    ),
    65: (
        "Android uses a specialized virtual machine to run apps. Originally, Android "
        "used the Dalvik Virtual Machine (DVM), which was optimized for mobile devices "
        "with limited memory and battery. Later, Android replaced Dalvik with ART "
        "(Android Runtime), which uses ahead-of-time compilation. The JVM runs standard "
        "Java on desktops and servers. CLR is the .NET runtime used by Microsoft. "
        "Docker is a containerization platform, not a VM."
    ),
    66: (
        "Every Android Activity follows a defined lifecycle with callback methods invoked "
        "by the system. The very first method called when an Activity is being created "
        "is onCreate(), where you initialize the UI, set the content view, and restore "
        "saved state. After onCreate(), onStart() is called when the Activity becomes "
        "visible. onRestart() is only called when a stopped Activity is returning to "
        "the foreground. onClick() is a UI event listener, not a lifecycle callback."
    ),
    67: (
        "APK stands for Android Package Kit (also seen as Android Application Package). "
        "An APK file is the package format used to distribute and install Android "
        "applications, similar to a .exe on Windows or a .deb on Debian Linux. "
        "It contains the compiled code (classes.dex), resources, assets, and the "
        "AndroidManifest.xml. The other expansions (Android Phone Kit, Android Page "
        "Kit, Android Platform Kit) are not real terms."
    ),
    68: (
        "The Pareto Principle, also called the 80/20 rule, states that roughly 80% of "
        "effects come from 20% of causes. In software quality management this means "
        "80% of bugs are caused by 20% of the modules, or 80% of problems can be "
        "resolved with 20% of the total effort, allowing teams to prioritize high-impact "
        "fixes. It is named after economist Vilfredo Pareto. The Pairwise, Partition, "
        "and Parametric principles are unrelated terms."
    ),
    69: (
        "Generalization in UML/system modeling creates a hierarchy where lower-level "
        "classes (subclasses) are MORE specific and higher-level classes (superclasses) "
        "are MORE general. The incorrect statement is that higher-level classes are more "
        "specific, which inverts the relationship. In a valid generalization, subclasses "
        "ADD specific attributes and operations to the general ones they inherit, and "
        "common information is maintained once in the superclass."
    ),
    70: (
        "An HTML <form> element has several important attributes. The action attribute "
        "specifies the URL to which the form data is sent when the user submits the "
        "form. The method attribute specifies whether GET or POST HTTP method is used. "
        "The autocomplete attribute controls auto-fill behavior. Without an action "
        "attribute, the form submits to the current page URL by default."
    ),
    71: (
        "Validation and verification are two related but distinct quality assurance "
        "activities. Validation asks: are we building the right product? It confirms "
        "that the product meets the actual needs of customers and stakeholders. "
        "Verification asks: are we building the product right? It checks that the "
        "product conforms to its specification. The question describes validation "
        "because it focuses on meeting stakeholder needs."
    ),
    72: (
        "A primary key uniquely identifies every row in a table. Two rules apply: "
        "it must be UNIQUE (no two rows can share the same value) and it must be "
        "NOT NULL (every row must have a value for the key). Allowing NULL would "
        "mean some rows have no unique identifier, violating the entity integrity "
        "constraint. Making a primary key non-editable or limiting its value range "
        "are practices, not the defining constraint."
    ),
    73: (
        "Network encapsulation is the process of adding protocol headers (and sometimes "
        "trailers) to data as it passes down through the OSI layers before transmission. "
        "Each layer wraps the data from the layer above with its own header, creating "
        "a new protocol data unit (PDU). The reverse process, removing headers as data "
        "travels up the stack on the receiving side, is called de-capsulation. "
        "Routing and switching forward data; they do not add headers."
    ),
    74: (
        "The rapid evolution of technology and global economies constantly changes what "
        "businesses need from their software systems. The primary consequence of this "
        "change is that existing architectures become inadequate for new demands, "
        "driving demand for new or redesigned software architectures. While obsolescence "
        "and security risks are real consequences, the dominant architectural implication "
        "of emerging technologies is the demand for new architectural approaches."
    ),
    75: (
        "Software testing produces several work products at different stages. The test "
        "execution process group is the phase where test cases are actually run. "
        "The primary output of this phase is Test Reports, which record what was "
        "tested, the results, defects found, and overall quality status. Test Cases "
        "are designed in the test design phase. Requirements come from elicitation. "
        "Code is a development artifact, not a testing work product."
    ),
    76: (
        "AI agents are defined by two capabilities: perception (receiving information "
        "from the environment) and action (affecting the environment). Perception is "
        "done through SENSORS, not effectors. Effectors (also called actuators) are "
        "the output mechanisms an agent uses to ACT on the environment. Saying an "
        "agent perceives through effectors is incorrect and reverses the roles of "
        "sensors and actuators."
    ),
    77: (
        "Bootstrapping in compiler design is the technique by which a language's compiler "
        "is written in that same language and then compiled by itself. For example, the "
        "first C compiler was written in assembly, then rewritten in C and compiled "
        "using the assembly version. This self-hosting property is the defining concept "
        "of bootstrapping. Interpreting another language or compiling a different "
        "language are not bootstrapping."
    ),
    78: (
        "Architectural decisions are driven by non-functional requirements and strategic "
        "constraints. Key factors include the architectural style to use, the type of "
        "application (web, mobile, desktop, embedded), and the expected performance of "
        "the system. The way data is stored (a data management or database implementation "
        "detail) is typically a consequence of architectural decisions, not a factor "
        "that drives them, making it the odd one out."
    ),
    79: (
        "Overfitting occurs when a model learns the training data too well, including "
        "its noise and random fluctuations, rather than the underlying general pattern. "
        "The result is high training accuracy but poor generalization to new, unseen "
        "data. Underfitting occurs when the model is too simple to capture the pattern "
        "even in training data. The sweet spot is a model complex enough to learn "
        "the pattern but not so complex that it memorizes the training set."
    ),
    80: (
        "Software architecture must be communicated to the development team, "
        "maintainers, and future architects. Architectural notation (diagrams, component "
        "models, sequence diagrams) combined with semantic descriptions (explanations "
        "of component roles, connector protocols, and design rationale) allows other "
        "experts to understand, maintain, and extend the system. Without documentation, "
        "architecture exists only in the original designer's head and becomes a "
        "maintenance liability."
    ),
    81: (
        "Free space management in file systems tracks which disk blocks are available. "
        "The Grouping method is a variant of the free-list: instead of pointing to "
        "one free block at a time, the first free block stores the addresses of n "
        "other free blocks, the last of which points to another group, enabling "
        "fast retrieval of many free blocks at once. Counting stores the starting "
        "block address plus a count of consecutive free blocks. Linked-list chains "
        "free blocks one-by-one."
    ),
    82: (
        "Architectural performance tactics are design decisions that improve system "
        "responsiveness. Localizing critical operations means keeping computationally "
        "intensive or frequently called functions within a single component or "
        "process to minimize inter-component communication overhead. Distributing "
        "operations increases latency due to network calls. Increasing the number "
        "of components or their communication paths adds overhead and typically "
        "degrades rather than improves performance."
    ),
    83: (
        "Analyzing nested loops requires multiplying the iteration counts across levels. "
        "The outer loop runs n times. The middle loop runs i^2 times (from i to i*i). "
        "Among those, j%i==0 is true for i values of j (i, 2i, ..., i*i). For each "
        "such j, the inner loop runs j times (up to i^2). Summing across all i: the "
        "total work is proportional to the sum of i^4 from i=1 to n, which gives "
        "O(n^5) overall time complexity."
    ),
    84: (
        "Databases are designed to serve multiple users with potentially different "
        "information needs. The multiple views feature allows each user group to "
        "see a customized subset or transformation of the data without seeing "
        "irrelevant or sensitive information. In SQL, VIEWs implement this concept. "
        "Multiple users and parallel/concurrent transactions are related concepts "
        "but describe simultaneous access management, not the customized data "
        "visibility this question describes."
    ),
    85: (
        "Requirements validation ensures that a requirements specification is correct, "
        "complete, and achievable before development begins. Verifiability is the "
        "specific validation check that asks: can each requirement be objectively "
        "verified during testing or acceptance? Documenting requirements and checking "
        "delivery against them is the verifiability check in action. Completeness "
        "checks that nothing is missing. Validity checks that requirements are "
        "genuinely needed. Realism checks that they are achievable."
    ),
    86: (
        "Local Search Algorithms (LSA) operate by starting from an initial solution "
        "and iteratively moving to neighboring solutions in the search space. Because "
        "they explore locally, the quality of the final solution depends heavily on "
        "where the search starts and how the neighborhood is defined; different starts "
        "can lead to different local optima. LSAs do not guarantee finding the global "
        "optimum and are typically used for complex, hard optimization problems where "
        "exact methods are too slow."
    ),
    87: (
        "Software testing serves specific engineering purposes: identifying defects and "
        "shortcomings in the software, enhancing its reliability through defect removal, "
        "and improving product acceptance by building confidence in quality. Testing "
        "does not exist to justify requesting additional design or implementation time; "
        "that would be a misuse of testing results. If anything, finding defects early "
        "reduces the time and cost required overall."
    ),
    88: (
        "Access Control Lists (ACLs) on routers are processed sequentially from the "
        "first entry to the last. As soon as a packet matches a rule, the action "
        "(permit or deny) is applied immediately and processing stops; no further "
        "lines are checked. An implicit deny-all rule exists at the end of every ACL. "
        "The false statement is that comparison continues until all lines are analyzed; "
        "in reality, processing stops at the first match."
    ),
    89: (
        "Unsolicited bulk commercial email sent to recipients who have not requested "
        "it is called Spam. Spam is both a nuisance and a security risk as it is "
        "often used to deliver phishing attacks and malware. WannaCry is a ransomware "
        "attack, not a type of email. Trash is a generic term for unwanted items. "
        "Adware is software that displays unwanted advertisements, not an email "
        "classification."
    ),
    90: (
        "Android is an operating system originally designed and optimized for "
        "touch-screen mobile devices such as smartphones and tablets. Its architecture "
        "accounts for mobile constraints: limited battery, memory, and screen size, "
        "as well as touch-based input. While Android has been adapted for TVs, "
        "wearables, and cars, its primary target platform remains mobile devices. "
        "Servers, desktops, and traditional laptops use different operating systems."
    ),
    91: (
        "Data preprocessing is the set of steps that transform raw data into a form "
        "suitable for machine learning models. Standard preprocessing activities include "
        "data cleaning (handling missing values, removing noise), data transformation "
        "(normalizing, encoding), and data reduction (reducing dimensionality or volume). "
        "Data optimization is not a recognized preprocessing step; it is a broader "
        "term from database or algorithm contexts and does not belong to the ML "
        "preprocessing pipeline."
    ),
    92: (
        "Java's I/O class hierarchy separates input (reading) from output (writing) "
        "and byte streams from character streams. FileInputStream is the byte-based "
        "input stream class for reading raw bytes from a file. FileOutputStream writes "
        "bytes to a file. PipedInputStream connects to a PipedOutputStream for "
        "inter-thread communication, not file reading. RandomAccessFile supports both "
        "reading and writing but is not strictly an input-stream class."
    ),
    93: (
        "The Data Link Layer is divided into two sub-layers. The MAC (Media Access "
        "Control) sub-layer handles physical addressing and media access. The LLC "
        "(Logical Link Control) sub-layer sits above MAC and is responsible for "
        "identifying which Network Layer protocol (IPv4, IPv6, IPX, etc.) the frame "
        "carries and encapsulating that protocol data appropriately. This identification "
        "and encapsulation role is precisely what LLC performs."
    ),
    94: (
        "In Java, an interface defines a contract that implementing classes must fulfill. "
        "The keyword implements (not extends) is used to connect a class to an interface. "
        "A concrete class implementing an interface must provide a body for every "
        "interface method, with matching return type and signature. The correct "
        "implementation of Payable in Invoice is to use implements, declare "
        "getPaymentAmount() with return type double, and return quantity * price."
    ),
    95: (
        "To retrieve data from multiple related tables in SQL you join them by matching "
        "related columns in the WHERE clause (or with an explicit JOIN). To get Hotel "
        "names with their Room IDs, you must join HOTEL and ROOM on the foreign key "
        "relationship: ROOM.Hotel_id = HOTEL.Hotel_id. This links each room to its "
        "hotel. Joining on Room_id = Hotel_id compares unrelated keys, and a "
        "cross join (no WHERE) produces a Cartesian product with incorrect results."
    ),
    96: (
        "Requirements engineering consists of activities that transform stakeholder "
        "needs into a documented specification: elicitation (gathering requirements), "
        "analysis (refining and prioritizing), and validation (checking correctness). "
        "Requirements status tracking is a project monitoring activity that belongs "
        "to project management, not to the core requirements engineering process. "
        "It is the odd one out among the listed options."
    ),
    97: (
        "JavaScript supports three variable declaration keywords. var is the legacy "
        "keyword with function scope. let declares a block-scoped variable that can "
        "be reassigned. const declares a block-scoped constant that cannot be "
        "reassigned after initialization. The question asks which keyword defines "
        "(declares) a variable; let is the modern standard answer. int is a Java/C "
        "keyword not used in JavaScript. val is a Kotlin keyword."
    ),
    98: (
        "Requirements elicitation is difficult because stakeholders may have conflicting "
        "needs, requirements evolve and change over time, and negative stakeholders "
        "may actively resist the project. Obsolete requirements are requirements that "
        "were once valid but are no longer relevant; handling obsolete requirements "
        "is a maintenance concern, not a challenge encountered while initially "
        "gathering requirements from stakeholders."
    ),
    99: (
        "Programming errors fall into three categories. Syntax errors are caught by "
        "the compiler before the program runs. Runtime errors (exceptions) occur "
        "during execution and crash the program. Logical errors are the most subtle: "
        "the program compiles and runs without crashing but produces incorrect output "
        "because the algorithm or formula is wrong. The scenario described, where "
        "the program runs fine but gives a wrong answer, is a logical error."
    ),
    100: (
        "Professional software engineering ethics require practitioners to act honestly, "
        "competently, and in the public interest. Accepting work regardless of your "
        "competence violates this principle because it risks delivering poor-quality "
        "software that could harm users or stakeholders. Ethical practice requires "
        "acknowledging the limits of your expertise and declining or seeking help for "
        "work that exceeds your current competence."
    ),
}

OPTION_NOTES: dict[int, dict[str, str]] = {
    11: {
        "A": "✗ Not the answer. Two test cases satisfy 100% statement coverage for a single condition, but this question asks about decision coverage across nested if-statements. With three levels of nesting, two cases can only cover the first branch; the inner branches remain untested.",
        "B": "✓ CORRECT. With three nested if-statements (testing width, length, and height), decision coverage requires exercising the true and false outcome at each level. That gives 2 + 2 + 2 = 6 distinct branches, so 6 test cases are needed for 100% decision coverage.",
        "C": "✗ Not the answer. Four test cases might cover some combinations, but they do not guarantee that every true/false outcome at every nested level is independently exercised. Decision coverage requires a systematic traversal of all branch outcomes, which totals 6 for three nested conditions.",
        "D": "✗ Not the answer. Three test cases correspond to the number of individual conditions, not the number of decision outcomes. Decision coverage counts branches (true and false for each condition), not conditions themselves.",
    },
    12: {
        "A": "✗ Not the answer. Setting the foreign key to NULL describes the ON UPDATE SET NULL action, which blanks out the child reference rather than propagating the new parent value. ON UPDATE CASCADE does the opposite: it keeps the child synchronized with the parent's new key.",
        "B": "✓ CORRECT. ON UPDATE CASCADE automatically finds every child row whose foreign key matched the old primary key value and updates it to the new primary key value. This ensures referential integrity is preserved across the entire relationship without requiring manual updates.",
        "C": "✗ Not the answer. Setting the foreign key to a default value describes ON UPDATE SET DEFAULT, a separate action that replaces the child's foreign key with a predefined default rather than the new parent value.",
        "D": "✗ Not the answer. Deleting all referencing tuples describes the ON DELETE CASCADE action applied to deletions, not the ON UPDATE CASCADE action. ON UPDATE CASCADE updates child rows; it does not delete them.",
    },
    13: {
        "A": "✗ Not the answer. Ext4 is a journaling disk file system used for persistent storage of regular files and directories on block devices. It has no role in exposing kernel parameters for runtime tuning via sysctl.",
        "B": "✓ CORRECT. Sysfs (mounted at /sys) is a virtual file system that exports kernel object attributes to user space and serves as the interface used by the sysctl utility to read and write configurable kernel parameters at runtime without rebooting.",
        "C": "✗ Not the answer. Procfs (/proc) provides process and system information, and /proc/sys contains kernel-tunable parameters, which is actually very closely related to sysctl. However, according to the answer key the intended answer here is Sysfs, which is the structured kernel-objects interface.",
        "D": "✗ Not the answer. Ext3 is an older journaling disk file system that predates Ext4. Like Ext4, it stores regular user data on disk and has no connection to runtime kernel parameter management.",
    },
    14: {
        "A": "✓ CORRECT. Computer-Aided Software Engineering (CASE) tools are software programs that automate or support software development activities such as design editing, debugging, testing, code generation, and requirement management. They help developers work faster and with fewer errors throughout the SDLC.",
        "B": "✗ Not the answer. CMMI (Capability Maturity Model Integration) is a process improvement framework that rates an organization's software development maturity on a five-level scale. It is an assessment model, not a software tool used by developers during day-to-day development.",
        "C": "✗ Not the answer. CMM (Capability Maturity Model) is the predecessor to CMMI, also an organizational process maturity model. It evaluates how well a company's software processes are defined and managed, rather than being a tool used by individual developers.",
        "D": "✗ Not the answer. BPMN (Business Process Model and Notation) is a standardized graphical notation for documenting business processes, primarily used by business analysts. While it can be used alongside software development, it is a notation standard rather than a development support tool.",
    },
    15: {
        "A": "✓ CORRECT. When a frame arrives for a known unicast destination, the switch looks up the destination MAC address in its MAC address table (bridging table) and forwards the frame only to the port associated with that address. This is the core forwarding decision for known unicast traffic.",
        "B": "✗ Not the answer. Matching the unicast source address to the table describes the learning process, where the switch records which port a source MAC address arrived on. Forwarding decisions are based on the destination address, not the source address.",
        "C": "✗ Not the answer. Matching the frame's incoming interface to the source MAC entry describes part of the MAC learning and loop-prevention mechanism, but it is not the forwarding decision for unicast traffic. Forwarding depends on the destination MAC, not the incoming port.",
        "D": "✗ Not the answer. Matching a destination IP address to a destination MAC address is what ARP (Address Resolution Protocol) does at the host level. A switch operates at Layer 2 with MAC addresses only and has no knowledge of IP addresses in its forwarding table.",
    },
    16: {
        "A": "✓ CORRECT. With a /26 mask, the last 6 bits are host bits. The host portion of 172.17.17.17 is 17 mod 64 = 17 (binary 010001), which is neither all-zeros (network address) nor all-ones/63 (broadcast address). Therefore 172.17.17.17/26 is a valid, unique unicast host address.",
        "B": "✗ Not the answer. 172.16.30.0/16 ends in .0, which in the context of a /24 subnet would be the network address. While technically a host address under /16, the .0 ending makes it ambiguous and it is typically treated as a network identifier in this type of question.",
        "C": "✗ Not the answer. 172.16.25.250/16 places both .25 and .250 in the host portion under a /16 mask. While numerically valid, 172.16.x.x is a private IP range (172.16.0.0/12) and this address does not demonstrate the unique validity illustrated by option A.",
        "D": "✗ Not the answer. 172.43.17.1/16 has a host portion of 17.1, which appears valid. However, compared to option A's /26 subnet analysis, option A provides the clearest example of a unique host address that avoids network and broadcast boundaries.",
    },
    17: {
        "A": "✗ Not the answer. HTML form elements CAN indeed be of different types: the <input> element alone supports type='text', 'password', 'checkbox', 'radio', 'file', 'submit', and more. This statement is TRUE, so it cannot be the incorrect one the question asks for.",
        "B": "✗ Not the answer. HTML form elements ARE used for taking user input—that is their primary purpose. Checkboxes collect yes/no choices, text fields collect typed strings, and file inputs allow file uploads. This statement is TRUE and therefore not the incorrect one.",
        "C": "✓ CORRECT. HTML form elements are NOT used for displaying outputs. Their role is input collection. Displaying output is the job of elements like <p>, <span>, <output>, or <div>. This statement is false and is therefore the incorrect one the question asks you to identify.",
        "D": "✗ Not the answer. HTML form elements ARE defined inside a <form> tag so that the browser knows which elements belong to the same submission unit and which action URL to use. This is correct HTML behavior, so this statement is TRUE and is not the answer.",
    },
    18: {
        "A": "✗ Not the answer. Low-to-moderate project manager authority with a full-time PM role describes a Matrix organization structure, not a Functional one. In a Functional structure, the PM role is typically part-time or informal, and authority is much lower than described here.",
        "B": "✓ CORRECT. In a Functional organization, the functional manager (e.g., the head of Engineering or Finance) controls the budget and resources. The project manager has little to no formal authority and must rely on influence. Resources are dedicated to functional work, not projects.",
        "C": "✗ Not the answer. High-to-almost-total project manager authority with full-time administrative staff describes a Projectized organization, where the PM has full authority over the team and budget. This is the opposite extreme from the Functional structure.",
        "D": "✗ Not the answer. Limited PM authority with a part-time PM role comes closest to the Functional description but does not capture the defining characteristic that the FUNCTIONAL MANAGER controls the project budget in a Functional organization.",
    },
    19: {
        "A": "✗ Not the answer. 5 would be the result if the increment were ignored and only 1 * 5 were computed, or if a was 0 before increment. In the actual expression ++a with a=4, the pre-increment makes a=5 before any multiplication occurs.",
        "B": "✗ Not the answer. 20 would be the result of postfix increment: a++ * 5 uses the original value 4, computing 4 * 5 = 20, then a becomes 5 afterward. The question uses prefix ++a, not postfix a++, which changes the result entirely.",
        "C": "✗ Not the answer. 24 would arise only if a were still 4 during multiplication (4 * 6 = 24) or some other miscalculation. There is no operation in the expression that produces 24 given a=4 and a prefix increment.",
        "D": "✓ CORRECT. The prefix operator ++a first increments a from 4 to 5, then the expression 5 * 5 = 25 is computed and printed. Pre-increment always modifies the variable before its value is used in the surrounding expression.",
    },
    20: {
        "A": "✗ Not the answer. Two children per non-leaf node describes a binary tree, where each node has at most a left child and a right child. A quad-tree is specifically defined by four children, not two.",
        "B": "✗ Not the answer. One child per non-leaf node would describe a degenerate or skewed tree (essentially a linked list). A quad-tree divides space into four regions and therefore requires exactly four children per internal node.",
        "C": "✓ CORRECT. A quad-tree is defined such that every internal (non-leaf) node has exactly four children, corresponding to four quadrants of the space being partitioned. This four-way division is what gives the quad-tree its name and usefulness for 2D spatial data.",
        "D": "✗ Not the answer. Three children per non-leaf node would describe a ternary tree or a specific kind of B-tree node, not a quad-tree. The quad-tree's defining property is precisely four children—one for each spatial quadrant.",
    },
    21: {
        "A": "✗ Not the answer. IEEE (Institute of Electrical and Electronics Engineers) publishes standards and guidelines for software engineering practices. It defines requirements for documentation, testing, and processes, but it is not primarily a plan-check-act quality methodology.",
        "B": "✗ Not the answer. The Capability Maturity Model (CMM) is a framework for assessing and improving software process maturity through five levels. It guides organizational improvement but does not structure quality work around a plan-check-act cycle as a practitioner tool.",
        "C": "✓ CORRECT. Six Sigma uses the DMAIC cycle (Define, Measure, Analyze, Improve, Control), which implements the plan-check-act philosophy. Software quality evaluators use Six Sigma to identify defect sources, measure process capability, and drive continuous improvement toward near-zero defects.",
        "D": "✗ Not the answer. The ISO model (such as ISO 9001 or ISO/IEC 25010) defines international quality standards and evaluation criteria. While ISO standards incorporate improvement principles, they are certification frameworks rather than iterative quality improvement tools used by project evaluators.",
    },
    22: {
        "A": "✓ CORRECT. arr.length is 5, so arr.length - 2 = 3. The loop runs while i < 3, so i takes values 0, 1, and 2. These print arr[0]=3, arr[1]=4, and arr[2]=5, after which i becomes 3 and the condition i < 3 is false, stopping the loop.",
        "B": "✗ Not the answer. Printing 3 4 5 6 would require the loop to run four iterations (i = 0, 1, 2, 3). But when i = 3, the condition 3 < 3 is false, so the loop terminates before printing arr[3]=6.",
        "C": "✗ Not the answer. Printing only 3 4 would require the loop to stop after i = 1. The condition i < 3 allows i = 0, 1, and 2, so three elements are printed, not two.",
        "D": "✗ Not the answer. Printing all five elements (3 4 5 6 7) would require the condition to be i < arr.length (i.e., i < 5). The actual condition is i < arr.length - 2 = i < 3, which limits the loop to the first three elements.",
    },
    23: {
        "A": "✓ CORRECT. Every AI system consists of an Agent that interacts with an Environment. The agent receives percepts from the environment through sensors and performs actions via actuators. This agent-environment loop is the universal foundation of all AI system design, from game players to self-driving cars.",
        "B": "✗ Not the answer. Data and Information describe the raw material and processed knowledge that AI systems work with, but they are inputs to an AI system rather than its structural composition. The architecture of an AI system is defined by the agent and its environment.",
        "C": "✗ Not the answer. Device and Network describe hardware and connectivity infrastructure. While AI systems run on devices and may communicate over networks, the conceptual composition of an AI system is the agent acting within its environment.",
        "D": "✗ Not the answer. Technology and Evolution describe the tools used to build AI and how AI improves over time. They are meta-level concepts about AI development, not the compositional model of what an AI system is made of.",
    },
    24: {
        "A": "✗ Not the answer. Using test data that simulates ideal scenarios describes one approach to unit testing where you test the happy path. Integration testing uses real interactions between components, not idealized simulations, because the goal is to find interface defects that only emerge when components are combined.",
        "B": "✗ Not the answer. Testing individual software components in isolation is the definition of unit testing, not integration testing. Unit tests use stubs and mocks to isolate the component under test from its dependencies.",
        "C": "✓ CORRECT. Integration testing verifies that separately developed components function correctly when brought together. It specifically targets interface defects, data flow issues, and interaction bugs that unit tests cannot detect because they only emerge when components communicate with each other.",
        "D": "✗ Not the answer. Integration testing is performed BEFORE system testing, not after it. The testing sequence is: unit testing first, then integration testing, then system testing, then acceptance testing. Performing integration only after system testing would leave interface defects undiscovered far too late.",
    },
    25: {
        "A": "✗ Not the answer. A Sprint is a time-boxed iteration within Scrum, typically lasting 1-4 weeks. It is a component or ceremony of Scrum, not a separate agile method in its own right.",
        "B": "✗ Not the answer. Six Sigma is a quality management methodology focused on defect reduction using DMAIC. While sometimes used alongside agile practices, it is not itself an agile development method.",
        "C": "✗ Not the answer. Extreme Programming (XP) is a legitimate agile methodology emphasizing practices like test-driven development, pair programming, and continuous integration. However, Scrum has wider industry adoption and is consistently described as the leading agile framework.",
        "D": "✓ CORRECT. Scrum is the most widely adopted agile development framework. It organizes work into sprints with clearly defined roles (Product Owner, Scrum Master, Development Team), events (sprint planning, daily standup, sprint review, retrospective), and artifacts (product backlog, sprint backlog, increment).",
    },
    26: {
        "A": "✗ Not the answer. Private restricts access strictly to the class that declares the member. Subclasses cannot access private members of their parent class directly, making it unsuitable when descendant classes need to use inherited instance variables.",
        "B": "✗ Not the answer. Inherited is not a valid Java access modifier. Java's four access modifiers are private, (package-private/default, no keyword), protected, and public. Using a nonexistent keyword would cause a compilation error.",
        "C": "✗ Not the answer. Public grants access from anywhere—any class in any package. While this satisfies the subclass requirement, it also exposes the variable to all external classes, which breaks encapsulation and is broader than necessary.",
        "D": "✓ CORRECT. Protected allows access from within the same class, from other classes in the same package, and from subclasses in any package. It is the precise modifier that makes instance variables accessible to both the declaring class and all descendant classes without making them publicly accessible.",
    },
    27: {
        "A": "✓ CORRECT. OSPF (Open Shortest Path First) is a Layer 3 (Network Layer) routing protocol that builds and maintains routing tables using link-state advertisements. It operates on IP networks to determine the best paths between routers and does not belong to the Data Link Layer.",
        "B": "✗ Not the answer. VLAN (Virtual LAN) is a Layer 2 technology that logically segments a network at the Data Link Layer using IEEE 802.1Q tagging on Ethernet frames. It is genuinely a data link layer technology.",
        "C": "✗ Not the answer. PPP (Point-to-Point Protocol) is a Layer 2 data link protocol used to establish direct connections between two nodes, commonly over serial links and DSL connections. It is a legitimate data link layer technology.",
        "D": "✗ Not the answer. Frame Relay is a Layer 2 WAN technology that uses frames to carry data across a packet-switched network. It operates at the data link layer and was widely used for WAN connectivity before being replaced by MPLS and broadband.",
    },
    28: {
        "A": "✗ Not the answer. Making code secure is not the purpose of any standard header file, including <iostream>. Security in C++ is achieved through careful programming practices, secure coding guidelines, and libraries like OpenSSL, not by including headers.",
        "B": "✗ Not the answer. Making code readable is a matter of code style, naming conventions, and comments. Header files declare functions and objects; they do not directly affect how readable or well-formatted the code appears.",
        "C": "✓ CORRECT. The <iostream> header declares the standard stream objects (std::cin, std::cout, std::cerr) and the operators (<< and >>) needed to use them. Including it is the prerequisite for any C++ program that reads from the keyboard or writes to the screen.",
        "D": "✗ Not the answer. Creating file streams (reading from and writing to files) is provided by the <fstream> header, which declares std::ifstream, std::ofstream, and std::fstream. The <iostream> header is strictly for standard input/output, not file I/O.",
    },
    29: {
        "A": "✗ Not the answer. Optimality means finding the best (lowest-cost) solution, not just any solution. Informed search algorithms can be optimal if their heuristic is admissible and consistent (e.g., A*), but optimality is a conditional property, not a defining characteristic of all informed search.",
        "B": "✗ Not the answer. Admissibility is a property of the heuristic function used by informed search, meaning h(n) never overestimates the true cost. It is a property of the heuristic, not of the search algorithm class as a whole.",
        "C": "✗ Not the answer. Consistency (monotonicity) is another heuristic property: h(n) <= cost(n, n') + h(n') for every successor n'. Like admissibility, it is a heuristic quality, not a defining property of informed algorithms generally.",
        "D": "✓ CORRECT. Informed search algorithms are complete when the search space is finite and the heuristic is admissible—they are guaranteed to find a solution if one exists. Completeness is the general property that distinguishes well-designed search algorithms, including informed ones that can find paths where uninformed methods would be impractical.",
    },
    30: {
        "A": "✗ Not the answer. MVC (Model-View-Controller) is a well-established software architectural style that separates application logic (Model), presentation (View), and user input handling (Controller). It is genuinely an architectural style used widely in web and desktop applications.",
        "B": "✗ Not the answer. Client-Server is a fundamental distributed architectural style where clients request services and servers provide them. It is one of the most commonly used architectural styles in networked software systems.",
        "C": "✓ CORRECT. UML (Unified Modeling Language) is a visual notation standard for modeling software systems using diagrams such as class diagrams, sequence diagrams, and use case diagrams. It is a modeling language used to document and communicate designs, not an architectural style for organizing system components.",
        "D": "✗ Not the answer. The OSI layer model is a networking reference model that describes how network protocols interact in seven layers. While sometimes confused with architecture, it is a network protocol framework, not a software architectural style for structuring application components.",
    },
    31: {
        "A": "✗ Not the answer. While it is true that exhaustive testing is impossible (you cannot test every possible input), this is a limitation of testing, not a principle that saves time and cost. Acknowledging this limitation helps testers prioritize but does not itself reduce costs.",
        "B": "✓ CORRECT. Detecting defects early, during requirements analysis or design, is far cheaper than discovering them after code has been written. The cost of fixing a defect multiplies at each stage: a design flaw caught in design costs 10x less to fix than the same flaw found during system testing.",
        "C": "✗ Not the answer. Risk-based testing prioritization is a valuable strategy for focusing effort where it matters most. However, the principle that most directly saves time and cost is the early testing principle, because it prevents defects from compounding into expensive rework.",
        "D": "✗ Not the answer. Testing the entire development process does not reduce time and cost—it increases them if done without focus. This statement confuses thorough testing with efficient testing. Early testing is what saves cost, not exhaustive coverage of all phases.",
    },
    32: {
        "A": "✗ Not the answer. Both DA and UCS are optimal for finding shortest paths when edge weights are non-negative. Claiming DA is optimal but not UCS inverts the truth; UCS is designed specifically to find the optimal path to the goal state in AI search problems.",
        "B": "✓ CORRECT. UCS (Uniform Cost Search) is a goal-directed algorithm that expands nodes in order of path cost and stops when the goal is reached, guaranteeing the optimal solution to that goal. Dijkstra's Algorithm processes the entire graph to find shortest paths to all nodes, without a specific stopping criterion for a single goal.",
        "C": "✗ Not the answer. This reverses the actual behavior. Dijkstra's Algorithm uses a priority queue and processes nodes as the queue dictates. UCS also uses a priority queue. The claim that DA collects into a queue while UCS discovers nodes as they come contradicts how both algorithms work.",
        "D": "✗ Not the answer. This also inverts the description incorrectly. Both algorithms use priority queues. The meaningful distinction is that UCS is goal-directed (stops at the goal) while DA computes all-pairs shortest paths from the source without a specific stopping goal.",
    },
    33: {
        "A": "✗ Not the answer. The F-measure (F1 score) is the harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall). It balances both metrics into a single score but is not itself the ratio of genuine faults to predicted faults.",
        "B": "✗ Not the answer. Recall (sensitivity) is TP / (TP + FN)—it measures how many of the actually faulty segments the model caught. The question asks about genuine faults relative to total predicted faults, which is precision, not recall.",
        "C": "✗ Not the answer. Accuracy is (TP + TN) / total—the proportion of all predictions that are correct. It includes both correct fault and correct non-fault predictions and is not the ratio of genuine faults to anticipated faults.",
        "D": "✓ CORRECT. Precision is TP / (TP + FP): among all segments the model predicted as faulty, what fraction are genuinely faulty? The question describes this exactly—genuine imperfect segments divided by total segments anticipated as faulty. High precision means fewer false alarms.",
    },
    34: {
        "A": "✗ Not the answer. An empty tree (null or no nodes) is indeed a valid binary tree by the recursive definition. The base case of a binary tree is the empty tree. This statement is TRUE about binary trees.",
        "B": "✗ Not the answer. Visualizing a binary tree as a root with two disjoint subtrees (left and right, either of which may be empty) is a standard and correct recursive description of a binary tree. This statement is TRUE.",
        "C": "✗ Not the answer. Saying each node has zero, one, or two children is the core definition of a binary tree. Every node has at most two children; it may also have one or zero. This statement is TRUE.",
        "D": "✓ CORRECT. Claiming a tree is binary only if every node has zero children would mean only trees consisting entirely of leaf nodes (no internal nodes) qualify—which is clearly wrong. Binary tree nodes can have zero, one, or two children. This statement is FALSE and therefore the answer to 'which is not true.'",
    },
    35: {
        "A": "✓ CORRECT. In C++ (and Java), a switch statement without break statements exhibits fall-through: once execution enters a matching case, it continues sequentially through all subsequent case blocks regardless of their label values. Every case after the match executes until a break, return, or the end of the switch is reached.",
        "B": "✗ Not the answer. The absence of a break statement does not cause an exception. Fall-through is valid, legal behavior in C++ and Java. No runtime error or exception is thrown; execution simply continues into the next case block.",
        "C": "✗ Not the answer. The default block only executes when no case label matches the switch expression, OR when fall-through reaches it from a previous case. Omitting break statements does not cause the default block to execute exclusively; it causes all subsequent cases to execute.",
        "D": "✗ Not the answer. The program does not halt due to missing break statements. The switch statement is not a loop and missing break does not cause an infinite loop or program termination; it simply lets execution continue into the next case.",
    },
    36: {
        "A": "✗ Not the answer. Software design is the phase where architectural and detailed design decisions are made. Security considerations are certainly applied during design, but security estimation as a formal activity—identifying threats, estimating likelihood and impact—is a risk management function, not a design function.",
        "B": "✗ Not the answer. Software development encompasses the coding and implementation phases. Developers apply security measures while coding (input validation, encryption), but the formal process of estimating security risks belongs to risk management, which precedes and guides development.",
        "C": "✗ Not the answer. SRS (Software Requirements Specification) design addresses capturing and documenting requirements. Security requirements may appear in the SRS, but security estimation—the systematic assessment of security threats—is a risk management activity.",
        "D": "✓ CORRECT. Risk management is the process that identifies potential threats to a project or product, estimates their likelihood and impact, and plans mitigation strategies. Security estimation fits naturally here because assessing security vulnerabilities, their probability of exploitation, and their potential damage is a core risk management task.",
    },
    37: {
        "A": "✗ Not the answer. Multiprogramming is an operating system technique that keeps multiple processes in memory simultaneously to maximize CPU utilization. While the OS may use queues internally to manage process states, multiprogramming itself is not an application of queues.",
        "B": "✗ Not the answer. OS job scheduling (print queues, CPU scheduling with equal priority) is a DIRECT application of queues—jobs literally wait in a FIFO queue. The question asks for the INDIRECT application, which is a different category.",
        "C": "✓ CORRECT. An indirect application of a queue is when the queue serves as an auxiliary data structure inside another algorithm. Breadth-First Search (BFS) is the classic example: BFS uses a queue to track which nodes to visit next, making the queue a helper rather than the primary purpose.",
        "D": "✗ Not the answer. Simulating real-world waiting lines (ticket counters, bank tellers) is a DIRECT application of queues because the simulation models a queue explicitly. Direct applications are those where the queue concept is the main idea being modeled.",
    },
    38: {
        "A": "✗ Not the answer. Staged delivery is a software development strategy that releases the product in incremental stages to get early feedback. It can help manage changing requirements but is a delivery model rather than a change-tracking mechanism that specifically reduces rework cost.",
        "B": "✗ Not the answer. Prototyping creates early working models to validate requirements with stakeholders before full development. It helps clarify requirements but does not directly manage code changes or reduce rework cost once development is underway.",
        "C": "✗ Not the answer. The Spiral model incorporates risk analysis and iteration but is a full development lifecycle model. It addresses requirement uncertainty through repeated cycles rather than providing a mechanism to track and reverse code changes efficiently.",
        "D": "✓ CORRECT. Software Version Control (e.g., Git) tracks every change to source code, stores the history of all revisions, supports branching for parallel development, and allows rollback to any prior state. When requirements change, version control minimizes rework cost by enabling teams to revert, branch, and merge changes systematically.",
    },
    39: {
        "A": "✗ Not the answer. A program (in project management terms) is a collection of related projects managed in a coordinated way to obtain benefits not available from managing them individually. A program is ongoing across multiple projects, not a single temporary endeavor.",
        "B": "✗ Not the answer. A portfolio is a collection of projects, programs, and operations managed together to achieve strategic business objectives. It is not temporary or unique in the same sense; it persists as long as the strategic goals require.",
        "C": "✓ CORRECT. A project is formally defined as a temporary endeavor with a definite start and end, undertaken to create a unique product, service, or result. Temporary and unique are the two key distinguishing characteristics. This PMBOK definition is the standard definition used in project management.",
        "D": "✗ Not the answer. A process is a repeatable, ongoing set of activities performed routinely (e.g., the payroll process, the build process). Processes are not temporary and do not create unique outputs; they produce standardized, repeated results.",
    },
    40: {
        "A": "✓ CORRECT. System design translates verified requirements into an architecture, identifying components, their interactions, and data flows. It belongs to the design phase of the SDLC. Requirement validation, elicitation, and analysis all belong to the requirements engineering phase, making system design the odd one out.",
        "B": "✗ Not the answer. Requirement validation is a requirements engineering activity that checks whether the documented requirements are correct, complete, consistent, and verifiable. It belongs with the other requirements activities.",
        "C": "✗ Not the answer. Requirement elicitation is the process of gathering requirements from stakeholders through interviews, workshops, prototyping, and observation. It is the first step in requirements engineering.",
        "D": "✗ Not the answer. Requirement analysis refines raw requirements by resolving conflicts, prioritizing, modeling, and checking feasibility. It is a core requirements engineering activity, alongside elicitation and validation.",
    },
    41: {
        "A": "✓ CORRECT. Gradient descent is the foundational optimization algorithm in machine learning. It iteratively adjusts model parameters in the direction opposite to the gradient of the loss function, minimizing the error. Variants such as SGD, mini-batch GD, and Adam are all built on this principle.",
        "B": "✗ Not the answer. Bagging (Bootstrap Aggregating) is an ensemble learning technique that trains multiple models on random subsets of training data and averages their predictions. It reduces variance and improves accuracy but is not an optimization algorithm for training a single model.",
        "C": "✗ Not the answer. Lasso (Least Absolute Shrinkage and Selection Operator) is a regularization technique that adds an L1 penalty to the loss function to shrink less important feature weights to zero, performing feature selection. It is not an optimization algorithm itself.",
        "D": "✗ Not the answer. Gradient Boosting is an ensemble technique that builds models sequentially, each correcting the errors of the previous one. Despite the word 'gradient' in its name, it is an ensemble learning strategy, not the core optimization algorithm used to minimize a model's loss function.",
    },
    42: {
        "A": "✗ Not the answer. UNIQUE is a constraint keyword applied to column or table definitions in CREATE TABLE or ALTER TABLE statements to enforce uniqueness in stored data. It is not a SELECT clause keyword for removing duplicates from query results.",
        "B": "✓ CORRECT. DISTINCT placed immediately after SELECT tells the database engine to eliminate duplicate rows from the result. For example, SELECT DISTINCT department FROM employees returns each department name only once, even if multiple employees share the same department.",
        "C": "✗ Not the answer. GROUP BY groups rows with the same values in specified columns and is used with aggregate functions (COUNT, SUM, AVG). While grouping produces one row per group, its purpose is aggregation, not duplicate elimination from a non-aggregated result.",
        "D": "✗ Not the answer. PRIMARY is the keyword used in PRIMARY KEY constraint definitions, not a SELECT clause operator. It identifies the primary key of a table at the schema level and has no role in filtering or removing duplicates from query output.",
    },
    43: {
        "A": "✗ Not the answer. Data protection—hiding internal state from external access—is the goal of encapsulation, not inheritance. Encapsulation uses access modifiers (private, protected) to shield object internals. Inheritance is about sharing and reusing behavior across a class hierarchy.",
        "B": "✓ CORRECT. Inheritance allows a subclass to reuse the attributes and methods of its parent class without duplicating code. Common logic is written once in the superclass and inherited by all subclasses, making the codebase smaller, more consistent, and easier to maintain.",
        "C": "✗ Not the answer. Resource saving may be a side effect of code reuse, but it is not the primary purpose of inheritance. The motivation for inheritance is the developer's ability to reuse and extend existing class behavior, which incidentally also saves computational or storage resources.",
        "D": "✗ Not the answer. Providing multiple forms for methods (the same method name behaving differently for different types) is the goal of polymorphism, specifically method overloading and overriding. Inheritance enables overriding to occur, but polymorphism is the principle that multiple forms characterizes.",
    },
    44: {
        "A": "✗ Not the answer. java.lang.class is not a valid fully-qualified class name in Java's standard library. The actual class that represents types at runtime is java.lang.Class (capital C), and it is not the base class of all objects—that role belongs to java.lang.Object.",
        "B": "✗ Not the answer. java.class.inherited is not a real class or package in Java. This option is designed to test whether you know the correct package structure (java.lang) and class name (Object).",
        "C": "✓ CORRECT. Every class in Java implicitly extends java.lang.Object if no explicit superclass is declared. This gives all objects built-in methods including toString(), equals(Object obj), hashCode(), and wait()/notify() for threading. It is the root of Java's entire class hierarchy.",
        "D": "✗ Not the answer. java.class.object is not a real Java package or class. The correct package is java.lang and the correct class name is Object (with a capital O). Misspelled or incorrectly structured class names like this do not exist in the Java standard library.",
    },
    45: {
        "A": "✓ CORRECT. Card Layout is a layout manager from Java's AWT/Swing library used for desktop Java applications. It stacks multiple panels like a deck of cards and shows one at a time. Android has its own set of layout classes and Card Layout is not among them.",
        "B": "✗ Not the answer. LinearLayout is a standard Android layout that arranges its child views in a single horizontal row or vertical column, depending on the orientation attribute. It is one of the most commonly used Android layouts.",
        "C": "✗ Not the answer. RelativeLayout is a standard Android layout that positions child views relative to each other or relative to the parent container using attributes like layout_toRightOf or layout_below. It is a built-in Android layout.",
        "D": "✗ Not the answer. FrameLayout is a standard Android layout designed to display a single child view or to layer multiple children on top of each other. It is commonly used for fragments and overlays in Android applications.",
    },
    46: {
        "A": "✗ Not the answer. border-circle is not a valid CSS property. CSS does not have a property with this name. You can create a circle by setting border-radius to 50% on a square element, but border-circle itself does not exist.",
        "B": "✗ Not the answer. border-rounded is not a valid CSS property name. Developers sometimes expect this to exist intuitively, but the actual CSS property for rounded corners is border-radius.",
        "C": "✓ CORRECT. border-radius is the CSS property that sets the radius of an element's corner curves. For example, border-radius: 8px rounds all four corners by 8 pixels. Setting border-radius: 50% on a square element creates a perfect circle.",
        "D": "✗ Not the answer. border-corner is not a valid CSS property. No CSS specification defines this property. Rounded corners are exclusively controlled by border-radius and its directional variants (border-top-left-radius, etc.).",
    },
    47: {
        "A": "✓ CORRECT. An Affinity Diagram is a project quality and management tool for organizing large volumes of ideas, facts, or opinions into natural groupings based on their affinity (similarity). Teams write ideas on cards or sticky notes and cluster related ones together for structured analysis.",
        "B": "✗ Not the answer. Activity-on-Node (AON) is a network diagramming technique used in project schedule management to represent activities as nodes and dependencies as arrows, helping to identify the critical path. It organizes tasks, not ideas.",
        "C": "✗ Not the answer. An Activity List is a project planning document that enumerates all scheduled activities required to complete project work. It is a planning artifact, not a technique for classifying and grouping large numbers of ideas.",
        "D": "✗ Not the answer. Adaptive Life Cycle is an agile or change-driven project management approach where the scope is refined iteratively as the project progresses. It is a project lifecycle model, not a tool for grouping and analyzing ideas.",
    },
    48: {
        "A": "✗ Not the answer. Integrity in the CIA triad means protecting data from unauthorized modification or tampering. An integrity violation occurs when data is altered or corrupted without authorization, not when it is disclosed to unauthorized parties.",
        "B": "✓ CORRECT. Confidentiality is the principle that sensitive information must only be accessible to authorized parties. Unauthorized disclosure—revealing data to someone not permitted to see it—is a confidentiality violation. Encryption, access controls, and need-to-know policies enforce confidentiality.",
        "C": "✗ Not the answer. Authentication is the process of verifying the identity of a user, device, or process—confirming that someone is who they claim to be. It is a prerequisite for authorization but does not itself describe unauthorized disclosure.",
        "D": "✗ Not the answer. Authorization determines what an authenticated entity is permitted to do or access. A failure of authorization can lead to unauthorized disclosure, but authorization itself refers to access rights management, not to the disclosure event itself.",
    },
    49: {
        "A": "✓ CORRECT. Introducing a new culture of data usage describes a broad organizational transformation outcome, not a direct analytical contribution of big data technologies. Big data tools analyze data; culture change is a human and organizational outcome that may result from insights, but it is not what the analysis itself contributes.",
        "B": "✗ Not the answer. Gaining competitive advantage is a primary business contribution of big data analysis. Organizations that can analyze large datasets faster and more accurately than competitors can make better decisions, identify opportunities earlier, and respond more effectively to market changes.",
        "C": "✗ Not the answer. Coping with a volatile market is a genuine contribution. Big data analytics enables real-time monitoring of market signals, demand shifts, and supply chain disruptions, allowing businesses to adapt quickly to unpredictable conditions.",
        "D": "✗ Not the answer. Satisfying customer needs is a direct contribution of big data analysis. By analyzing purchase patterns, usage data, and customer feedback at scale, organizations can personalize products, services, and marketing to better match what customers want.",
    },
    50: {
        "A": "✗ Not the answer. Using commas instead of semicolons between the three parts is a syntax error in Java, C, C++, and JavaScript. The for loop header requires semicolons as separators: for(init; condition; update). Commas are used to separate multiple expressions within a single part, not to separate the parts themselves.",
        "B": "✗ Not the answer. for(initialization; condition) is incomplete—it is missing the update expression. A for loop requires all three parts separated by semicolons. An incomplete header causes a compilation error.",
        "C": "✗ Not the answer. for(increment/decrement; initialization; condition) has the three parts in the wrong order. The correct order is always initialization first, then condition, then update. Swapping initialization and condition means the update expression would be evaluated as the condition, producing incorrect behavior.",
        "D": "✓ CORRECT. The correct for loop syntax is for(initialization; condition; increment/decrement). Initialization runs once before the loop starts, the condition is checked before each iteration, and the update expression runs after each iteration body. This order is consistent across Java, C, C++, and JavaScript.",
    },
    51: {
        "A": "✓ CORRECT. The cost of change increases exponentially with project phase. If a requirement is added late—during coding or testing—the team must redesign components, rewrite code that was already completed, and re-run tests. This rework multiplies the original implementation cost many times over.",
        "B": "✗ Not the answer. Coding complexity increases with late requirements because new features must integrate with existing, already-completed code. However, the root cause that makes late changes discouraged is not technical complexity but the economic cost of rework across all affected artifacts.",
        "C": "✗ Not the answer. Analysis complexity may increase when new requirements must be reconciled with existing ones. However, the analysis effort alone is smaller than the total rework cost that cascades through design, coding, and testing when a late requirement arrives.",
        "D": "✗ Not the answer. Requirement complexity—the internal complexity of understanding what is needed—is a challenge during elicitation and analysis, not the primary reason late introductions are discouraged. A complex requirement introduced on time is far less costly than a simple requirement introduced late.",
    },
    52: {
        "A": "✗ Not the answer. Network authorization controls what authenticated users are permitted to access on a network. It does not verify the integrity or authenticity of specific messages exchanged between communicating processes.",
        "B": "✗ Not the answer. A decryption algorithm reverses encryption to recover plaintext, but it alone cannot verify that a message was not tampered with or that it came from the claimed sender. Decryption is one step within a larger security scheme.",
        "C": "✗ Not the answer. A Message Digest (hash) produces a fixed-length fingerprint of a message that detects tampering but does not authenticate the sender. Anyone can compute a hash; a message digest alone cannot prove the identity of the message originator.",
        "D": "✓ CORRECT. A Digital Signature combines hashing and asymmetric encryption: the sender hashes the message and encrypts the hash with their private key. The receiver decrypts with the sender's public key and re-hashes the message to confirm both integrity (not tampered) and authenticity (from the claimed sender). This is the correct mechanism for verifying inter-process message integrity.",
    },
    53: {
        "A": "✓ CORRECT. A back-end component is an architectural concept in multi-tier web applications referring to server-side logic. It is not a structural element of a fundamental program. All programs—regardless of architecture—consist of variable definitions, a main() entry point, and input/output features.",
        "B": "✗ Not the answer. Variable definitions are a core structural element of any program. Variables store the data the program operates on, and every meaningful program declares at least some variables.",
        "C": "✗ Not the answer. The main() method (or equivalent entry point) is the starting point of program execution in languages like Java, C, and C++. Without it, the runtime has no place to begin executing the program.",
        "D": "✗ Not the answer. Input/output features allow the program to communicate with users or external systems. Without I/O (even something as simple as printing a result), a program produces no observable effect and serves no practical purpose.",
    },
    54: {
        "A": "✗ Not the answer. For sequence 12, 14, 3, 9, 4, 18, 21: inserting 12 at slot 12, then 14 at slot 14, then 3 at slot 3, then 9 at slot 9—but at this point slot 9 should be empty. However when 4 comes, it hashes to slot 4. Then 18 hashes to slot 8 (18 mod table_size). Tracing this sequence reveals it cannot produce the given table state through valid linear probing.",
        "B": "✗ Not the answer. Sequence 9, 14, 4, 18, 12, 3, 21: inserting 9 first places it at slot 9, then 14 at slot 14, etc. Checking the linear probing trace against the final table state shows this order does not produce the correct slot assignments.",
        "C": "✗ Not the answer. Sequence 12, 9, 18, 3, 14, 21, 4: tracing each insertion with linear probing shows that some elements cannot reach their required final positions in this order, making this sequence inconsistent with the given table.",
        "D": "✓ CORRECT. With the identity function f(x)=x, inserting 12, 3, 14, 18, 4, 9, 21 in that order and resolving collisions by linear probing produces exactly the table state shown in the question. Each element finds its slot consistently: 12 at 12, 3 at 3, 14 at 14, 18 at 8 (or its probed slot), and so on.",
    },
    55: {
        "A": "✗ Not the answer. Integrity in software quality refers to the correctness and consistency of data—ensuring data is accurate and not corrupted. It is a data quality attribute, not a system-level property describing behavior under unexpected conditions.",
        "B": "✓ CORRECT. Robustness is the ability of a system to continue functioning correctly despite unexpected inputs, component failures, or environmental disturbances. A robust system handles edge cases, hardware failures, and invalid data gracefully rather than crashing or producing incorrect results.",
        "C": "✗ Not the answer. Maintainability measures how easily software can be modified, corrected, or extended. A maintainable system has clean code, good documentation, and modular design. It is about ease of change, not about tolerating unexpected runtime conditions.",
        "D": "✗ Not the answer. Reliability is the probability that a system operates without failure over a specified period under normal operating conditions. It measures how often the system works as expected in typical use. Robustness specifically addresses behavior under abnormal or unexpected conditions, which is what the question describes.",
    },
    56: {
        "A": "✗ Not the answer. Speed of storage consumption would describe how quickly disk or memory fills up with data—a capacity concern. Velocity is specifically about how fast new data is being produced and entering the system, not how quickly storage is being consumed.",
        "B": "✗ Not the answer. Speed of data ingestion refers to how fast the system can receive and absorb incoming data—a processing capacity metric. Velocity is about the rate at which data is being generated at the source, which then drives the need for fast ingestion.",
        "C": "✓ CORRECT. Velocity in big data refers to the speed at which new data is generated. Social media creates millions of posts per second, sensors emit readings continuously, and financial systems log thousands of transactions per minute. This high generation rate demands real-time or near-real-time processing pipelines.",
        "D": "✗ Not the answer. Speed of data processing and storing describes throughput capability of the data platform—how fast it can handle data after it arrives. This is a system performance attribute, not the big data characteristic that velocity is named for.",
    },
    57: {
        "A": "✗ Not the answer. The Manifest (AndroidManifest.xml) is a configuration file that declares app components, permissions, and metadata. It does not display any UI on screen; it is read by the Android system at install and launch time.",
        "B": "✗ Not the answer. An Intent is a messaging object used to request an action from another app component, such as starting an Activity or Service. Intents communicate between components but do not themselves render anything on screen.",
        "C": "✓ CORRECT. A View is the fundamental UI building block in Android. Every button, text field, image, checkbox, and layout is a View or a subclass of View (ViewGroup for containers). Views are what actually appear on screen within an Activity.",
        "D": "✗ Not the answer. A Fragment is a modular section of an Activity's UI and behavior, representing a reusable portion of a screen. While Fragments display UI, they are composed of Views and depend on an Activity host. The base class for all visible UI elements is View.",
    },
    58: {
        "A": "✗ Not the answer. STUDENT having total participation would mean every student must be assigned to a dorm. The rule states that every DORM must have a student, not that every student must have a dorm. Total participation applies to the entity that must always be in the relationship.",
        "B": "✗ Not the answer. STUDENT having existence dependency would mean students cannot exist without a dorm. But the constraint is on DORM: a dorm cannot exist without students. Existence dependency follows the direction of the rule.",
        "C": "✗ Not the answer. DORM having partial participation would mean some dorms may have no students at all—the opposite of the stated rule. Partial participation means participation is optional, not mandatory.",
        "D": "✓ CORRECT. The rule says every DORM must have at least one student, meaning DORM cannot exist in the database without being linked to a student. This is existence dependency: DORM's existence depends on its association with STUDENT. This also implies DORM has total participation in the relationship.",
    },
    59: {
        "A": "✗ Not the answer. Bootstrap is the general concept of a self-starting process—the idea of pulling oneself up by one's bootstraps. In computing it refers to the overall startup sequence, not specifically to the program that initializes hardware and loads the OS.",
        "B": "✗ Not the answer. Cache memory is a small, fast hardware memory layer between the CPU and main memory that stores frequently accessed data to reduce latency. It is a hardware component, not a program that initializes the system.",
        "C": "✓ CORRECT. The bootloader is the specific program (stored in ROM or firmware) that initializes all hardware components—CPU registers, device controllers, and main memory—and then locates and loads the operating system kernel into memory to start execution.",
        "D": "✗ Not the answer. BIOS (Basic Input/Output System) is firmware embedded in the motherboard that runs the Power-On Self Test (POST) and then hands control to the bootloader. BIOS starts the bootloader; it does not itself fully initialize the system and load the OS in the way the bootloader does.",
    },
    60: {
        "A": "✗ Not the answer. Abstraction simplifies complex reality by exposing only essential details and hiding implementation specifics through abstract classes and interfaces. Method overriding is not a characteristic of abstraction; overriding provides concrete implementations for abstract methods.",
        "B": "✗ Not the answer. Inheritance establishes parent-child relationships that enable method overriding to exist, but inheritance itself describes the IS-A relationship and code reuse mechanism. Method overriding is the mechanism; polymorphism is the principle it characterizes.",
        "C": "✗ Not the answer. Encapsulation bundles data and methods within a class and restricts direct access to internal state using access modifiers. It is about data hiding and controlled access, not about a method behaving differently based on the object's runtime type.",
        "D": "✓ CORRECT. Method overriding is runtime polymorphism (dynamic dispatch): a subclass provides its own implementation of a method defined in its superclass. At runtime, the JVM calls the overriding method based on the actual object type, not the reference type—one interface, multiple behaviors.",
    },
    61: {
        "A": "✓ CORRECT. A Code Auditor is a CASE tool that statically analyzes source code against defined coding standards, style rules, and quality metrics without executing the program. Tools such as Checkstyle, PMD, FindBugs, and SonarQube are examples that flag code quality violations.",
        "B": "✗ Not the answer. Documenters (or documentation generators) automatically produce human-readable documentation from source code comments and signatures. Tools like Javadoc extract API documentation. They improve documentation quality but do not check code against coding standards.",
        "C": "✗ Not the answer. Test Data Generators create synthetic input data for test cases, including boundary values, equivalence class representatives, and random inputs. They support test execution but do not analyze code quality.",
        "D": "✗ Not the answer. Interactive Debuggers (like gdb, jdb, or IDE debuggers) allow developers to step through code execution, inspect variable values, and set breakpoints at runtime. They help find runtime bugs but do not check code against standards statically.",
    },
    62: {
        "A": "✗ Not the answer. A Compiler translates high-level source code into machine code or bytecode, producing an executable or object file. It is a translation tool that runs at compile time, not software that resides in main memory during program execution.",
        "B": "✓ CORRECT. The Loader is the system software component that reads an executable file from secondary storage, allocates main memory, loads the program's code and data into memory, and transfers control to the program's entry point. It actively resides in main memory during the loading process.",
        "C": "✗ Not the answer. Executor is not a standard system software component. Execution is performed by the CPU under the control of the operating system's process manager, not by a separate piece of software called an executor.",
        "D": "✗ Not the answer. The Linker combines multiple object files and libraries into a single executable by resolving external symbol references. Linking typically occurs before loading (static linking) or at load/run time (dynamic linking), but the linker itself does not reside in main memory as runtime system software.",
    },
    63: {
        "A": "✗ Not the answer. Overriding allows a subclass to redefine a method inherited from its superclass with the same name, return type, and parameter list. This is runtime polymorphism where the method signature is identical across classes, not different parameter/return types.",
        "B": "✗ Not the answer. Inheritance defines the IS-A relationship between classes and enables method reuse and overriding. It is the mechanism that makes polymorphism possible but is not itself the principle describing multiple methods with the same name and different signatures.",
        "C": "✗ Not the answer. Encapsulation bundles data with the methods that operate on it and hides internal implementation details. It does not describe creating multiple methods with the same name but different type signatures.",
        "D": "✓ CORRECT. Polymorphism through method overloading (compile-time polymorphism) allows a class to define several methods with the same name but differing in the number, type, or order of parameters. The compiler selects the correct method at compile time based on the argument types provided.",
    },
    64: {
        "A": "✗ Not the answer. Modularity—the ability to divide a program into self-contained, reusable components—is a positive criterion for language selection. Languages that support strong modularity (through classes, modules, packages, or namespaces) lead to more maintainable codebases.",
        "B": "✓ CORRECT. Platform dependency is a disadvantage, not a selection criterion. A language that binds you to a specific operating system or hardware limits deployment flexibility. Desirable languages are platform-independent or at least portable, so platform dependency is the characteristic you want to avoid.",
        "C": "✗ Not the answer. Portability—the ability to run on multiple platforms without modification—is a valuable criterion. Highly portable languages (like Java or Python) reduce deployment costs and increase the reach of the software.",
        "D": "✗ Not the answer. Code efficiency—how well the generated code uses CPU cycles and memory—is a key criterion especially for performance-critical, embedded, or resource-constrained applications. Languages like C and C++ are chosen partly for their code efficiency.",
    },
    65: {
        "A": "✗ Not the answer. CLR (Common Language Runtime) is the virtual machine of Microsoft's .NET platform. It executes .NET bytecode (MSIL/CIL) for languages like C# and VB.NET. CLR is a Microsoft technology with no relationship to Android.",
        "B": "✗ Not the answer. Docker is a containerization platform that packages applications and their dependencies into portable containers. It is not a virtual machine and is not part of Android's runtime architecture.",
        "C": "✓ CORRECT. Android originally used the Dalvik Virtual Machine (DVM), designed specifically for mobile devices with limited RAM and battery. Dalvik used JIT (just-in-time) compilation and ran .dex (Dalvik Executable) files. Later versions replaced Dalvik with ART (Android Runtime), which uses AOT compilation.",
        "D": "✗ Not the answer. The JVM (Java Virtual Machine) runs standard Java bytecode (.class files) on desktop and server platforms. Although Android apps are written in Java/Kotlin, the Android runtime (Dalvik/ART) runs .dex files optimized for mobile, not the standard JVM.",
    },
    66: {
        "A": "✗ Not the answer. onRestart() is called when an Activity that was previously stopped (but not destroyed) is being restarted and returned to the foreground. It comes after onStop() and before onStart() in the restart path—not the initial creation path.",
        "B": "✓ CORRECT. onCreate() is the very first lifecycle callback invoked when the system creates an Activity. In onCreate() you initialize the UI (setContentView()), bind views to variables, set up adapters, and restore any saved state from the Bundle parameter.",
        "C": "✗ Not the answer. onClick() is an event listener method called when the user taps a UI element. It is a UI interaction event, not a lifecycle callback, and is not invoked automatically by the Android system as part of the Activity lifecycle sequence.",
        "D": "✗ Not the answer. onStart() is the second lifecycle callback, called after onCreate() when the Activity becomes visible to the user but before it gains user focus. It is not the first; onCreate() always precedes onStart().",
    },
    67: {
        "A": "✗ Not the answer. Android Phone Kit is an invented expansion that does not correspond to any official Android acronym. APK has nothing to do with the device type (phone).",
        "B": "✓ CORRECT. APK stands for Android Package Kit (sometimes called Android Application Package). An APK file is the distribution format for Android apps, bundling the compiled code (.dex files), resources, assets, and AndroidManifest.xml into a single installable archive.",
        "C": "✗ Not the answer. Android Page Kit is a fabricated expansion. APK describes a package (the installable bundle), not a page or webpage-related concept.",
        "D": "✗ Not the answer. Android Platform Kit is another incorrect expansion. While APK files are designed to run on the Android platform, the P stands for Package, not Platform.",
    },
    68: {
        "A": "✗ Not the answer. The Pairwise principle is not a standard quality management principle. In testing, pairwise testing (all-pairs testing) is a technique for combinatorial test case reduction, which is a different concept entirely from the 80/20 rule.",
        "B": "✗ Not the answer. The Partition principle is not the name of the 80/20 principle. Partitioning in testing refers to equivalence partitioning, which divides input space into equivalent groups for test case design.",
        "C": "✓ CORRECT. The Pareto Principle (80/20 rule), named after economist Vilfredo Pareto, states that 80% of effects come from 20% of causes. In software quality management this means 80% of defects come from 20% of the code, so fixing that 20% with 20% of the effort resolves most problems.",
        "D": "✗ Not the answer. The Parametric principle is not a recognized quality management principle. In project management, parametric estimation uses statistical relationships between parameters to estimate cost or duration, which is unrelated to the 80/20 rule.",
    },
    69: {
        "A": "✗ Not the answer. In generalization, attributes and operations of higher-level (superclass) entities are indeed inherited by lower-level (subclass) entities. Subclasses automatically have everything their superclass has, plus their own additions. This statement is TRUE about generalization.",
        "B": "✓ CORRECT. This statement is FALSE and therefore the answer. In generalization, higher-level classes (superclasses) are MORE GENERAL, not more specific. Lower-level classes (subclasses) are MORE SPECIFIC because they add additional specialized attributes and operations to those inherited from the superclass.",
        "C": "✗ Not the answer. Generalization does facilitate easy data modification because common attributes and behaviors are centralized in the superclass. Changing the superclass automatically propagates to all subclasses. This is a true benefit of generalization.",
        "D": "✗ Not the answer. Keeping common information in one place (the superclass) is a fundamental advantage of generalization that avoids duplication and ensures consistency. This is a true characteristic of the generalization relationship in UML.",
    },
    70: {
        "A": "✗ Not the answer. The autocomplete attribute (not action) controls whether the browser should automatically fill in form field values based on the user's past entries. action and autocomplete are different attributes serving different purposes.",
        "B": "✗ Not the answer. The HTTP method (GET or POST) is specified by the method attribute of the <form> element. The action attribute specifies the destination URL, not which HTTP method to use.",
        "C": "✗ Not the answer. The action attribute does not describe what action is happening in a natural language sense. It is a URL-valued attribute that tells the browser where to send the form data, not a description of the user's action.",
        "D": "✓ CORRECT. The action attribute of an HTML <form> element specifies the URL to which the form data is submitted when the user clicks the submit button. For example, action='/submit' sends the data to the /submit endpoint. If action is omitted, the form submits to the current page URL.",
    },
    71: {
        "A": "✗ Not the answer. Variance in project management is the difference between planned and actual performance (cost variance, schedule variance). It is a project monitoring metric, not a quality assurance activity that assures a product meets stakeholder needs.",
        "B": "✗ Not the answer. SWOT Analysis evaluates Strengths, Weaknesses, Opportunities, and Threats of a project or organization. It is a strategic planning tool, not a quality assurance technique that confirms product fitness for purpose.",
        "C": "✓ CORRECT. Validation confirms that the product meets the actual needs of customers and stakeholders—that the right product was built. The question's description of checking that needs are met maps precisely to validation. The classic phrase is: verification = built it right; validation = built the right thing.",
        "D": "✗ Not the answer. Verification confirms that the product conforms to its documented specification—that it was built correctly according to the spec. Verification checks internal correctness, while validation checks external fitness for stakeholder needs.",
    },
    72: {
        "A": "✗ Not the answer. Making a primary key non-editable is a recommended practice in many systems (surrogate keys should not change once assigned), but it is not the defining constraint of a primary key in relational theory. The core constraint is uniqueness and NOT NULL.",
        "B": "✓ CORRECT. A primary key must satisfy two constraints: it must be UNIQUE (no two rows can have the same value) and it must be NOT NULL (every row must have a value). Together these ensure every row has a distinct, defined identifier. Allowing NULL would mean some rows lack an identity.",
        "C": "✗ Not the answer. Limiting the primary key to a range of values (e.g., IDs between 1 and 1000) is a business rule constraint on key values, not a defining property of the primary key concept in relational databases.",
        "D": "✗ Not the answer. Defining a primary key as NULL is the exact opposite of the correct constraint. A NULL primary key would mean the row has no identifier, violating entity integrity. Primary keys are explicitly required to be NOT NULL.",
    },
    73: {
        "A": "✗ Not the answer. De-capsulation (or decapsulation) is the reverse process: as data travels up the receiving host's protocol stack, each layer strips off the header (and trailer) added by the corresponding layer on the sending side.",
        "B": "✗ Not the answer. Routing is the process of selecting the best path for a packet to travel from source to destination across interconnected networks. Routers route packets based on destination IP addresses but do not add headers to data as it moves down the stack.",
        "C": "✗ Not the answer. Switching forwards frames within a local network segment based on MAC addresses. Switches operate at Layer 2 and forward frames without adding new headers to the data payload.",
        "D": "✓ CORRECT. Encapsulation is the process of adding a protocol header (and sometimes a trailer) to data as it passes down through each OSI layer. Application data gets a TCP/UDP header, then an IP header, then a MAC header, creating increasingly larger protocol data units for transmission.",
    },
    74: {
        "A": "✗ Not the answer. While technological evolution can make some legacy systems obsolete, making existing systems obsolete is a secondary effect. The primary consequence that drives industry and research is the demand for new architectures capable of handling new requirements and scale.",
        "B": "✓ CORRECT. As business models and available technologies evolve rapidly, existing software architectures often cannot accommodate new scalability, integration, or performance demands. This mismatch creates sustained demand for new and updated software architectures. This is the primary architectural consequence of change.",
        "C": "✗ Not the answer. Requiring new testing on existing systems is a maintenance and quality assurance concern triggered by updates. While true, it describes a testing response to change rather than the primary architectural consequence of business and technological evolution.",
        "D": "✗ Not the answer. Privacy and security breaches are risks introduced by new technologies (IoT, AI, cloud) and require security engineering responses. They are consequences of technology adoption, not the primary reason why new software architectures are demanded.",
    },
    75: {
        "A": "✓ CORRECT. During the test execution process group, test cases are run against the software and outcomes are recorded. The primary work product of this phase is Test Reports, which document test results, defect counts, pass/fail rates, and provide an overall quality assessment to stakeholders.",
        "B": "✗ Not the answer. Requirements are produced during the requirements engineering phase and serve as inputs to testing (they define what must be verified and validated). They are not outputs of the test execution process.",
        "C": "✗ Not the answer. Test Cases are created during the test design and planning phase, before execution begins. Test cases are inputs to the execution phase, not outputs of it.",
        "D": "✗ Not the answer. Code is a software development artifact produced during implementation. It is the artifact being tested, not a product produced by the testing process.",
    },
    76: {
        "A": "✓ CORRECT. This statement is FALSE and therefore the answer. An AI agent perceives its environment through SENSORS, not effectors. Effectors (also called actuators) are the mechanisms through which the agent ACTS on the environment. Mixing up sensors (perception) and effectors (action) reverses the fundamental agent model.",
        "B": "✗ Not the answer. Saying AI is a preprogrammed system is an oversimplification but could be debated. However, it is not definitively incorrect in the way that mixing up sensors and effectors is. The question asks for the inappropriate (clearly wrong) statement.",
        "C": "✗ Not the answer. AI is indeed a multidisciplinary field drawing from computer science, mathematics, psychology, linguistics, neuroscience, and engineering. This is a TRUE statement about AI.",
        "D": "✗ Not the answer. The ability to learn from the environment is a core characteristic of modern AI systems, particularly machine learning. This is a TRUE statement about AI's defining capabilities.",
    },
    77: {
        "A": "✗ Not the answer. A language interpreting other language programs describes how some languages implement interpreters for other languages (e.g., Python interpreting JavaScript). This is cross-language interpretation, not bootstrapping.",
        "B": "✓ CORRECT. Bootstrapping in compiler construction means the compiler for language X is written in language X itself and then compiled. This is how the first self-hosting compilers were built: write a subset compiler in another language, use it to compile the full compiler written in X, then use that to compile future versions.",
        "C": "✗ Not the answer. A language compiling other language programs describes cross-compilers or transpilers that translate code from one language to another. For example, TypeScript compiling to JavaScript. This is cross-compilation, not bootstrapping.",
        "D": "✗ Not the answer. All of the above would make bootstrapping mean all three scenarios simultaneously. Since only 'a language compiles itself' is the correct definition, 'all of the above' is incorrect.",
    },
    78: {
        "A": "✗ Not the answer. The architectural style to use (layered, microservices, event-driven, MVC, etc.) is a fundamental architectural decision. Choosing the wrong style for a system's requirements leads to serious long-term consequences.",
        "B": "✗ Not the answer. The type of application (web, mobile, desktop, real-time, batch processing) directly shapes architectural decisions about deployment, communication patterns, UI frameworks, and scalability strategies.",
        "C": "✓ CORRECT. The way data is stored (relational database, NoSQL, flat files) is a data management implementation detail that follows from architectural decisions rather than driving them. Architecture defines what components exist and how they interact; storage is an implementation choice within that architecture.",
        "D": "✗ Not the answer. Expected performance requirements (response time, throughput, scalability targets) are non-functional requirements that heavily influence architectural decisions such as caching strategies, load balancing, asynchronous processing, and component distribution.",
    },
    79: {
        "A": "✓ CORRECT. Overfitting occurs when a model learns the training data too precisely—including noise, outliers, and irrelevant patterns—resulting in excellent training accuracy but poor performance on unseen data. The model has memorized examples rather than learning generalizable patterns.",
        "B": "✗ Not the answer. The sweet spot refers to the ideal model complexity where training error and generalization error are both low. It is the balance point between underfitting (too simple) and overfitting (too complex), not the problematic scenario described.",
        "C": "✗ Not the answer. Under performing is a generic informal term, not a defined machine learning concept. The question asks for the specific technical term for a model that does well on training but poorly on new data.",
        "D": "✗ Not the answer. Underfitting is when a model is too simple to capture the underlying pattern in the data—it performs poorly on both training and test data. This is the opposite of the described scenario, where training performance is good but test performance is poor.",
    },
    80: {
        "A": "✗ Not the answer. Architectural optimization techniques focus on improving the performance, scalability, or resource use of an architecture. While useful, optimization alone does not make an architecture understandable to others; clear documentation and notation are required for that.",
        "B": "✓ CORRECT. Architectural notation (UML component diagrams, deployment diagrams, sequence diagrams) combined with semantic descriptions (narrative explanations of component roles, interaction protocols, and design rationale) enable other experts to understand, maintain, and evolve the architecture over time.",
        "C": "✗ Not the answer. Architectural refactoring improves the internal structure of an architecture without changing its behavior, addressing technical debt. While refactoring can simplify an architecture, it does not itself produce the documentation that makes it understandable to others.",
        "D": "✗ Not the answer. Architectural reverse engineering reconstructs an architectural description from existing code when documentation is missing. It is a remediation technique for undocumented systems, not the proactive approach to making architecture understandable from the start.",
    },
    81: {
        "A": "✓ CORRECT. Grouping is a free-space management technique where the first free block stores the addresses of n other free blocks (and the last of those points to the next group). This allows the OS to quickly retrieve a large batch of free block addresses in a single read, improving allocation efficiency.",
        "B": "✗ Not the answer. Counting is a free-space management method that stores the starting address of a contiguous run of free blocks along with a count of how many consecutive free blocks follow. It is efficient when disk is organized in large contiguous runs but differs from the group-address approach described.",
        "C": "✗ Not the answer. Linked-list (free list) is the basic approach where each free block contains a pointer to the next free block, forming a chain. This is the original method that grouping modifies to improve efficiency; accessing many free blocks via linked-list requires many disk reads.",
        "D": "✗ Not the answer. Deadlock is a concurrency problem where two or more processes are each waiting for a resource held by the other, causing all to be stuck. It is a process management concept unrelated to free-space management in file systems.",
    },
    82: {
        "A": "✗ Not the answer. Increasing the number of component communications (inter-process calls, network requests, API invocations) adds latency and coordination overhead. More communications mean more round-trip delays, which degrades performance rather than improving it.",
        "B": "✗ Not the answer. Increasing the number of components can introduce more communication paths and deployment overhead. While parallelism can improve throughput in some cases, blindly adding components adds coordination and deployment complexity that can hurt performance.",
        "C": "✓ CORRECT. Localizing critical operations means keeping computationally intensive, frequently called, or latency-sensitive logic within a single process or component to minimize inter-component communication. When critical operations are collocated, they avoid network latency and context-switching overhead.",
        "D": "✗ Not the answer. Distributing operations across a network introduces network latency, serialization overhead, and potential for partial failures. Unless distribution is specifically needed for scalability or redundancy, it degrades performance of critical operations.",
    },
    83: {
        "A": "✗ Not the answer. O(n^7) overestimates the complexity. While the nested loops are complex, careful analysis shows the total work grows as approximately n^5, not n^7. An O(n^7) claim would require an additional level of nesting not present in this code.",
        "B": "✗ Not the answer. O(n^2) greatly underestimates the complexity. A simple double nested loop would be O(n^2), but this code has three levels of nesting where the inner two loops each have ranges that grow with i, making the true complexity much higher.",
        "C": "✓ CORRECT. The outer loop is O(n). The middle loop runs i^2 times. Among those, j%i==0 holds for i values of j (j = i, 2i, ..., i*i). For each such j, the inner loop runs j times (up to i^2). Summing: for each i the work is approximately i * i^2 = i^3, and summing i^3 from 1 to n gives O(n^4)—but upper-bounding each factor at n gives n * n^2 * n^2 = O(n^5), the conservative but correct exam answer.",
        "D": "✗ Not the answer. O(n log n) is typical of efficient sorting algorithms like merge sort or heap sort, or algorithms that divide the problem in half at each step. The triple-nested structure here with quadratic inner loops is far more expensive than O(n log n).",
    },
    84: {
        "A": "✗ Not the answer. Parallel transaction describes multiple transactions executing at the same time, which is handled by the DBMS concurrency control mechanism. It describes simultaneous access, not the ability to present different perspectives of data to different user groups.",
        "B": "✗ Not the answer. Multiple users refers to the database's ability to serve many simultaneous users. While related, it describes concurrent access management rather than the feature that each user group sees a tailored view of the data relevant to their needs.",
        "C": "✓ CORRECT. The multiple views feature allows different user groups to see customized subsets or transformations of the database. A sales team sees customer and order data; an HR team sees employee records. SQL VIEWs implement this by defining virtual tables tailored to each group's needs.",
        "D": "✗ Not the answer. Concurrent transaction refers to transactions that execute overlapping in time, requiring isolation mechanisms (locks, MVCC) to prevent interference. Like parallel transactions, this concerns simultaneous access management, not customized data visibility.",
    },
    85: {
        "A": "✗ Not the answer. Realism check (or feasibility check) verifies that requirements can actually be achieved given the available technology, time, and budget. It asks 'can this be built?' rather than 'can this be checked during delivery?'",
        "B": "✓ CORRECT. Verifiability is the requirement validation check that asks: can each requirement be objectively tested or verified? Documenting requirements precisely and then checking at delivery whether each one was implemented is exactly the verifiability process—it creates a testable contract between customer and contractor.",
        "C": "✗ Not the answer. Completeness check ensures that the requirements specification covers all necessary functionality and does not omit important scenarios. It asks 'is anything missing?' rather than 'can we verify each requirement was delivered?'",
        "D": "✗ Not the answer. Validity check ensures that requirements reflect what stakeholders actually need (not what was assumed they needed). It confirms requirements are genuinely required, not that they can be verified against a delivered product.",
    },
    86: {
        "A": "✓ CORRECT. Local Search Algorithms explore the solution space by moving iteratively from the current solution to a neighboring one. Because they only look locally, the final solution quality is strongly influenced by the starting point (different starts may reach different local optima) and the neighborhood function (what 'nearby' means).",
        "B": "✗ Not the answer. LSAs are typically used for non-convex, combinatorial, or NP-hard optimization problems where exact methods are too slow. Convex problems are better solved with gradient-based methods that guarantee global optima; LSAs are precisely for cases where convexity cannot be assumed.",
        "C": "✗ Not the answer. The time complexity of LSAs does depend on the problem size—larger problems have more states to explore and the algorithms typically run longer. The number of iterations or evaluations needed scales with the size and complexity of the search space.",
        "D": "✗ Not the answer. LSAs do NOT guarantee finding the globally optimal solution. They can get stuck in local optima—solutions that are better than all their neighbors but worse than the global best. Techniques like simulated annealing and tabu search try to escape local optima but still provide no absolute guarantee.",
    },
    87: {
        "A": "✗ Not the answer. Improving product acceptance is a legitimate purpose of testing. When comprehensive testing reveals and removes defects before release, customers and stakeholders gain confidence in the product, increasing its acceptance and reducing post-release complaints.",
        "B": "✗ Not the answer. Enhancing reliability through defect identification and removal is a core purpose of testing. Each defect found and fixed before deployment improves the software's probability of failure-free operation.",
        "C": "✗ Not the answer. Identifying shortcomings in the software is the fundamental purpose of testing. Testing is the process of exercising the software to find defects, gaps between specified and actual behavior, and areas that need improvement.",
        "D": "✓ CORRECT. Requesting more design and implementation time is not a purpose of software testing. Testing is conducted to find and fix defects in order to deliver quality software on schedule, not to justify extending the development timeline. Using test results to argue for more time would be a misuse of the testing process.",
    },
    88: {
        "A": "✗ Not the answer. ACLs ARE always processed sequentially from the first entry to the last (in order of entry number). Packets are compared against each rule in sequence until a match is found. This statement is TRUE about ACL processing.",
        "B": "✓ CORRECT. This statement is FALSE: the comparison does NOT continue until all lines are analyzed. ACL processing uses first-match semantics—as soon as a packet matches a rule, the corresponding action (permit or deny) is applied immediately and no further lines are checked.",
        "C": "✗ Not the answer. Every ACL does have an implicit deny-all statement at the end. If a packet matches no explicit rule, it is denied by this implicit rule. This is a TRUE and important property of ACLs that many security engineers rely on.",
        "D": "✗ Not the answer. Once a packet matches a rule, the action is applied and processing stops immediately. This is the correct description of ACL first-match behavior. This statement is TRUE and is precisely why statement B is false.",
    },
    89: {
        "A": "✗ Not the answer. WannaCry is a well-known ransomware cyberattack that encrypted victims' files and demanded ransom payment in Bitcoin. It is a type of malware, not a term for unsolicited commercial email.",
        "B": "✓ CORRECT. Spam is unsolicited bulk commercial email sent to recipients who did not request it. It ranges from harmless advertising to dangerous phishing and malware-delivery campaigns. Anti-spam filters, blacklists, and legal regulations (like CAN-SPAM) exist to combat it.",
        "C": "✗ Not the answer. Trash is the informal term for the recycle bin or deleted items folder in an email client. It describes where deleted messages are stored, not a specific category of unwanted unsolicited commercial email.",
        "D": "✗ Not the answer. Adware is software installed on a device that automatically displays unwanted advertisements, often bundled with free software. While both spam and adware are unwanted advertising, adware is a software category, not a type of email.",
    },
    90: {
        "A": "✗ Not the answer. Servers run operating systems like Linux, Windows Server, or Unix that are optimized for high availability, multi-user access, and heavy workloads. Android's architecture—designed for touchscreens, limited battery, and mobile sensors—is poorly suited to server environments.",
        "B": "✓ CORRECT. Android was designed from the ground up for mobile devices, specifically touchscreen smartphones and tablets. Its architecture addresses mobile-specific constraints: battery efficiency, varying screen sizes, touch input, mobile sensors (GPS, accelerometer), and cellular connectivity.",
        "C": "✗ Not the answer. Traditional laptops use macOS, Windows, or Linux distributions designed for keyboard-and-trackpad interaction, larger screens, and sustained power. While Android has been used experimentally on laptops (Chromebooks with Android apps), laptops are not Android's primary target.",
        "D": "✗ Not the answer. Desktops use traditional operating systems like Windows, macOS, or Linux. Android is not designed for desktop environments with mouse and keyboard primary input, large monitors, and always-on power.",
    },
    91: {
        "A": "✗ Not the answer. Data transformation is a standard preprocessing step that converts data into a form suitable for modeling: normalizing numerical features to [0,1], standardizing to zero mean, encoding categorical variables, or applying log transforms. It is a core preprocessing activity.",
        "B": "✗ Not the answer. Data cleaning addresses missing values, duplicate records, inconsistent formats, and outliers. It is the first and most critical preprocessing step, making raw data usable by removing errors and inconsistencies.",
        "C": "✓ CORRECT. Data optimization is not a recognized step in the ML data preprocessing pipeline. The standard steps are cleaning, transformation, integration, and reduction. Optimization is a term from databases (query optimization) or algorithms (parameter tuning) and does not describe a preprocessing activity.",
        "D": "✗ Not the answer. Data reduction decreases the volume of data while preserving important information. Techniques include dimensionality reduction (PCA, feature selection) and instance selection (sampling). Reducing data size speeds up training and can improve model generalization.",
    },
    92: {
        "A": "✗ Not the answer. FileOutputStream is the class for WRITING bytes to a file, not reading. The Output in its name indicates the direction of data flow: from the program to the file. Using it to read would require a different class.",
        "B": "✗ Not the answer. PipedInputStream is a stream class for reading bytes that are being written by a connected PipedOutputStream, enabling communication between threads. It is designed for inter-thread data transfer, not for reading from disk files.",
        "C": "✓ CORRECT. FileInputStream is the standard Java class for reading raw bytes from a file. You create it with a filename or File object, and then read bytes using its read() method. For reading text files efficiently, it can be wrapped in an InputStreamReader and BufferedReader.",
        "D": "✗ Not the answer. RandomAccessFile supports both reading and writing to a file and allows seeking to any position using seek(). While it can read files, it is not classified as an InputStream and is used when you need random (non-sequential) access to file contents.",
    },
    93: {
        "A": "✗ Not the answer. Point-to-Point (PPP) Encapsulation is a data link framing protocol that wraps network layer packets for transmission over point-to-point links. It is a specific Data Link protocol, not the name of the sub-layer responsible for identifying and encapsulating higher-layer protocols.",
        "B": "✗ Not the answer. MAC (Media Access Control) is the lower sub-layer of the Data Link Layer. It handles physical addressing (MAC addresses), media access methods (CSMA/CD, CSMA/CA), and frame delimiting. It does not identify Network Layer protocols.",
        "C": "✗ Not the answer. Frame Relay is a Layer 2 WAN protocol that carries frames between switches. It is a specific technology, not a sub-layer name or function responsible for identifying Network Layer protocol types.",
        "D": "✓ CORRECT. LLC (Logical Link Control) is the upper sub-layer of the Data Link Layer (IEEE 802.2). Its primary role is to identify which Network Layer protocol (IPv4, IPv6, IPX) is carried in the frame and to encapsulate that protocol's data with appropriate LLC headers so the receiving station knows how to process the payload.",
    },
    94: {
        "A": "✗ Not the answer. Writing 'public class Invoice extends Payable' uses the wrong keyword. In Java, classes implement interfaces using the implements keyword, not extends. The extends keyword is used to inherit from another class. This code would not compile.",
        "B": "✗ Not the answer. Missing the return type double on getPaymentAmount() would cause a compilation error. The interface declares double getPaymentAmount(), so the implementing class must match the return type exactly. Omitting the return type is a syntax error.",
        "C": "✓ CORRECT. The correct implementation uses implements (not extends) for the interface, provides a public method with the exact signature double getPaymentAmount(), and returns the correct calculation: getQuantity() * getPricePerItem(). This satisfies the Payable contract and compiles without error.",
        "D": "✗ Not the answer. Using an abstract class when a concrete implementation is available is unnecessary and complicates the design. If Invoice provides a full implementation of getPaymentAmount(), there is no reason to declare Invoice abstract. Abstract classes are appropriate only when some methods are left unimplemented.",
    },
    95: {
        "A": "✓ CORRECT. To join HOTEL and ROOM and retrieve hotel names with room IDs, the correct condition is ROOM.Hotel_id = HOTEL.Hotel_id—this matches each room to its hotel via the foreign key. The SELECT clause retrieves Hotel_Name from HOTEL and Room_Id from ROOM.",
        "B": "✗ Not the answer. WHERE ROOM.Room_id = HOTEL.Hotel_id joins the room's primary key to the hotel's primary key. These are unrelated identifiers—a room ID of 5 has no meaningful relationship to a hotel whose ID happens to be 5. This produces a Cartesian product cross-join on coincidentally equal IDs.",
        "C": "✗ Not the answer. Adding AND ROOM.Hotel_id = HOTEL.Hotel_id to an already incorrect join condition from option B does not fix the query; it adds a redundant (and still incorrect) condition alongside the wrong one. The corrected query needs only ROOM.Hotel_id = HOTEL.Hotel_id.",
        "D": "✗ Not the answer. Omitting a WHERE clause entirely produces a Cartesian product: every hotel row is paired with every room row regardless of relationship. A database with 100 hotels and 600 rooms would return 60,000 rows, almost all of which pair the wrong hotel with the wrong room.",
    },
    96: {
        "A": "✗ Not the answer. Requirements elicitation is the process of gathering requirements from stakeholders through interviews, workshops, observations, and document analysis. It is a core requirements engineering activity.",
        "B": "✗ Not the answer. Requirements validation checks that the requirements specification is correct, complete, consistent, and verifiable before development begins. It is an essential requirements engineering activity.",
        "C": "✗ Not the answer. Requirements analysis refines raw requirements by resolving conflicts, prioritizing, modeling scenarios, and checking feasibility. It is central to requirements engineering.",
        "D": "✓ CORRECT. Requirements status tracking monitors which requirements have been implemented, tested, or are still pending throughout the development lifecycle. This is a project monitoring and control activity belonging to project management, not one of the core requirements engineering activities (elicitation, analysis, specification, validation).",
    },
    97: {
        "A": "✗ Not the answer. const declares a block-scoped constant in JavaScript: once assigned, its binding cannot be reassigned. While const does declare an identifier, it creates a constant, not a general variable. The question asks for the keyword that 'defines a variable' implying mutability.",
        "B": "✗ Not the answer. int is a primitive type keyword in Java, C, and C++ used to declare integer variables. JavaScript is dynamically typed and does not use int for variable declaration; attempting to use int in JavaScript would result in an error or be treated as an identifier name.",
        "C": "✗ Not the answer. val is a keyword in Kotlin (and Scala) used to declare an immutable (read-only) variable. JavaScript does not have a val keyword; it is not part of the JavaScript specification.",
        "D": "✓ CORRECT. let is the modern JavaScript keyword for declaring a block-scoped variable that can be reassigned. Introduced in ES6 (2015), let replaced var for most use cases because it has predictable block scope rather than function scope, avoiding common bugs from hoisting and scope leakage.",
    },
    98: {
        "A": "✗ Not the answer. Conflicting requirements arise when different stakeholders have contradictory needs (e.g., the marketing team wants feature X while the security team says X is unsafe). Resolving conflicts is a real and common challenge during requirements elicitation and analysis.",
        "B": "✓ CORRECT. Obsolete requirements are requirements that were once valid but are no longer relevant due to changes in business context, technology, or regulations. Managing obsolescence is a maintenance concern for existing requirements documentation, not a challenge encountered while initially eliciting new requirements from stakeholders.",
        "C": "✗ Not the answer. Requirement change is a pervasive challenge: stakeholders change their minds, business conditions shift, and new laws emerge. Managing changing requirements throughout the project lifecycle is one of the most difficult aspects of requirements engineering.",
        "D": "✗ Not the answer. Negative stakeholders are individuals or groups who oppose the project and may provide misleading, incomplete, or obstructive input during elicitation. Identifying and managing them is a recognized challenge in stakeholder management and requirements elicitation.",
    },
    99: {
        "A": "✗ Not the answer. A compiling error (compilation error) is caught by the compiler before the program ever runs: syntax mistakes, type mismatches, or undeclared variables cause the compiler to reject the code. The scenario states there was no error, eliminating compilation errors.",
        "B": "✗ Not the answer. A syntax error is a type of compilation error—the code does not conform to the language grammar. Like compilation errors, syntax errors are detected before execution. The program running successfully rules out syntax errors.",
        "C": "✓ CORRECT. A logical error occurs when the program compiles and executes without any crash or exception but produces an incorrect result because the algorithm or formula is wrong. For example, computing average with sum/count-1 instead of sum/count runs fine but gives wrong numbers. Only careful testing and code review reveal logical errors.",
        "D": "✗ Not the answer. A runtime error (runtime exception) occurs during program execution and typically crashes the program or throws an exception (e.g., NullPointerException, ArrayIndexOutOfBoundsException, division by zero). The scenario states the program ran without any visible error, ruling out runtime exceptions.",
    },
    100: {
        "A": "✓ CORRECT. Professional ethics require engineers to work only within their competence. Accepting work you are not qualified to do risks producing low-quality, defective, or unsafe software. The ACM and IEEE codes of software engineering ethics explicitly require practitioners to be honest about their competence and to decline work that exceeds it.",
        "B": "✗ Not the answer. Remaining up-to-date in your profession is an ethical obligation, not a violation. Technology evolves rapidly, and engineers who do not keep current may inadvertently produce outdated or insecure solutions. Continuous learning is a professional responsibility.",
        "C": "✗ Not the answer. Respecting the confidentiality of employers and clients is a core ethical duty. Software engineers often access sensitive business information, proprietary algorithms, and personal data; disclosing these without authorization would be a serious ethical and often legal violation.",
        "D": "✗ Not the answer. Using technical skills responsibly—not causing harm, protecting privacy, and considering societal impacts—is fundamental to professional engineering ethics. Responsible use of skills is what ethics requires, not what it prohibits.",
    },
}
