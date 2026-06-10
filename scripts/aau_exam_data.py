"""Answer key, manual OCR fixes, and teaching notes for AAU Model Exit Exam (by page/examNumber 1-100)."""

# Keyed by examNumber (= PDF page index for pages 1-100)
ANSWERS: dict[int, str] = {
    1: "D",
    2: "C",
    3: "C",
    4: "B",
    5: "C",
    6: "B",
    7: "D",
    8: "A",
    9: "A",
    10: "D",
    11: "A",
    12: "D",
    13: "D",
    14: "B",
    15: "A",
    16: "C",
    17: "C",
    18: "C",
    19: "A",
    20: "C",
    21: "B",
    22: "A",
    23: "B",
    24: "C",
    25: "C",
    26: "B",
    27: "A",
    28: "A",
    29: "B",
    30: "B",
    31: "D",
    32: "A",
    33: "B",
    34: "A",
    35: "B",
    36: "A",
    37: "B",
    38: "C",
    39: "D",
    40: "D",
    41: "B",
    42: "C",
    43: "D",
    44: "D",
    45: "B",
    46: "D",
    47: "D",
    48: "D",
    49: "C",
    50: "B",
    51: "C",
    52: "B",
    53: "B",
    54: "D",
    55: "B",
    56: "C",
    57: "A",
    58: "D",
    59: "D",
    60: "B",
    61: "D",
    62: "C",
    63: "D",
    64: "D",
    65: "D",
    66: "A",
    67: "D",
    68: "C",
    69: "B",
    70: "A",
    71: "C",
    72: "C",
    73: "A",
    74: "B",
    75: "D",
    76: "B",
    77: "D",
    78: "A",
    79: "C",
    80: "D",
    81: "D",
    82: "C",
    83: "C",
    84: "D",
    85: "B",
    86: "A",
    87: "B",
    88: "C",
    89: "A",
    90: "A",
    91: "C",
    92: "C",
    93: "B",
    94: "B",
    95: "A",
    96: "D",
    97: "B",
    98: "A",
    99: "B",
    100: "A",
}

# examNumber -> {text?, options?, topic?, concept?}
MANUAL_OVERRIDES: dict[int, dict] = {
    1: {
        "text": "Consider a relation schema R with attributes α ⊆ R and β ⊆ R. The functional dependency α → β holds on R if, in every legal relation r(R), for all pairs of tuples t1 and t2 in r such that t1[α] = t2[α], we also have t1[β] = t2[β]. This concept is called:",
        "options": [
            {"key": "A", "text": "Normalization"},
            {"key": "B", "text": "Decomposition"},
            {"key": "C", "text": "Set Theory"},
            {"key": "D", "text": "Functional Dependency"},
        ],
    },
    2: {
        "text": "Which one of the principles of cyber security refers to the security mechanism being as small and simple as possible?",
        "options": [
            {"key": "A", "text": "Fail-safe Defaults"},
            {"key": "B", "text": "Least privilege"},
            {"key": "C", "text": "Economy of Mechanism"},
            {"key": "D", "text": "Open Design"},
        ],
    },
    3: {
        "text": "Which of the following alternatives is most suitable for supporting a qualitative analysis of your software architecture?",
        "options": [
            {"key": "A", "text": "Team size"},
            {"key": "B", "text": "Organizational structures"},
            {"key": "C", "text": "Quality scenarios"},
            {"key": "D", "text": "Log files"},
        ],
    },
    4: {
        "text": "What is the maximum number of swaps that can be performed in the Selection Sort algorithm on n elements?",
        "options": [
            {"key": "A", "text": "n - 2"},
            {"key": "B", "text": "n - 1"},
            {"key": "C", "text": "n"},
            {"key": "D", "text": "n / 2"},
        ],
    },
    5: {
        "text": "Which of the following statements is NOT correct?",
        "options": [
            {"key": "A", "text": "C++ is an object-oriented programming language"},
            {"key": "B", "text": "Java is an object-oriented programming language"},
            {"key": "C", "text": "The object-oriented approach does not separate the behavior of a system from the data"},
            {"key": "D", "text": "Java is the only object-oriented programming language"},
        ],
    },
    6: {
        "text": "Why is it important to maintain a good relationship between software testers and developers?",
        "options": [
            {"key": "A", "text": "To ensure that the project is completed on time"},
            {"key": "B", "text": "To foster collaboration and communication between the two teams"},
            {"key": "C", "text": "To make sure that the software is defect-free"},
            {"key": "D", "text": "To reduce the cost of the project"},
        ],
    },
    7: {
        "text": "Which OSI layer is responsible for wireless signal encoding and frequency band definition?",
        "options": [
            {"key": "A", "text": "Application Layer"},
            {"key": "B", "text": "Logical Link Control Layer"},
            {"key": "C", "text": "Medium Access Layer"},
            {"key": "D", "text": "Physical Layer"},
        ],
        "answer": "D",
    },
    8: {
        "text": "Which of the following qualities can most likely be improved by using a layered architecture?",
        "options": [
            {"key": "A", "text": "Flexibility in modifying or changing the system"},
            {"key": "B", "text": "Runtime efficiency (performance)"},
            {"key": "C", "text": "Flexibility at runtime (configurability)"},
            {"key": "D", "text": "Non-repudiability"},
        ],
    },
    9: {
        "text": "The software requirements specification (SRS) is said to be consistent if and only if no subset of individual requirements described in it conflict with each other. This property is called:",
        "options": [
            {"key": "A", "text": "Consistent"},
            {"key": "B", "text": "Verifiable"},
            {"key": "C", "text": "Unambiguous"},
            {"key": "D", "text": "Correct"},
        ],
    },
    10: {
        "text": "Why is software architecture so important?",
        "options": [
            {"key": "A", "text": "Communication among stakeholders"},
            {"key": "B", "text": "Early design decisions"},
            {"key": "C", "text": "Transferable abstraction of a system"},
            {"key": "D", "text": "All of the above"},
        ],
    },
    12: {
        "text": "You try to analyze your architecture quantitatively. Which is the most appropriate indicator for architectural problem areas?",
        "options": [
            {"key": "A", "text": "Missing comments"},
            {"key": "B", "text": "Names of public methods do not reflect their purpose"},
            {"key": "C", "text": "Number of test cases per component"},
            {"key": "D", "text": "High coupling of components"},
        ],
    },
    13: {
        "text": "Polymorphism means:",
        "options": [
            {"key": "A", "text": "Declaring all the methods of a class as public"},
            {"key": "B", "text": "Declaring all the attributes of a class as private"},
            {"key": "C", "text": "Hiding information so it is not accessible to other classes"},
            {"key": "D", "text": "Having methods or operators with the same name performing different functions"},
        ],
    },
    14: {
        "text": "What is the use of a content provider in Android?",
        "options": [
            {"key": "A", "text": "For entering data in the database"},
            {"key": "B", "text": "For sharing data between applications"},
            {"key": "C", "text": "For passing data from one Activity to another"},
            {"key": "D", "text": "None of the above"},
        ],
    },
    15: {
        "text": "For a binary relationship set R between entity sets A and B, the ______ expresses the number of entities to which another entity can be associated.",
        "options": [
            {"key": "A", "text": "Cardinality ratio"},
            {"key": "B", "text": "Limited ratio"},
            {"key": "C", "text": "Degree ratio"},
            {"key": "D", "text": "Participation constraints"},
        ],
    },
    16: {
        "text": "Which pair of algorithms has equal cost in terms of time and space complexity under an equal step-cost function?",
        "options": [
            {"key": "A", "text": "BFS and DFS"},
            {"key": "B", "text": "DFS and UCS"},
            {"key": "C", "text": "UCS and BFS"},
            {"key": "D", "text": "DFS and BFS"},
        ],
    },
    18: {
        "text": "Which of the following is the main goal of software testing as part of the quality assurance process?",
        "options": [
            {"key": "A", "text": "To monitor the software development lifecycle"},
            {"key": "B", "text": "To control the cost of software development"},
            {"key": "C", "text": "To ensure that the software meets the specified requirements"},
            {"key": "D", "text": "To manage project timelines and deadlines"},
        ],
    },
    19: {
        "text": "An algorithm that calls itself directly or indirectly is known as:",
        "options": [
            {"key": "A", "text": "Recursion"},
            {"key": "B", "text": "Sub algorithm"},
            {"key": "C", "text": "Traversal algorithm"},
            {"key": "D", "text": "Polish notation"},
        ],
    },
    20: {
        "text": "What is supervised learning in AI?",
        "options": [
            {"key": "A", "text": "Reinforcement learning with a reward-based system"},
            {"key": "B", "text": "Learning by observing human behavior"},
            {"key": "C", "text": "Training a machine learning model with labeled data"},
            {"key": "D", "text": "Training a machine learning model with unlabeled data"},
        ],
    },
    21: {
        "text": "Which one of the following is NOT a function of the operating system?",
        "options": [
            {"key": "A", "text": "Runs software utilities and programs"},
            {"key": "B", "text": "Translates high-level programming language into machine code"},
            {"key": "C", "text": "Manages computer system resources"},
            {"key": "D", "text": "Makes the computer system convenient to use"},
        ],
    },
    22: {
        "text": "The ______ must be looked up in order to deliver a message to the appropriate application software running on a host.",
        "options": [
            {"key": "A", "text": "Port number"},
            {"key": "B", "text": "CRC"},
            {"key": "C", "text": "MAC address"},
            {"key": "D", "text": "IP address only"},
        ],
    },
    23: {
        "text": "What is inter-process communication (IPC)?",
        "options": [
            {"key": "A", "text": "Allows processes to communicate when using the same address space only"},
            {"key": "B", "text": "Allows processes to communicate and synchronize without sharing the same address space"},
            {"key": "C", "text": "Allows processes to synchronize without communication"},
            {"key": "D", "text": "None of the above"},
        ],
    },
    24: {
        "text": "What will be the output of the following JavaScript code? function rev(a){ let arr=[]; for(let i=a.length-1;i>=0;i--) arr.unshift(a[i]); return arr; } rev([22,111,44]);",
        "options": [
            {"key": "A", "text": "[1122, 111, 44]"},
            {"key": "B", "text": "[44, 111, 22]"},
            {"key": "C", "text": "[22, 111, 44]"},
            {"key": "D", "text": "[111]"},
        ],
        "answer": "C",
    },
    26: {
        "text": "The purpose of a foreign key is to identify a particular row in the:",
        "options": [
            {"key": "A", "text": "Parent and child tables simultaneously"},
            {"key": "B", "text": "Referenced (parent) table"},
            {"key": "C", "text": "Child table only"},
            {"key": "D", "text": "All of the above"},
        ],
    },
    27: {
        "text": "When a thread is running, it can return directly to the READY state by which of the following means?",
        "options": [
            {"key": "A", "text": "Encountering a yield() call"},
            {"key": "B", "text": "Encountering a sleep() call"},
            {"key": "C", "text": "Encountering a wait() on a lock"},
            {"key": "D", "text": "Becoming blocked waiting for I/O"},
        ],
    },
    29: {
        "text": "Accepting risk occurrence but not doing anything about it is called:",
        "options": [
            {"key": "A", "text": "Risk avoidance"},
            {"key": "B", "text": "Risk retention"},
            {"key": "C", "text": "Risk reduction"},
            {"key": "D", "text": "Risk transfer"},
        ],
    },
    32: {
        "text": "Which of the following is NOT a state in the Android service lifecycle?",
        "options": [
            {"key": "A", "text": "Destroyed"},
            {"key": "B", "text": "Running"},
            {"key": "C", "text": "Start"},
            {"key": "D", "text": "Paused"},
        ],
    },
    33: {
        "text": "An attribute takes a ______ value when an entity does not have a value for it.",
        "options": [
            {"key": "A", "text": "Not Applicable"},
            {"key": "B", "text": "Null"},
            {"key": "C", "text": "Default"},
            {"key": "D", "text": "Zero"},
        ],
    },
    34: {
        "text": "Which sorting algorithm provides the best worst-case time complexity?",
        "options": [
            {"key": "A", "text": "Merge sort"},
            {"key": "B", "text": "Selection sort"},
            {"key": "C", "text": "Quick sort"},
            {"key": "D", "text": "Bubble sort"},
        ],
    },
    35: {
        "text": "Modifying software to match changes in the ever-changing environment is known as:",
        "options": [
            {"key": "A", "text": "Perfective maintenance"},
            {"key": "B", "text": "Adaptive maintenance"},
            {"key": "C", "text": "Preventive maintenance"},
            {"key": "D", "text": "Corrective maintenance"},
        ],
    },
    36: {
        "text": "In TCP, reliable transport verifies safe arrival of data using:",
        "options": [
            {"key": "A", "text": "Acknowledgment"},
            {"key": "B", "text": "Bits"},
            {"key": "C", "text": "Buffer"},
            {"key": "D", "text": "Frame"},
        ],
    },
    37: {
        "text": "During which activity in the fundamental test process are tests designed and executed?",
        "options": [
            {"key": "A", "text": "Test analysis and design"},
            {"key": "B", "text": "Test implementation and execution"},
            {"key": "C", "text": "Test planning and control"},
            {"key": "D", "text": "Test closure"},
        ],
    },
    38: {
        "text": "Which data structure allows deleting elements from the front and inserting at the rear?",
        "options": [
            {"key": "A", "text": "Deque"},
            {"key": "B", "text": "Binary search tree"},
            {"key": "C", "text": "Queue"},
            {"key": "D", "text": "Stack"},
        ],
    },
    40: {
        "text": "Which is a type of independent malicious program that never requires a host program?",
        "options": [
            {"key": "A", "text": "Trap door"},
            {"key": "B", "text": "Trojan horse"},
            {"key": "C", "text": "Virus"},
            {"key": "D", "text": "Worm"},
        ],
    },
    41: {
        "text": "Which OSI layer functions as the basis for dialog control and synchronization?",
        "options": [
            {"key": "A", "text": "Network layer"},
            {"key": "B", "text": "Session layer"},
            {"key": "C", "text": "Data link layer"},
            {"key": "D", "text": "Transport layer"},
        ],
    },
    42: {
        "text": "What is the term for a collection of large, complex data sets that cannot be processed using traditional data processing tools?",
        "options": [
            {"key": "A", "text": "Wisdom"},
            {"key": "B", "text": "Tiny data"},
            {"key": "C", "text": "Big data"},
            {"key": "D", "text": "Information"},
        ],
    },
    43: {
        "text": "The lowest level of work on a project schedule is called a:",
        "options": [
            {"key": "A", "text": "Work product"},
            {"key": "B", "text": "Milestone"},
            {"key": "C", "text": "Task set"},
            {"key": "D", "text": "Task"},
        ],
    },
    45: {
        "text": "Which network topology design makes it most difficult to identify faults?",
        "options": [
            {"key": "A", "text": "Star"},
            {"key": "B", "text": "Bus"},
            {"key": "C", "text": "Mesh"},
            {"key": "D", "text": "Ring"},
        ],
    },
    47: {
        "text": "What does the HTTP status code 201 indicate?",
        "options": [
            {"key": "A", "text": "No content"},
            {"key": "B", "text": "Accepted"},
            {"key": "C", "text": "OK"},
            {"key": "D", "text": "Created"},
        ],
    },
    48: {
        "text": "Which are famous common cyber-attacks used to infiltrate user systems?",
        "options": [
            {"key": "A", "text": "DDoS and drive-by downloads"},
            {"key": "B", "text": "Malware and malvertising"},
            {"key": "C", "text": "Phishing and password attacks"},
            {"key": "D", "text": "All of the above"},
        ],
    },
    49: {
        "text": "Identify a possible source of unstructured data:",
        "options": [
            {"key": "A", "text": "RDBMS tables"},
            {"key": "B", "text": "University student registration database"},
            {"key": "C", "text": "Twitter feeds"},
            {"key": "D", "text": "Employee payroll table"},
        ],
    },
    50: {
        "text": "What type of CSS is generally recommended for designing large web pages?",
        "options": [
            {"key": "A", "text": "Embedded"},
            {"key": "B", "text": "External"},
            {"key": "C", "text": "Inline"},
            {"key": "D", "text": "Internal only"},
        ],
    },
    51: {
        "text": "What is the time complexity of: void solve(){ string s=\"scalar\"; int n=s.size(); for(int i=0;i<n;i++) cout<<s[i]; }",
        "options": [
            {"key": "A", "text": "O(log n)"},
            {"key": "B", "text": "O(1)"},
            {"key": "C", "text": "O(n)"},
            {"key": "D", "text": "O(n²)"},
        ],
    },
    54: {
        "text": "What is the time complexity of the binary search algorithm?",
        "options": [
            {"key": "A", "text": "O(1)"},
            {"key": "B", "text": "O(n)"},
            {"key": "C", "text": "O(n log n)"},
            {"key": "D", "text": "O(log n)"},
        ],
    },
    55: {
        "text": "Which of the following is NOT an Activity lifecycle callback method in Android?",
        "options": [
            {"key": "A", "text": "onStart()"},
            {"key": "B", "text": "onClick()"},
            {"key": "C", "text": "onCreate()"},
            {"key": "D", "text": "onBackPressed()"},
        ],
    },
    56: {
        "text": "What must be enabled for a RESTful web service to receive invocations from different domains, subdomains, or ports?",
        "options": [
            {"key": "A", "text": "Cache-Control headers only"},
            {"key": "B", "text": "HTTP/2"},
            {"key": "C", "text": "CORS"},
            {"key": "D", "text": "SSL alone"},
        ],
    },
    58: {
        "text": "What will be the output of the following C++ code? void solve() { int a[]={1,2,3,4,5}; int sum=0; for(int i=0;i<5;i++) if(i%2==0) sum+=a[i]; cout<<sum; }",
        "options": [
            {"key": "A", "text": "6"},
            {"key": "B", "text": "9"},
            {"key": "C", "text": "12"},
            {"key": "D", "text": "15"},
        ],
    },
    66: {
        "text": "What is Android?",
        "options": [
            {"key": "A", "text": "An operating system"},
            {"key": "B", "text": "A web server"},
            {"key": "C", "text": "A database engine"},
            {"key": "D", "text": "None of the above"},
        ],
    },
    79: {
        "text": "What will be the output of the following C++ code? void solve() { int a[]={2,4,6,8}; int sum=0; for(int i=0;i<4;i++) if(i%2==1) sum+=a[i]; else sum-=a[i]; cout<<sum; }",
        "options": [
            {"key": "A", "text": "10"},
            {"key": "B", "text": "20"},
            {"key": "C", "text": "15"},
            {"key": "D", "text": "34"},
        ],
    },
    57: {
        "text": "Java's garbage collector carries out which of the following functions?",
        "options": [
            {"key": "A", "text": "Frees memory locations that are no longer in use"},
            {"key": "B", "text": "Disposes applets when a web page closes"},
            {"key": "C", "text": "Closes GUI frames"},
            {"key": "D", "text": "Terminates threads"},
        ],
    },
    59: {
        "text": "Which statement is true of a class that has package (default) scope in Java?",
        "options": [
            {"key": "A", "text": "It may contain only abstract methods"},
            {"key": "B", "text": "It is a source file, not a class file"},
            {"key": "C", "text": "Only package-scope classes can be imported"},
            {"key": "D", "text": "It is visible only to other classes within the same package"},
        ],
    },
    60: {
        "text": "In an operating system, which mechanism is used to create a process?",
        "options": [
            {"key": "A", "text": "Deadlock detection and recovery"},
            {"key": "B", "text": "Execution of a process-creation system call by a running process"},
            {"key": "C", "text": "User request alone without OS support"},
            {"key": "D", "text": "System initialization only"},
        ],
    },
    61: {
        "text": "In Linux, a process creates a child process using which system call?",
        "options": [
            {"key": "A", "text": "yield()"},
            {"key": "B", "text": "exec()"},
            {"key": "C", "text": "init()"},
            {"key": "D", "text": "fork()"},
        ],
    },
    62: {
        "text": "For a binary relationship with mapping cardinality ONE-TO-ONE between entity sets A and B:",
        "options": [
            {"key": "A", "text": "An entity in A may map to many in B and vice versa"},
            {"key": "B", "text": "An entity in A may map to many in B; an entity in B maps to at most one in A"},
            {"key": "C", "text": "An entity in A maps to at most one in B and an entity in B maps to at most one in A"},
            {"key": "D", "text": "An entity in A maps to at most one in B; an entity in B may map to many in A"},
        ],
    },
    65: {
        "text": "What keyword is used to declare an asynchronous function in JavaScript?",
        "options": [
            {"key": "A", "text": "future"},
            {"key": "B", "text": "sync"},
            {"key": "C", "text": "await"},
            {"key": "D", "text": "async"},
        ],
    },
    67: {
        "text": "Which sorting algorithm is a divide-and-conquer type?",
        "options": [
            {"key": "A", "text": "Bubble sort"},
            {"key": "B", "text": "Insertion sort"},
            {"key": "C", "text": "Selection sort"},
            {"key": "D", "text": "Quick sort"},
        ],
    },
    68: {
        "text": "What is the main disadvantage of uninformed search algorithms?",
        "options": [
            {"key": "A", "text": "They are not optimal"},
            {"key": "B", "text": "They are not consistent"},
            {"key": "C", "text": "They are not complete"},
            {"key": "D", "text": "They are not admissible"},
        ],
    },
    69: {
        "text": "Which SQL statement gives every employee a 10% raise?",
        "options": [
            {"key": "A", "text": "CHANGE Emp SET salary = salary * 1.1"},
            {"key": "B", "text": "UPDATE Emp SET salary = salary * 1.1"},
            {"key": "C", "text": "ALTER Emp SET salary = salary * 1.1"},
            {"key": "D", "text": "MODIFY Emp SET salary = salary * 1.1"},
        ],
    },
    70: {
        "text": "Which of the following is a valid IPv4 address?",
        "options": [
            {"key": "A", "text": "127.12.5.31"},
            {"key": "B", "text": "126.11.3.32"},
            {"key": "C", "text": "12611.5.32"},
            {"key": "D", "text": "128.11.3.31"},
        ],
    },
    71: {
        "text": "Which of the following is NOT desired in a good software requirements specification (SRS)?",
        "options": [
            {"key": "A", "text": "Functional requirements"},
            {"key": "B", "text": "Goals of implementation"},
            {"key": "C", "text": "Algorithm for software implementation"},
            {"key": "D", "text": "Non-functional requirements"},
        ],
    },
    72: {
        "text": "Under which license is Android primarily distributed?",
        "options": [
            {"key": "A", "text": "Proprietary closed license"},
            {"key": "B", "text": "SourceForge license"},
            {"key": "C", "text": "Apache/MIT open-source license"},
            {"key": "D", "text": "None of the above"},
        ],
    },
    73: {
        "text": "What is the main advantage of informed search algorithms?",
        "options": [
            {"key": "A", "text": "They are admissible when the heuristic is admissible"},
            {"key": "B", "text": "They are always optimal without conditions"},
            {"key": "C", "text": "They are always complete in finite graphs"},
            {"key": "D", "text": "They never use heuristics"},
        ],
    },
    76: {
        "text": "What is the difference between Dijkstra's algorithm and Uniform Cost Search (UCS)?",
        "options": [
            {"key": "A", "text": "UCS is optimal but Dijkstra is not"},
            {"key": "B", "text": "They are essentially the same for non-negative edge costs"},
            {"key": "C", "text": "Dijkstra uses a queue while UCS does not"},
            {"key": "D", "text": "UCS uses a stack while Dijkstra uses a queue"},
        ],
    },
    77: {
        "text": "Which one of the following is NOT possible in Java?",
        "options": [
            {"key": "A", "text": "Implement more than one interface"},
            {"key": "B", "text": "Execute more than one thread at a time"},
            {"key": "C", "text": "Create arrays with more than two dimensions"},
            {"key": "D", "text": "Create and manipulate raw pointers like C++"},
        ],
    },
    78: {
        "text": "A public-key cryptosystem is useful because:",
        "options": [
            {"key": "A", "text": "It uses two different keys (public and private)"},
            {"key": "B", "text": "It is purely symmetric"},
            {"key": "C", "text": "It eliminates all key distribution needs without any tradeoffs"},
            {"key": "D", "text": "Private keys are published openly"},
        ],
    },
    80: {
        "text": "What are some benefits of big data applications?",
        "options": [
            {"key": "A", "text": "Improved decision-making"},
            {"key": "B", "text": "Better customer understanding"},
            {"key": "C", "text": "Enhanced operational efficiency"},
            {"key": "D", "text": "All of the above"},
        ],
    },
    81: {
        "text": "______ involves generating, collecting, disseminating, and storing project information.",
        "options": [
            {"key": "A", "text": "Critical management"},
            {"key": "B", "text": "Configuration management"},
            {"key": "C", "text": "Concurrent management"},
            {"key": "D", "text": "Communication management"},
        ],
    },
    83: {
        "text": "A hotel booking system was updated with real-time room availability. A tester verifies that booking and payment still work. What testing is this?",
        "options": [
            {"key": "A", "text": "User acceptance testing"},
            {"key": "B", "text": "Functional testing"},
            {"key": "C", "text": "Regression testing"},
            {"key": "D", "text": "Integration testing"},
        ],
    },
    84: {
        "text": "Which agile method uses the metaphor of a team moving the ball downfield in an apparently ad hoc manner?",
        "options": [
            {"key": "A", "text": "RAD"},
            {"key": "B", "text": "DSDM"},
            {"key": "C", "text": "Evolutionary waterfall"},
            {"key": "D", "text": "Scrum"},
        ],
    },
    85: {
        "text": "A good software requirements specification should NOT be characterized by:",
        "options": [
            {"key": "A", "text": "Completeness"},
            {"key": "B", "text": "Reliability (as a substitute for clarity/consistency)"},
            {"key": "C", "text": "Consistency"},
            {"key": "D", "text": "Clarity"},
        ],
    },
    87: {
        "text": "What does the ... (spread) operator do in JavaScript?",
        "options": [
            {"key": "A", "text": "Makes a for-loop execute three times"},
            {"key": "B", "text": "Spreads iterables into individual elements"},
            {"key": "C", "text": "Continues iterators with a fixed increment"},
            {"key": "D", "text": "No such operator exists"},
        ],
    },
    88: {
        "text": "Which memory management scheme is NOT used for mapping logical addresses to physical addresses?",
        "options": [
            {"key": "A", "text": "Segmentation"},
            {"key": "B", "text": "Paging with segmentation"},
            {"key": "C", "text": "Swapping"},
            {"key": "D", "text": "Paging"},
        ],
    },
    89: {
        "text": "Which method is used to access HTML elements using JavaScript?",
        "options": [
            {"key": "A", "text": "document.getElementById()"},
            {"key": "B", "text": "getElementsByHTMLName()"},
            {"key": "C", "text": "getHTMLClassByName()"},
            {"key": "D", "text": "getElementsByClassName()"},
        ],
    },
    90: {
        "text": "Computing project cost by comparing to a similar project in the same application domain is called:",
        "options": [
            {"key": "A", "text": "Estimation by analogy"},
            {"key": "B", "text": "Empirical model"},
            {"key": "C", "text": "Expert judgement"},
            {"key": "D", "text": "Ad hoc approach"},
        ],
    },
    94: {
        "text": "Which of the following is NOT an objective of software testing?",
        "options": [
            {"key": "A", "text": "Enhancing usability"},
            {"key": "B", "text": "Increasing development time"},
            {"key": "C", "text": "Identifying defects"},
            {"key": "D", "text": "Improving performance"},
        ],
        "answer": "B",
    },
    95: {
        "text": "The CPU fetches the next instruction from memory according to the value of the:",
        "options": [
            {"key": "A", "text": "Program counter"},
            {"key": "B", "text": "Program status word"},
            {"key": "C", "text": "Instruction register"},
            {"key": "D", "text": "Status register"},
        ],
    },
    96: {
        "text": "What is the first step in the data-driven decision-making process?",
        "options": [
            {"key": "A", "text": "Making a decision"},
            {"key": "B", "text": "Analyzing data"},
            {"key": "C", "text": "Interpreting results"},
            {"key": "D", "text": "Collecting data"},
        ],
    },
    97: {
        "text": "Triple DES (3DES) works by:",
        "options": [
            {"key": "A", "text": "Using 144-bit blocks with a single DES pass"},
            {"key": "B", "text": "Applying DES three times on 64-bit blocks with 56-bit keys"},
            {"key": "C", "text": "Using only 128-bit blocks with two DES passes"},
            {"key": "D", "text": "Replacing DES with AES in one round"},
        ],
    },
    98: {
        "text": "Which of the following is an example of a checked exception in Java?",
        "options": [
            {"key": "A", "text": "IOException"},
            {"key": "B", "text": "RuntimeException"},
            {"key": "C", "text": "NumberFormatException"},
            {"key": "D", "text": "NegativeArraySizeException"},
        ],
    },
    99: {
        "text": "Which is a FALSE assumption when solving the critical-region problem to avoid race conditions?",
        "options": [
            {"key": "A", "text": "No process outside its critical region may block others indefinitely"},
            {"key": "B", "text": "Assumptions may be made about CPU speeds and number of processors"},
            {"key": "C", "text": "No process waits forever to enter its critical region"},
            {"key": "D", "text": "No two processes are simultaneously inside their critical regions"},
        ],
    },
}

FOCUS_GUIDE = {
    "Database": "Normalization, keys, ER diagrams, SQL updates, and functional dependencies.",
    "Java/OOP": "OOP concepts, package scope, exceptions, GC, and what Java cannot do (pointers).",
    "Networking": "OSI layers, TCP reliability, ICMP, ports, IPv4, CORS, and topology fault isolation.",
    "Android": "Services, lifecycle, src folder, licensing, and content providers.",
    "Security": "Saltzer-Schroeder principles, PKI, Triple DES, integrity, and malware types.",
    "PM": "Spiral model, risk retention, WBS tasks, critical path, and communication management.",
    "AI/ML": "Supervised learning, search algorithms (UCS, BFS, A*), and local search.",
    "SE": "SRS properties, requirements engineering, maintenance types, and testing process.",
    "OS": "Process creation, fork(), threads, memory mapping vs swapping, and program counter.",
    "C++": "Time complexity of loops and trace small code outputs.",
    "Web": "CSS types, JavaScript spread/async, DOM access, and HTTP status codes.",
    "Data Structures": "Queues, selection sort swaps, sorting complexity, and binary search.",
    "Software Architecture": "Quality scenarios, layered architecture, coupling, and architecture goals.",
    "General": "Review lecture notes for any remaining topics.",
}

# Per-question teaching blurbs for deep explanations (examNumber -> dict)
DEEP_NOTES: dict[int, dict] = {}
