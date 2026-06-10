"""Build deep explanations for 2025 MoEE Exit Exam."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / "data" / "exams" / "moe2025" / "questions.json"
OUT_PATH = ROOT / "data" / "exams" / "moe2025" / "deep_explanations.json"


def _opt(correct: str, key: str, text: str, body: str) -> str:
    tag = "CORRECT" if key == correct else "INCORRECT"
    return f'Option {key} ({tag}): "{text}". {body}'


def _wrong(text: str, reason: str) -> str:
    return f'"{text}" sounds plausible but is wrong because {reason}'


def _right(text: str, reason: str) -> str:
    return f'"{text}" is correct because {reason}'


# Per-question deep teaching content: overview, option bodies (A-D), studyTip
# Keys are examNumber (1-100)
BANK: dict[int, dict[str, Any]] = {}


def _reg(n: int, overview: str, opts: dict[str, str], tip: str) -> None:
    BANK[n] = {"overview": overview, "options": opts, "studyTip": tip}


def _build_bank() -> None:
    """Register handcrafted deep explanations for all 100 questions."""

    _reg(1,
         "Loops are control-flow structures that repeat a block of code while a condition holds (for/while) "
         "or for a fixed count (for). Their primary purpose is iteration — executing the same logic multiple times "
         "without duplicating source lines. Variable declaration, function definition, and exception handling are "
         "separate language features with different roles.",
         {"A": _wrong("To declare variables", "variable declaration happens once with assignment or type "
                      "declarations; loops consume variables but do not create them as their primary purpose."),
          "B": _right("To execute a block of code repeatedly", "this is the defining behavior of every loop "
                      "construct — for, while, do-while — in all mainstream languages."),
          "C": _wrong("To define a function", "functions group reusable code; loops call code repeatedly "
                      "inside an existing block but do not define named callable units."),
          "D": _wrong("To handle exceptions", "try/catch (or try/except) blocks handle runtime errors; "
                      "loops control repetition, not error recovery.")},
         "Loop = repeat; if = branch; function = reuse; try = errors.")

    _reg(2,
         "In C, the `/` operator performs integer division when both operands are integers. "
         "5 / 2 discards the fractional part (truncates toward zero), yielding 2 — not 2.5. "
         "To get floating-point division you need at least one operand as float/double (e.g., 5.0 / 2). "
         "printf(\"%d\", ...) expects an integer format specifier.",
         {"A": _wrong("2.5", "2.5 is a floating-point result; integer division in C never produces a float "
                      "without casting or using float literals."),
          "B": _right("2", "integer division 5/2 = 2 with remainder 1 discarded; %d prints 2."),
          "C": _wrong("3", "3 would require rounding up (ceiling), but C integer division truncates down."),
          "D": _wrong("0", "0 would imply 2/5 or a modulo confusion, not 5/2.")},
         "C integer `/` truncates: 5/2=2, 7/2=3. Use 5.0/2 for 2.5.")

    _reg(3,
         "Python identifier rules: must start with a letter or underscore; may contain letters, digits, "
         "and underscores; cannot start with a digit; hyphens and # are operators/syntax, not name characters. "
         "variable_1 satisfies all rules.",
         {"A": _wrong("1variable", "identifiers cannot begin with a digit — SyntaxError at parse time."),
          "B": _right("variable_1", "starts with letter, contains underscore and digit — fully valid Python name."),
          "C": _wrong("variable-1", "hyphen is the subtraction operator; Python parses this as variable minus 1."),
          "D": _wrong("variable#1", "# starts an inline comment; not part of an identifier.")},
         "Python names: [a-zA-Z_][a-zA-Z0-9_]* — no hyphens, no leading digits.")

    _reg(4,
         "break immediately terminates the innermost enclosing loop or switch, transferring control to the "
         "statement after the loop. continue skips the rest of the current iteration and jumps to the next "
         "loop test. They are frequently confused on exams.",
         {"A": _wrong("Skips the current iteration", "that is continue, not break — continue goes to next "
                      "iteration while staying inside the loop."),
          "B": _right("Exits the loop entirely", "break leaves the loop completely; no further iterations run."),
          "C": _wrong("Restarts the loop", "no standard keyword restarts from iteration 1; you'd reassign "
                      "counter or use a nested loop structure."),
          "D": _wrong("Continues to the next iteration", "that describes continue; break exits, not advances.")},
         "break = exit loop; continue = skip to next iteration.")

    _reg(5,
         "Java constants are declared with final — applied to variables, methods (no override), or classes "
         "(no subclass). C/C++ use const; Python has no true const keyword; immutable is a general concept, "
         "not a Java keyword.",
         {"A": _wrong("static", "static means class-level membership/shared state, not immutability."),
          "B": _right("final", "final variable must be assigned once; reference cannot point to new object "
                      "(object internals may still mutate unless deeply immutable)."),
          "C": _wrong("const", "const is C/C++ keyword; Java uses final instead."),
          "D": _wrong("immutable", "not a Java keyword — immutability is achieved via final + design "
                      "(e.g., String class).")},
         "Java constant field: private static final TYPE NAME = value;")

    _reg(6,
         "Linear search scans each of n elements once in the worst case, comparing the target with every item "
         "until found or exhausted. Time complexity is O(n) — linear in input size. O(1) is direct index access; "
         "O(log n) is binary search on sorted data; O(n²) is nested loops.",
         {"A": _wrong("O(1)", "constant time requires direct addressing (array index, hash lookup average case) "
                      "— linear search may scan all n elements."),
          "B": _right("O(n)", "one pass through up to n elements → linear time."),
          "C": _wrong("O(log n)", "logarithmic search halves the search space each step (binary search), "
                      "not sequential scan."),
          "D": _wrong("O(n²)", "quadratic time implies nested iteration over n — not a single linear scan.")},
         "Unsorted search = O(n); sorted array binary search = O(log n).")

    _reg(7,
         "Conditional execution selects one path based on a Boolean condition. if-else (and switch/match "
         "variants) implement branching. Loops repeat; functions organize code; arrays store data.",
         {"A": _wrong("Loop", "loops repeat while/for a condition; they don't choose between alternate "
                      "single-pass paths like if-else."),
          "B": _wrong("Function", "functions encapsulate code but don't inherently branch — branching uses "
                      "if inside functions."),
          "C": _right("If-else statement", "evaluates condition and executes exactly one branch — core "
                      "conditional construct."),
          "D": _wrong("Array", "arrays are data structures for storing multiple values, not control flow.")},
         "Selection (if) vs iteration (loop) vs sequence (statements) — classic control-flow trio.")

    _reg(8,
         "Python comparison operators return bool. x > 5 is True (10>5) and x < 15 is True (10<15). "
         "and requires both True → print outputs True. It does not print the number 10 or raise an error.",
         {"A": _right("True", "both comparisons hold for x=10, so boolean and is True."),
          "B": _wrong("False", "would require at least one comparison to fail — neither does for x=10."),
          "C": _wrong("10", "print receives a boolean expression result, not the integer x."),
          "D": _wrong("Error", "syntax and types are valid; no exception raised.")},
         "Python print(bool_expr) prints True/False, not the original integer.")

    _reg(9,
         "C primitive types include int, char, float, double, void, etc. string is NOT a built-in primitive — "
         "C uses char arrays or char* for text. stdio.h provides string handling via C strings, not a string type.",
         {"A": _wrong("int", "int is fundamental numeric primitive in C."),
          "B": _wrong("float", "float is standard floating-point primitive."),
          "C": _right("string", "C has no string primitive; text is char[] or pointer to char."),
          "D": _wrong("char", "char stores single character — primitive type.")},
         "C primitives: int, char, float, double. Text = char array.")

    _reg(10,
         "Modular programming decomposes a large program into smaller modules (functions, classes, files) "
         "with clear interfaces. Benefits: easier testing, maintenance, team parallel work, and reuse. "
         "It does not eliminate debugging or intentionally slow execution.",
         {"A": _wrong("To increase code complexity", "modularity reduces perceived complexity by separation "
                      "of concerns — opposite of this answer."),
          "B": _right("To break a program into smaller, manageable functions", "core definition of modular "
                      "design — divide and conquer at code level."),
          "C": _wrong("To eliminate the need for debugging", "bugs still occur; modules make isolation "
                      "easier but don't remove debugging."),
          "D": _wrong("To reduce program execution speed", "modularity may add tiny call overhead but goal "
                      "is maintainability, not slower execution.")},
         "Modular = smaller units + interfaces; think functions, packages, layers.")

    _reg(11,
         "Python supports tuple unpacking for simultaneous assignment: a, b = b, a swaps without temp variable "
         "by evaluating RHS tuple first then binding names. Arithmetic swap works in some languages but is "
         "unnecessary in Python. a=b; b=a fails to swap (loses original a). swap() is not built-in.",
         {"A": _wrong("a = a + b; b = a - b; a = a - b", "arithmetic swap works in languages without "
                      "tuple unpacking but is error-prone with overflow; Python idiomatic way is C."),
          "B": _wrong("a = b; b = a", "after first line both hold b's old value — original a is lost."),
          "C": _right("a, b = b, a", "Python evaluates (b, a) tuple then unpacks — elegant one-line swap."),
          "D": _wrong("swap(a, b)", "no built-in swap(); you'd need a custom function.")},
         "Python swap idiom: a, b = b, a — always remember RHS evaluated first.")

    _reg(12,
         "Arrays have fixed size (in many languages) and O(1) random access but costly insert/delete in middle. "
         "Linked lists allocate nodes dynamically — grow/shrink at runtime without predeclaring max size. "
         "Access is O(n) for linked lists; memory overhead per node exists.",
         {"A": _wrong("Faster access time", "arrays offer O(1) index access; linked lists require O(n) traversal."),
          "B": _right("Dynamic size adjustment", "linked lists allocate nodes as needed — primary advantage "
                      "over static arrays."),
          "C": _wrong("Less memory usage", "linked lists store pointer overhead per node — often MORE memory."),
          "D": _wrong("Constant-time insertion", "insertion is O(1) only at known position with pointer; "
                      "searching that position is still O(n).")},
         "Linked list wins on dynamic size; array wins on random access.")

    _reg(13,
         "Stack: Last-In-First-Out — push adds to top, pop removes top (like plate stack). "
         "Queue: FIFO — first in, first out. Linked list is implementation structure; binary tree is hierarchical.",
         {"A": _wrong("Queue", "queue is FIFO — opposite order of LIFO."),
          "B": _right("Stack", "LIFO defines stack behavior — used in call stacks, undo, parsing."),
          "C": _wrong("Linked List", "linked list is implementation technique; LIFO describes stack ADT."),
          "D": _wrong("Binary Tree", "tree organizes hierarchical data with left/right children, not LIFO.")},
         "LIFO = Stack; FIFO = Queue — memorize both acronyms.")

    _reg(14,
         "QuickSort average O(n log n) but worst case O(n²) when pivots are poorly chosen (already sorted "
         "with first-element pivot). MergeSort guarantees O(n log n) worst case. Exam asks worst case.",
         {"A": _wrong("O(n log n)", "average/good-case QuickSort, not worst case."),
          "B": _right("O(n²)", "worst case with unbalanced partitions — all elements on one side of pivot."),
          "C": _wrong("O(n)", "linear time is one pass — QuickSort is divide-and-conquer with recursion."),
          "D": _wrong("O(log n)", "logarithmic is binary search style, not sorting entire array.")},
         "QuickSort worst = O(n²); MergeSort worst = O(n log n).")

    _reg(15,
         "Dijkstra's algorithm finds shortest paths from a source to all vertices in weighted graphs with "
         "non-negative edge weights. DFS/BFS don't handle weighted shortest path optimally. Merge Sort sorts arrays.",
         {"A": _wrong("Depth-First Search", "DFS explores deeply — doesn't guarantee shortest weighted path."),
          "B": _wrong("Breadth-First Search", "BFS finds shortest path in unweighted graphs, not weighted."),
          "C": _right("Dijkstra's Algorithm", "classic greedy algorithm for non-negative weighted shortest paths."),
          "D": _wrong("Merge Sort", "sorting algorithm, unrelated to graph pathfinding.")},
         "Weighted shortest path (non-negative) → Dijkstra; unweighted → BFS.")

    _reg(16,
         "Binary Search Tree property: for every node, all keys in left subtree are less than node's key; "
         "all keys in right subtree are greater (or equal depending on variant). "
         "Less-than values go LEFT of root.",
         {"A": _wrong("Right subtree", "right subtree holds values GREATER than root."),
          "B": _right("Left subtree", "BST invariant: left < root < right."),
          "C": _wrong("Parent node", "parent is one level up — not where all smaller values live."),
          "D": _wrong("Root node", "root is single comparison point; smaller values descend left.")},
         "BST: left smaller, right larger — trace insertions on paper.")

    _reg(17,
         "Balanced BST (AVL, Red-Black) maintains height O(log n), so insert/search/delete are O(log n). "
         "Unbalanced degenerate tree can be O(n). Balanced guarantees logarithmic height.",
         {"A": _wrong("O(1)", "insertion must traverse tree height — cannot be constant for arbitrary size."),
          "B": _wrong("O(n)", "would be skewed/unbalanced tree worst case, not balanced BST."),
          "C": _right("O(log n)", "balanced tree height ~ log n → insert takes proportional steps."),
          "D": _wrong("O(n²)", "no standard BST operation is quadratic for single insert.")},
         "Balanced BST operations: O(log n); skewed chain: O(n).")

    _reg(18,
         "Inheritance allows subclass (derived) to acquire fields and methods from superclass (base). "
         "Encapsulation hides internals; polymorphism is many forms; abstraction hides complexity.",
         {"A": _wrong("Encapsulation", "bundling data + methods with access control — not parent-child sharing."),
          "B": _wrong("Polymorphism", "same interface, different behavior — often uses inheritance but is "
                      "distinct principle."),
          "C": _right("Inheritance", "is-a relationship: Dog extends Animal inherits sound(), etc."),
          "D": _wrong("Abstraction", "showing essential features while hiding detail — broader design concept.")},
         "Four OOP pillars: Encapsulation, Abstraction, Inheritance, Polymorphism.")

    _reg(19,
         "Encapsulation restricts direct access to internal state via private fields and public getters/setters. "
         "Goal: protect invariants, reduce coupling, allow implementation change without breaking clients.",
         {"A": _wrong("To allow multiple inheritance", "Java allows one class inheritance; multiple inheritance "
                      "is separate language feature, not encapsulation's purpose."),
          "B": _right("To hide data and restrict direct access", "private/protected modifiers + accessors = "
                      "encapsulation."),
          "C": _wrong("To enable method overloading", "overloading is compile-time polymorphism — same name, "
                      "different parameters."),
          "D": _wrong("To create abstract classes", "abstract classes support inheritance/abstraction, not "
                      "primarily data hiding definition.")},
         "Encapsulation = data hiding + controlled access through methods.")

    _reg(20,
         "Java this refers to current object instance — access instance fields, call other constructors "
         "(this()), pass current object. super refers to parent class. self is Python. instance is not keyword.",
         {"A": _right("this", "this.field, this.method(), this() constructor chaining."),
          "B": _wrong("super", "super accesses superclass members — different from current object reference."),
          "C": _wrong("self", "Python convention for instance reference; Java uses this."),
          "D": _wrong("instance", "not a Java keyword for current object.")},
         "Java: this (current), super (parent). Python: self.")

    _reg(21,
         "Runtime polymorphism: Animal reference holds Dog object; overridden sound() in Dog is invoked via "
         "dynamic dispatch (virtual method table). Static type is Animal; dynamic type is Dog — Bark prints.",
         {"A": _wrong("Generic sound", "would be result if sound() were not overridden or reference called "
                      "static binding on non-virtual method."),
          "B": _right("Bark", "method overriding + dynamic dispatch → Dog.sound() runs."),
          "C": _wrong("Error", "valid Java — subclass IS-A superclass; assignment legal."),
          "D": _wrong("No output", "sound() explicitly prints Bark.")},
         "Override + parent reference to child object → child method runs (dynamic binding).")

    _reg(22,
         "Polymorphism ('many forms'): same method name, different behavior in subclasses via overriding, "
         "or overloading at compile time. Overriding subclass method is classic polymorphism example.",
         {"A": _wrong("Defining a variable", "basic syntax — not polymorphism."),
          "B": _right("Overriding a method in a subclass", "runtime polymorphism through method override."),
          "C": _wrong("Declaring a constant", "final const declaration — unrelated."),
          "D": _wrong("Creating a loop", "control flow — not OOP polymorphism.")},
         "Polymorphism types: override (runtime) vs overload (compile-time).")

    _reg(23,
         "HTML anchor element <a href=\"url\"> creates clickable hyperlinks. <link> is for external resources "
         "(CSS) in head. <href> and <url> are not valid HTML tags.",
         {"A": _wrong("<link>", "link associates document with stylesheet/icon — not inline hyperlinks."),
          "B": _right("<a>", "anchor tag with href attribute defines hyperlinks."),
          "C": _wrong("<href>", "not an HTML element — href is an attribute name."),
          "D": _wrong("<url>", "not standard HTML tag.")},
         "Hyperlink = <a href=\"...\">text</a>; stylesheet = <link rel=\"stylesheet\">.")

    _reg(24,
         "CSS (Cascading Style Sheets) controls presentation: colors, fonts, layout, spacing, responsive design. "
         "HTML structures content; JavaScript adds behavior; server-side code handles business logic.",
         {"A": _wrong("To handle server-side logic", "PHP, Java servlets, Node handle server logic — not CSS."),
          "B": _right("To style and format web pages", "CSS separates presentation from HTML structure."),
          "C": _wrong("To manage databases", "DBMS/SQL layer — unrelated to CSS."),
          "D": _wrong("To execute JavaScript code", "browser executes JS; CSS is declarative styling rules.")},
         "HTML=structure, CSS=presentation, JS=behavior — separation of concerns.")

    _reg(25,
         "JavaScript array methods: push() adds to end; pop() removes from end; shift() removes from front; "
         "unshift() adds to front. push/end pair is most commonly tested.",
         {"A": _right("push()", "arr.push(item) appends to end, returns new length."),
          "B": _wrong("pop()", "removes and returns LAST element — opposite of add."),
          "C": _wrong("shift()", "removes FIRST element."),
          "D": _wrong("unshift()", "adds to beginning, not end.")},
         "push/pop = end; shift/unshift = front.")

    _reg(26,
         "AJAX = Asynchronous JavaScript and XML — technique for background server communication without "
         "full page reload. Modern apps often use JSON instead of XML but acronym remains.",
         {"A": _right("Asynchronous JavaScript and XML", "correct expansion — async partial updates."),
          "B": _wrong("Active JavaScript and XML", "Active is wrong first word — Asynchronous."),
          "C": _wrong("Asynchronous JSON and XML", "JSON not in original acronym expansion."),
          "D": _wrong("Automated JavaScript and XHTML", "Automated and XHTML are incorrect.")},
         "AJAX enables fetch/XHR calls updating page sections dynamically.")

    _reg(27,
         "HTTP GET requests retrieve/read resources — idempotent, parameters often in URL query string. "
         "POST creates/submits data; PUT updates; DELETE removes.",
         {"A": _wrong("POST", "POST submits entity body — typically create or non-idempotent actions."),
          "B": _right("GET", "retrieve data from server — read operation."),
          "C": _wrong("PUT", "replace/update resource at URI."),
          "D": _wrong("DELETE", "remove resource.")},
         "GET=read, POST=create/submit, PUT=update, DELETE=remove.")

    _reg(28,
         "Classic JavaScript runs in the browser (client-side) interpreting HTML/CSS DOM. "
         "Node.js enables server-side JS but exam default context is browser client execution.",
         {"A": _wrong("Server-side", "server-side JS exists (Node) but traditional web JS is client-side."),
          "B": _right("Client-side", "browser executes JS embedded or linked from HTML."),
          "C": _wrong("Database", "databases run SQL/stored procedures — not JS engine primary role."),
          "D": _wrong("Middleware", "middleware sits between client/server — not primary JS execution context.")},
         "Browser JS manipulates DOM; server logic often PHP/Java/Python/Node.")

    _reg(29,
         "Postfix x++ uses 5 then increments to 6. Prefix ++x increments first. Expression: x++ + ++x "
         "→ 5 + 6 = 11? Wait: after x++ x becomes 6, ++x makes x=7 and uses 7? "
         "Trace: x=5; left x++ returns 5, x=6; ++x returns 7, x=7; 5+7=12. Answer is 12.",
         {"A": _wrong("10", "would be 5+5 without prefix increment on second operand."),
          "B": _wrong("11", "common miscalculation ignoring that ++x increments before use."),
          "C": _right("12", "x++ yields 5; ++x yields 7; sum = 12."),
          "D": _wrong("13", "over-counts increment steps.")},
         "Trace increment operators left-to-right: postfix returns old, prefix returns new.")

    _reg(30,
         "PHP is widely taught as server-side scripting for web (WordPress, legacy apps). "
         "HTML/CSS are markup/style; JavaScript primarily client (though Node exists).",
         {"A": _wrong("HTML", "markup language — not scripting."),
          "B": _wrong("CSS", "stylesheet — not server scripting."),
          "C": _right("PHP", "runs on server, generates HTML dynamically."),
          "D": _wrong("JavaScript", "primarily client-side in browser context of exam.")},
         "Server-side scripting examples: PHP, Python/Django, Java/JSP, Node.js.")

    _reg(31,
         "Django is Python web framework providing MVC/MVT structure, ORM, routing, templates, admin — "
         "full scaffolding for web apps, not just database or styling.",
         {"A": _wrong("To manage database connections only", "ORM is part of Django but framework scope is broader."),
          "B": _right("To provide a structure for developing web applications", "routing, views, templates, models."),
          "C": _wrong("To handle client-side styling", "CSS handles styling; Django is server-side."),
          "D": _wrong("To execute SQL queries directly", "ORM abstracts SQL; not raw query executor only.")},
         "Frameworks (Django, Spring, Rails) = structure + conventions + built-in tools.")

    # Q32-100 continue with same depth...
    _build_bank_part2()


def _build_bank_part2() -> None:
    _reg(32,
         "Android traditionally used Java (now Kotlin preferred officially). Swift is iOS. "
         "Python/C++ are not primary Android app languages.",
         {"A": _wrong("Swift", "Apple iOS/macOS language — not Android."),
          "B": _right("Java", "long-standing primary Android SDK language alongside Kotlin."),
          "C": _wrong("Python", "not native Android UI development language."),
          "D": _wrong("C++", "used in NDK/native code but not primary app language.")},
         "Android: Java/Kotlin + XML layouts; iOS: Swift/Objective-C.")

    _reg(33,
         "Activity represents single screen with UI and lifecycle (onCreate, onPause, etc.). "
         "Service runs background; BroadcastReceiver handles events; ContentProvider shares data.",
         {"A": _right("Activity", "screen + user interaction — defines UI for one focused task."),
          "B": _wrong("Service", "long-running background work without UI."),
          "C": _wrong("Broadcast Receiver", "responds to system/app broadcasts."),
          "D": _wrong("Content Provider", "structured data sharing between apps.")},
         "Activity = screen; Service = background; Intent = messaging.")

    _reg(34,
         "Intent is messaging object for starting activities, services, delivering broadcasts — "
         "carries action, data URI, extras between components.",
         {"A": _wrong("To manage database connections", "Room/SQLite handle persistence — not Intent purpose."),
          "B": _right("To facilitate communication between components", "explicit/implicit intents link app parts."),
          "C": _wrong("To handle background services", "Service component handles background; Intent starts it."),
          "D": _wrong("To secure the application", "permissions/Manifest secure app — not Intent role.")},
         "Intent = navigation + data passing between Android components.")

    _reg(35,
         "AndroidManifest.xml declares app components, permissions, intent filters, package name, "
         "min SDK — required app metadata file.",
         {"A": _right("AndroidManifest.xml", "permissions like INTERNET, CAMERA declared here."),
          "B": _wrong("build.gradle", "build dependencies and SDK versions — not runtime permissions list."),
          "C": _wrong("activity_main.xml", "layout UI definition for one screen."),
          "D": _wrong("MainActivity.java", "Activity logic source — permissions not declared in Java file.")},
         "Permissions and components → AndroidManifest.xml.")

    _reg(36,
         "Mobile security requires encrypting sensitive data at rest (SharedPreferences, SQLite) and in transit (TLS). "
         "Storing passwords/API keys plaintext is critical vulnerability.",
         {"A": _wrong("Using too many colors in the UI", "UX choice — not security vulnerability."),
          "B": _right("Storing sensitive data unencrypted", "data breach if device compromised — major OWASP mobile risk."),
          "C": _wrong("Including large images", "performance/storage concern — not primary security issue."),
          "D": _wrong("Using multiple activities", "normal architecture — not security flaw.")},
         "Mobile security: encrypt secrets, use KeyStore, HTTPS, certificate pinning.")

    _reg(37,
         "Primary key uniquely identifies each row — NOT NULL + UNIQUE. Enables relationships via foreign keys "
         "and efficient indexing.",
         {"A": _wrong("To allow duplicate records", "primary key FORBIDS duplicates — opposite."),
          "B": _right("To uniquely identify each record", "exact definition of primary key constraint."),
          "C": _wrong("To store foreign keys", "foreign keys live in child table referencing parent's PK."),
          "D": _wrong("To index all columns", "PK creates index on key column(s) only — not every column.")},
         "PK = unique + not null identifier per row.")

    _reg(38,
         "SQL DML: INSERT adds rows; UPDATE modifies existing rows; DELETE removes; SELECT queries.",
         {"A": _wrong("INSERT", "adds new records — doesn't modify existing."),
          "B": _right("UPDATE", "SET column= value WHERE condition modifies existing data."),
          "C": _wrong("DELETE", "removes rows — doesn't change remaining row values."),
          "D": _wrong("SELECT", "read-only retrieval — no modification.")},
         "INSERT=add, UPDATE=change, DELETE=remove, SELECT=read.")

    _reg(39,
         "WHERE Age > 20 filters rows strictly greater than 20 — relational comparison on Age column.",
         {"A": _wrong("All records from Students", "no filter would need SELECT * FROM Students without WHERE."),
          "B": _right("Records from Students where Age is greater than 20", "matches SQL predicate exactly."),
          "C": _wrong("Records from Students where Age is less than 20", "would be Age < 20 — wrong operator."),
          "D": _wrong("No records", "returns empty only if no rows satisfy condition — not definition.")},
         "Read WHERE clause literally: > means greater than.")

    _reg(40,
         "Normalization decomposes tables to reduce redundancy and update anomalies (insert/delete/update). "
         "Goals: 1NF, 2NF, 3NF, BCNF — organized data without unnecessary duplication.",
         {"A": _wrong("Adding redundant data to tables", "denormalization adds redundancy — opposite of normalization."),
          "B": _right("Organizing data to eliminate redundancy", "core purpose of normalization process."),
          "C": _wrong("Creating multiple databases", "normalization works within schema design — not multi-DB creation."),
          "D": _wrong("Deleting unused tables", "may happen during redesign but not definition of normalization.")},
         "Normalization removes redundancy; denormalization adds it for performance.")

    _reg(41,
         "One-to-Many: one parent row relates to many child rows via FK in child table "
         "(one Department, many Employees). One-to-One is rare; Many-to-Many needs junction table.",
         {"A": _wrong("One-to-One", "each parent maps to exactly one child — stricter than PK-FK typical pattern."),
          "B": _right("One-to-Many", "classic PK in parent, FK in child referencing it."),
          "C": _wrong("Many-to-Many", "requires associative/junction table with two FKs."),
          "D": _wrong("No relationship", "FK explicitly defines relationship.")},
         "PK→FK pattern usually One-to-Many (one customer, many orders).")

    _reg(42,
         "ACID transaction properties: Atomicity (all or nothing), Consistency (valid state), "
         "Isolation (concurrent transactions don't interfere), Durability (committed survives crash).",
         {"A": _right("Atomicity, Consistency, Isolation, Durability", "canonical database transaction acronym."),
          "B": _wrong("Accuracy, Completeness, Integrity, Dependability", "plausible words but not ACID expansion."),
          "C": _wrong("Adaptability, Connectivity, Isolation, Durability", "wrong first letters — not ACID."),
          "D": _wrong("Atomicity, Consistency, Integration, Durability", "Integration is wrong third word.")},
         "ACID: Atomicity, Consistency, Isolation, Durability — memorize exactly.")

    _reg(43,
         "Operating system manages CPU, memory, I/O devices, file systems; provides abstraction and "
         "scheduling for applications. It doesn't write app code or compile programs (compiler tool job).",
         {"A": _wrong("To write application code", "developers write applications; OS provides platform."),
          "B": _right("To manage hardware and software resources", "core OS definition — resource manager."),
          "C": _wrong("To design user interfaces", "UI design is application/GUI toolkit layer."),
          "D": _wrong("To compile programs", "compiler is separate utility (gcc, javac) — OS may invoke it.")},
         "OS = resource manager + abstraction layer between hardware and apps.")

    _reg(44,
         "Shortest Job Next (SJN) / Shortest Remaining Time First picks process with smallest next CPU burst. "
         "FCFS is arrival order; Round Robin uses time quantum; Priority uses priority field.",
         {"A": _wrong("First-Come, First-Served", "FIFO queue — ignores burst length."),
          "B": _right("Shortest Job Next", "selects shortest next CPU burst — minimizes average wait in theory."),
          "C": _wrong("Round Robin", "time-sliced fair scheduling with quantum."),
          "D": _wrong("Priority Scheduling", "uses priority values, not strictly shortest burst.")},
         "Shortest burst → SJN/SRTF; time quantum → Round Robin.")

    _reg(45,
         "Deadlock: circular wait — each process holds resource another needs, none can proceed. "
         "Requires mutual exclusion, hold-and-wait, no preemption, circular wait (Coffman conditions).",
         {"A": _wrong("A process running indefinitely", "infinite loop — not deadlock (no resource circular wait)."),
          "B": _right("A situation where processes are unable to proceed due to resource conflicts",
                      "classic deadlock definition."),
          "C": _wrong("A memory overflow error", "may kill process but not mutual blocking deadlock."),
          "D": _wrong("A hardware failure", "physical fault — unrelated to resource deadlock.")},
         "Deadlock = circular wait for resources; prevention/avoidance/detection strategies exist.")

    _reg(46,
         "Paging divides physical memory into fixed-size frames; logical memory into same-size pages. "
         "Segmentation uses variable-sized logical segments. Swapping moves processes in/out of memory.",
         {"A": _right("Paging", "fixed-size partitions (frames/pages) — answer."),
          "B": _wrong("Segmentation", "variable-sized segments reflecting logical program parts."),
          "C": _wrong("Swapping", "moves entire processes between disk and memory."),
          "D": _wrong("Fragmentation", "problem (external/internal), not management technique.")},
         "Paging = fixed size; Segmentation = variable size; both map virtual→physical.")

    _reg(47,
         "Mutex (mutual exclusion lock) ensures only one thread/process enters critical section at a time, "
         "preventing race conditions on shared data.",
         {"A": _wrong("To allocate memory", "malloc/allocator handles memory — not mutex."),
          "B": _right("To ensure mutual exclusion", "lock before critical section, unlock after."),
          "C": _wrong("To schedule processes", "scheduler picks next process — different subsystem."),
          "D": _wrong("To manage I/O devices", "device drivers/I/O subsystem — not mutex role.")},
         "Mutex/semaphore = synchronization; scheduler = CPU allocation.")

    _reg(48,
         "Modern OS security: user authentication, access control lists, ASLR, DEP, encryption, "
         "mandatory access control. Plaintext passwords and disabling firewalls are anti-patterns.",
         {"A": _wrong("Allowing unrestricted access to all files", "violates least privilege — security failure."),
          "B": _right("Implementing user authentication", "verify identity before granting access — valid control."),
          "C": _wrong("Disabling firewalls", "weakens network protection — bad practice."),
          "D": _wrong("Storing passwords in plain text", "critical vulnerability — never acceptable.")},
         "OS security: authentication, authorization, auditing, encryption.")

    _reg(49,
         "Software engineering applies systematic, disciplined, quantifiable approaches to develop "
         "reliable, efficient, maintainable software — not increasing complexity or skipping testing.",
         {"A": _wrong("To increase software complexity", "goal is manage complexity, not increase it."),
          "B": _right("To develop reliable and efficient software systems", "IEEE/SWEBOK aligned primary goal."),
          "C": _wrong("To reduce software documentation", "appropriate documentation is essential deliverable."),
          "D": _wrong("To eliminate testing", "testing is integral to quality assurance.")},
         "SE = systematic development of quality software within constraints.")

    _reg(50,
         "Waterfall model: requirements → design → implementation → testing → maintenance in strict "
         "sequential phases with phase gates. Agile/Scrum are iterative; Spiral is risk-driven cycles.",
         {"A": _wrong("Agile", "iterative, adaptive — opposite of strict linear sequence."),
          "B": _right("Waterfall", "linear sequential SDLC model."),
          "C": _wrong("Spiral", "iterative with explicit risk analysis loops."),
          "D": _wrong("Scrum", "agile framework with sprints — not linear waterfall.")},
         "Waterfall = sequential phases; Agile = iterative delivery.")

    _reg(51,
         "Agile emphasizes iterative/incremental delivery, customer collaboration, responding to change. "
         "Fixed requirements and no user involvement contradict Agile Manifesto values.",
         {"A": _wrong("Fixed requirements throughout the project", "Agile expects evolving requirements."),
          "B": _right("Iterative and incremental development", "short cycles delivering working software."),
          "C": _wrong("No user involvement", "Agile requires continuous stakeholder/customer feedback."),
          "D": _wrong("Single-phase development", "multiple iterations/sprints — not one phase.")},
         "Agile Manifesto: individuals, working software, collaboration, responding to change.")

    _reg(52,
         "UML dynamic behavior diagrams: Sequence (message order over time), Activity (workflow), "
         "State Machine (state transitions). Class/Component are structural.",
         {"A": _wrong("Class Diagram", "static structure — classes, attributes, relationships."),
          "B": _wrong("Use Case Diagram", "actor-system interactions — behavioral at use-case level."),
          "C": _right("Sequence Diagram", "shows object interactions over time — dynamic behavior."),
          "D": _wrong("Component Diagram", "physical/software components and dependencies — structural.")},
         "Dynamic: Sequence, Activity, State. Static: Class, Component, Deployment.")

    _reg(53,
         "Feasibility study evaluates technical, economic, operational, schedule viability before "
         "committing resources — answers 'should we proceed?' not how to code.",
         {"A": _wrong("To write code for the project", "implementation phase activity."),
          "B": _right("To assess the viability of a project", "technical/economic/operational feasibility analysis."),
          "C": _wrong("To deploy the software", "deployment is late SDLC stage."),
          "D": _wrong("To test the software", "verification/validation — separate phase.")},
         "Feasibility = can/should we build it? (TEOS: Technical, Economic, Operational, Schedule).")

    _reg(54,
         "Non-functional requirements (NFRs) specify quality constraints: performance, security, usability, "
         "reliability. Login, store data, generate reports are functional capabilities.",
         {"A": _wrong("The system must allow users to log in", "functional — describes a system capability."),
          "B": _right("The system must respond within 2 seconds", "performance NFR — measurable quality constraint."),
          "C": _wrong("The system must store user data", "functional data storage requirement."),
          "D": _wrong("The system must generate reports", "functional feature requirement.")},
         "Functional = what system does; Non-functional = how well (quality attributes).")

    _reg(55,
         "Requirements elicitation discovers stakeholder needs through interviews, workshops, observation, "
         "prototypes — before design and coding.",
         {"A": _wrong("To test the software", "testing validates built product — post-implementation."),
          "B": _right("To gather and document user needs", "elicitation = extract and record requirements."),
          "C": _wrong("To deploy the system", "release to production — far downstream."),
          "D": _wrong("To write code", "implementation follows requirements specification.")},
         "Elicitation techniques: interviews, surveys, observation, prototyping, document analysis.")

    _reg(56,
         "Stakeholder interviews are classic requirements gathering technique — direct conversation "
         "to uncover needs, constraints, and priorities.",
         {"A": _wrong("Writing code", "implementation — not requirements gathering."),
          "B": _right("Conducting interviews", "structured/unstructured interviews with stakeholders."),
          "C": _wrong("Debugging software", "fixing defects in existing code."),
          "D": _wrong("Deploying the system", "release activity — not elicitation.")},
         "Requirements gathering: interviews, JAD sessions, questionnaires, ethnography.")

    _reg(57,
         "Testable requirement is unambiguous, measurable, verifiable with clear acceptance criteria. "
         "'System shall respond within 2 seconds under 100 concurrent users' is testable; "
         "'system shall be fast' is not.",
         {"A": _wrong("It is vague and ambiguous", "vague requirements are NOT testable."),
          "B": _right("It is measurable and verifiable", "can write test cases with pass/fail criteria."),
          "C": _wrong("It lacks clarity", "lack of clarity prevents testing."),
          "D": _wrong("It is incomplete", "incomplete requirements hinder verification.")},
         "SMART requirements: Specific, Measurable, Achievable, Relevant, Time-bound.")

    _reg(58,
         "Software Requirements Specification (SRS) documents functional and non-functional requirements, "
         "interfaces, constraints — contract between stakeholders and developers.",
         {"A": _wrong("Software Design Document", "SDD describes HOW — architecture and design, not full requirements."),
          "B": _right("Software Requirements Specification (SRS)", "WHAT the system must do and quality constraints."),
          "C": _wrong("Test Plan", "how testing will be conducted — derived from requirements."),
          "D": _wrong("User Manual", "end-user guide for operating finished system.")},
         "SRS = requirements; SDD = design; Test Plan = verification strategy.")

    _reg(59,
         "Requirements change during development (scope creep, new regulations, market shifts) is "
         "primary management challenge — needs traceability and change control.",
         {"A": _wrong("Writing error-free code", "coding challenge — not requirements management focus."),
          "B": _right("Handling requirement changes during development", "change impact analysis and version control."),
          "C": _wrong("Deploying the software", "deployment challenge — different domain."),
          "D": _wrong("Testing the user interface", "UI testing — not requirements management core issue.")},
         "Requirements volatility → change control boards, traceability matrices, agile backlogs.")

    _reg(60,
         "Software architecture defines high-level structure (components, connectors), behavior, "
         "and quality attribute tradeoffs — blueprint before detailed coding.",
         {"A": _wrong("To write detailed code", "implementation follows architecture."),
          "B": _right("To define the system's structure and behavior", "components, interactions, constraints."),
          "C": _wrong("To test the software", "QA activity — separate from architectural definition."),
          "D": _wrong("To deploy the application", "operations/release management.")},
         "Architecture = structures + behaviors + quality attribute rationale.")

    _build_bank_part3()


def _build_bank_part3() -> None:
    _reg(61,
         "Bridge pattern decouples abstraction from implementation so both can vary independently "
         "(e.g., Shape abstraction with different Renderer implementations). "
         "Singleton ensures one instance; Factory creates objects; Observer notifies dependents.",
         {"A": _wrong("Singleton", "ensures single instance — creational pattern, not abstraction/implementation split."),
          "B": _wrong("Factory", "creates objects without specifying exact class — creational."),
          "C": _right("Bridge", "separates interface/abstraction from implementation hierarchy."),
          "D": _wrong("Observer", "publish-subscribe notification — behavioral pattern.")},
         "Bridge = abstraction vs implementation; Adapter = interface conversion.")

    _reg(62,
         "Client-Server architecture: clients request services; servers provide resources — "
         "fundamental web model (browser/server). Monolithic is single deployable; "
         "Pipe-and-Filter streams data; Layered organizes tiers.",
         {"A": _wrong("Monolithic", "single unified application — can host web but exam targets distributed web model."),
          "B": _right("Client-Server", "browsers/clients communicate with web servers — standard web architecture."),
          "C": _wrong("Pipe-and-Filter", "data processing pipeline — Unix filters, compilers — not typical web label."),
          "D": _wrong("Layered", "organizes tiers (presentation/business/data) — can be inside client-server but "
                      "Client-Server is the web-appropriate architectural style asked.")},
         "Web apps: Client-Server with possible Layered or MVC inside server.")

    _reg(63,
         "Quality attributes (non-functional): performance, scalability, availability, security, "
         "modifiability. Programming language and team size are project context, not architecture quality attributes.",
         {"A": _wrong("The programming language used", "technology choice — not ISO 25010 quality attribute."),
          "B": _right("The system's performance or scalability", "classic architectural quality attribute."),
          "C": _wrong("The number of developers", "project staffing — not system quality attribute."),
          "D": _wrong("The project budget", "management constraint — not architecture quality attribute.")},
         "Quality attributes: -ility words (availability, scalability, modifiability, usability).")

    _reg(64,
         "Class Diagram shows static structure: classes, attributes, methods, relationships "
         "(inheritance, association). Sequence/Activity are behavioral; Use Case shows actor interactions.",
         {"A": _wrong("Sequence Diagram", "message passing over time — dynamic behavior."),
          "B": _right("Class Diagram", "structural view of system classes and relationships."),
          "C": _wrong("Activity Diagram", "workflow/process flow — behavioral."),
          "D": _wrong("Use Case Diagram", "actors and use cases — functional scope, not class structure.")},
         "Structure → Class/Component; Behavior → Sequence/Activity/State.")

    _reg(65,
         "Work Breakdown Structure (WBS) hierarchically decomposes project deliverables into "
         "work packages — foundation for scheduling, estimating, assigning responsibility.",
         {"A": _wrong("To write code", "development task — not WBS purpose."),
          "B": _right("To divide a project into manageable tasks", "decomposition of scope into work packages."),
          "C": _wrong("To test the software", "QA activity."),
          "D": _wrong("To deploy the system", "release/operations activity.")},
         "WBS: 100% rule — sum of work packages equals total project scope.")

    _reg(66,
         "Gantt chart visualizes tasks on timeline with bars showing duration and dependencies — "
         "standard PM scheduling tool.",
         {"A": _right("Gantt Chart", "task bars, milestones, dependencies over calendar time."),
          "B": _wrong("Pie Chart", "proportions of whole — not schedule visualization."),
          "C": _wrong("Histogram", "frequency distribution — statistics, not project scheduling."),
          "D": _wrong("Scatter Plot", "correlation between variables — not task dependencies.")},
         "Gantt = schedule; PERT = network diagram; both used in project time management.")

    _reg(67,
         "Risk management: identify, analyze, prioritize, plan responses (mitigate, transfer, avoid, accept), "
         "monitor throughout project lifecycle.",
         {"A": _wrong("Writing code", "implementation — not risk management."),
          "B": _right("Identifying and mitigating potential risks", "core risk management cycle."),
          "C": _wrong("Designing the user interface", "UX design activity."),
          "D": _wrong("Testing the database", "QA/data validation activity.")},
         "Risk response: avoid, mitigate, transfer, accept (AMTA mnemonic).")

    _reg(68,
         "Product Owner owns product backlog, prioritizes user stories by business value, "
         "represents stakeholders. Scrum Master facilitates process; Dev Team builds; stakeholders advise.",
         {"A": _wrong("Scrum Master", "removes impediments, coaches process — doesn't prioritize backlog."),
          "B": _right("Product Owner", "single person accountable for backlog ordering and value."),
          "C": _wrong("Development Team", "implements items — may estimate but PO prioritizes."),
          "D": _wrong("Stakeholders", "provide input but PO makes prioritization decisions.")},
         "Scrum roles: PO=prioritize, SM=process, Team=build.")

    _reg(69,
         "Project schedule plans task start/finish dates, milestones, critical path — "
         "tracks progress against baseline timeline.",
         {"A": _wrong("To document code", "code documentation — developer activity."),
          "B": _right("To plan and track project timelines", "schedule management purpose."),
          "C": _wrong("To test the software", "QA — separate from scheduling."),
          "D": _wrong("To manage hardware resources", "infrastructure — not schedule primary focus.")},
         "Schedule baseline + Gantt/PERT + critical path method (CPM).")

    _reg(70,
         "Unit testing verifies smallest testable units (functions, methods, classes) in isolation, "
         "often with mocks/stubs. Integration/system/UI tests cover broader scope.",
         {"A": _wrong("To test the entire system", "system testing — whole integrated product."),
          "B": _right("To test individual components or functions", "unit test definition."),
          "C": _wrong("To test the user interface", "UI/acceptance testing domain."),
          "D": _wrong("To test the database", "database testing specific layer.")},
         "Test pyramid: many unit tests, fewer integration, fewest E2E/system.")

    _reg(71,
         "White-box (structural) testing uses internal code structure — branches, paths, statements. "
         "Black-box tests I/O without knowing internals. Integration/system are levels, not techniques by structure.",
         {"A": _wrong("Black-box testing", "tests external behavior without code knowledge."),
          "B": _right("White-box testing", "uses code structure for coverage (branch, path)."),
          "C": _wrong("Integration testing", "tests combined modules — test level, not structural technique."),
          "D": _wrong("System testing", "whole system validation — test level.")},
         "White-box = see code (coverage); Black-box = see inputs/outputs only.")

    _reg(72,
         "Test case specifies inputs, execution conditions, expected results to verify specific "
         "requirement or behavior — fundamental QA artifact.",
         {"A": _right("A set of conditions to verify a system's functionality", "test case definition."),
          "B": _wrong("A programming script", "test script automates cases but case is logical specification."),
          "C": _wrong("A project plan", "PM document — different purpose."),
          "D": _wrong("A database schema", "data model — not test case.")},
         "Test case = preconditions + inputs + expected result + postconditions.")

    _reg(73,
         "Quality Assurance ensures processes and products meet specified requirements and standards — "
         "prevent defects through process, not just find them (QC/testing).",
         {"A": _wrong("To increase development time", "QA aims for efficiency with quality — not lengthen arbitrarily."),
          "B": _right("To ensure the software meets specified requirements", "conformance to specs and standards."),
          "C": _wrong("To reduce documentation", "QA often requires documented processes (ISO, CMMI)."),
          "D": _wrong("To eliminate user feedback", "user feedback essential for quality improvement.")},
         "QA = process focus; QC/Testing = product verification.")

    _reg(74,
         "Software defect (bug) is behavior deviating from specified requirements — causes incorrect "
         "results or crashes. Features meeting requirements are not defects.",
         {"A": _wrong("A feature that meets user requirements", "correct behavior — not a defect."),
          "B": _right("A bug that causes incorrect behavior", "failure to meet specification — defect."),
          "C": _wrong("A well-documented code", "good practice — not defect."),
          "D": _wrong("A user manual", "deliverable documentation — not defect.")},
         "Defect = gap between expected (spec) and actual (behavior).")

    _reg(75,
         "Software maintenance modifies deployed software after delivery — corrective, adaptive, "
         "perfective, preventive — not greenfield development.",
         {"A": _wrong("Writing new code from scratch", "new development — not maintenance."),
          "B": _right("Updating and fixing existing software", "maintenance definition per IEEE."),
          "C": _wrong("Designing the user interface", "could be part of perfective maintenance but too narrow."),
          "D": _wrong("Deploying the software", "release activity — maintenance follows deployment.")},
         "Maintenance types: Corrective, Adaptive, Perfective, Preventive (CAPP).")

    _reg(76,
         "Corrective maintenance fixes reported bugs/errors after release. "
         "Adaptive adapts to environment changes; perfective improves performance/features; preventive prevents future issues.",
         {"A": _right("Corrective maintenance", "fixes user-reported faults — answer."),
          "B": _wrong("Adaptive maintenance", "adjusts to OS/hardware/regulatory environment changes."),
          "C": _wrong("Perfective maintenance", "enhancements and performance improvements."),
          "D": _wrong("Preventive maintenance", "refactoring to reduce future failure risk.")},
         "User bug report → Corrective; OS upgrade compatibility → Adaptive.")

    _reg(77,
         "Refactoring improves internal code structure (readability, design patterns) without "
         "changing external observable behavior — key maintenance discipline.",
         {"A": _wrong("Adding new features", "perfective enhancement — changes functionality."),
          "B": _right("Improving code structure without changing functionality", "refactoring definition (Fowler)."),
          "C": _wrong("Deleting old code", "may happen during refactor but not the definition."),
          "D": _wrong("Testing the software", "verification activity — not refactoring.")},
         "Refactor = same behavior, better structure; feature = new behavior.")

    _reg(78,
         "Maintenance cost correlates strongly with system complexity — tangled code, poor documentation, "
         "high coupling increase change cost (Lehman's laws).",
         {"A": _wrong("The programming language used", "minor factor compared to complexity and design quality."),
          "B": _wrong("The number of users", "may affect adaptive load but not primary cost driver in SE theory."),
          "C": _right("The complexity of the software", "complex systems cost more to understand and modify."),
          "D": _wrong("The project timeline", "schedule pressure affects cost but complexity is structural driver.")},
         "Lehman's Law: complexity increases unless work done to reduce it.")

    _reg(79,
         "Best practices (code reviews, testing, documentation, refactoring) improve reliability "
         "and reduce defect rates over system lifetime.",
         {"A": _wrong("Increased software bugs", "best practices reduce bugs — opposite."),
          "B": _right("Improved software reliability", "primary long-term benefit of maintenance discipline."),
          "C": _wrong("Reduced documentation", "good maintenance includes adequate docs."),
          "D": _wrong("Slower development", "initial investment pays off in lower maintenance cost.")},
         "Invest in maintainability early — majority of cost is post-release maintenance.")

    _reg(80,
         "OSI (Open Systems Interconnection) model standardizes networking into 7 layers — "
         "interoperability reference model, not a protocol itself or hardware manager.",
         {"A": _wrong("To write network protocols", "protocols implement layers — OSI is reference framework."),
          "B": _right("To standardize network communication layers", "7-layer conceptual model for teaching/design."),
          "C": _wrong("To manage hardware resources", "OS role — OSI is network-specific."),
          "D": _wrong("To secure the network", "security spans layers but OSI primary purpose is layering standard.")},
         "OSI 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application.")

    _reg(81,
         "Network layer (Layer 3) handles logical addressing (IP) and routing packets across networks. "
         "Data Link (L2) uses MAC/switching; Transport (L4) TCP/UDP; Application (L7) HTTP/DNS.",
         {"A": _wrong("Data Link Layer", "MAC addresses, switches, frames — local segment."),
          "B": _right("Network Layer", "IP routing between networks — routers operate here."),
          "C": _wrong("Transport Layer", "end-to-end segments, TCP/UDP ports."),
          "D": _wrong("Application Layer", "user-facing protocols HTTP, FTP, SMTP.")},
         "Router = Layer 3; Switch = Layer 2; HTTP = Layer 7.")

    _reg(82,
         "Router forwards IP packets between different networks using routing tables — "
         "connects LANs to WANs. Switch connects devices same LAN; doesn't store packets long-term.",
         {"A": _wrong("To connect devices within the same network", "switch/hub role on same broadcast domain."),
          "B": _right("To forward data packets between networks", "router interconnects distinct IP networks."),
          "C": _wrong("To store data packets", "routers forward — buffering temporary, not storage purpose."),
          "D": _wrong("To encrypt data", "VPN appliances may encrypt; basic routing doesn't require encryption.")},
         "Switch = same network; Router = between networks; Gateway = protocol translation.")

    _reg(83,
         "HTTPS = HTTP over TLS/SSL — encrypts web traffic, authenticates server via certificates. "
         "HTTP is plaintext; FTP file transfer; SMTP email.",
         {"A": _wrong("HTTP", "unencrypted web protocol — not secure."),
          "B": _wrong("FTP", "file transfer protocol — not primary secure web browsing."),
          "C": _right("HTTPS", "HTTP Secure — TLS encryption for web communication."),
          "D": _wrong("SMTP", "Simple Mail Transfer Protocol — email, not web browsing security.")},
         "Secure web = HTTPS (port 443); plain HTTP = port 80.")

    _reg(84,
         "Subnet mask defines network vs host portion of IP address, enabling subnet division "
         "and routing decisions — not encryption or DHCP assignment directly.",
         {"A": _wrong("To encrypt network traffic", "encryption uses TLS/IPsec — not subnet mask function."),
          "B": _right("To divide a network into smaller subnetworks", "subnetting splits address space logically."),
          "C": _wrong("To assign IP addresses", "DHCP assigns; mask defines subnet boundaries."),
          "D": _wrong("To secure the network", "ACLs/firewalls secure; mask defines topology.")},
         "Subnet mask + IP = network address + host address (AND operation).")

    _reg(85,
         "Gateway connects networks using different protocols or architectures — "
         "translates between them (e.g., IP to legacy system). Switch/hub same protocol L2; repeater amplifies signal.",
         {"A": _wrong("Switch", "L2 device forwarding frames within same network technology."),
          "B": _wrong("Hub", "L1 broadcast device — deprecated, no intelligence."),
          "C": _right("Gateway", "interconnects heterogeneous networks with protocol translation."),
          "D": _wrong("Repeater", "regenerates signal on same segment — extends distance only.")},
         "Gateway = different network types; Router = different IP subnets same stack.")

    _reg(86,
         "Encryption transforms plaintext to ciphertext using keys — protects confidentiality "
         "so unauthorized parties cannot read data. Does not primarily speed up or simplify code.",
         {"A": _wrong("To increase software size", "ciphertext may be larger but that's side effect, not purpose."),
          "B": _right("To protect data confidentiality", "core goal of encryption in CIA triad."),
          "C": _wrong("To speed up execution", "encryption adds computational overhead — slows, not speeds."),
          "D": _wrong("To simplify code", "crypto adds complexity — libraries help but not simplification goal.")},
         "CIA: Confidentiality (encryption), Integrity (hash/HMAC), Availability (redundancy).")

    _reg(87,
         "SQL Injection inserts malicious SQL through unsanitized user input in web forms/queries — "
         "OWASP Top 10 vulnerability. Phishing is social engineering; DoS floods resources; brute force guesses passwords.",
         {"A": _wrong("Phishing", "deceptive emails/sites stealing credentials — social attack."),
          "B": _right("SQL Injection", "malicious SQL in input fields exploiting dynamic query construction."),
          "C": _wrong("Denial of Service", "overwhelms availability — not code injection into DB queries."),
          "D": _wrong("Brute Force", "systematic password guessing — not SQL code injection.")},
         "Prevent SQLi: parameterized queries/prepared statements, input validation, least privilege DB accounts.")

    _reg(88,
         "Firewall monitors/filters network traffic based on rules (IP, port, protocol) — "
         "perimeter defense between trusted/untrusted networks.",
         {"A": _wrong("To store data", "storage devices/servers store — firewall filters traffic."),
          "B": _right("To monitor and control network traffic", "allow/deny rules at network boundary."),
          "C": _wrong("To assign IP addresses", "DHCP server assigns IP addresses."),
          "D": _wrong("To manage databases", "DBMS manages data — unrelated to firewall.")},
         "Firewall + IDS/IPS = network security monitoring and control.")

    _reg(89,
         "Multi-Factor Authentication (MFA) requires two or more factors: something you know (password), "
         "have (token/phone), are (biometric). SSO is single login for multiple apps — different concept.",
         {"A": _wrong("Single Sign-On", "one login accesses multiple services — convenience, not multi-factor."),
          "B": _right("Multi-Factor Authentication", "combines independent authentication factors."),
          "C": _wrong("Password Authentication", "single factor only — something you know."),
          "D": _wrong("Token Authentication", "one factor (something you have) unless combined with password.")},
         "MFA = 2+ factors; examples: password + SMS OTP, password + fingerprint.")

    _reg(90,
         "Regular security patches fix known vulnerabilities (CVEs) — critical mitigation. "
         "Ignoring feedback, increasing complexity, disabling encryption worsen security posture.",
         {"A": _wrong("Ignoring user feedback", "bad practice — doesn't mitigate vulnerabilities."),
          "B": _right("Applying regular security patches", "closes known exploits — essential hygiene."),
          "C": _wrong("Increasing code complexity", "more complexity often means more attack surface."),
          "D": _wrong("Disabling encryption", "removes confidentiality protection — dangerous.")},
         "Patch management: test patches, deploy promptly, monitor CVE advisories.")

    _build_bank_part4()


def _build_bank_part4() -> None:
    _reg(91,
         "Intelligent agent (Russell & Norvig): entity that perceives environment through sensors "
         "and acts through actuators to achieve goals — foundational AI concept.",
         {"A": _wrong("A program that writes code", "code generation tool — not agent definition."),
          "B": _right("A system that perceives and acts in an environment", "canonical agent definition."),
          "C": _wrong("A database management system", "stores data — no perception/action loop."),
          "D": _wrong("A user interface", "UI presents information — agent includes reasoning/action.")},
         "Agent = Perceive + Act + (optional) Learn in Environment.")

    _reg(92,
         "Breadth-First Search (BFS) explores all nodes at depth d before depth d+1 — "
         "level-order, uses queue. DFS goes deep first (stack); A*/Greedy use heuristics.",
         {"A": _wrong("Depth-First Search", "explores one branch deeply before backtracking — not level-by-level."),
          "B": _right("Breadth-First Search", "expands shallowest nodes first — current depth before deeper."),
          "C": _wrong("A* Search", "informed best-first with f(n)=g(n)+h(n) — not strictly level-order."),
          "D": _wrong("Greedy Search", "uses heuristic only — may not explore all nodes at current depth.")},
         "BFS = queue, level-order; DFS = stack, depth-first; BFS finds shortest path unweighted.")

    _reg(93,
         "Expert system knowledge base stores domain facts and IF-THEN rules for inference engine "
         "to reason and explain decisions — distinct from user data storage.",
         {"A": _wrong("To store user data", "user profiles are application data — not knowledge base purpose."),
          "B": _right("To store rules and facts for decision-making", "domain knowledge + production rules."),
          "C": _wrong("To manage hardware resources", "OS responsibility — not expert system KB."),
          "D": _wrong("To execute search algorithms", "inference engine uses KB; KB is data, not algorithm executor.")},
         "Expert system: Knowledge Base + Inference Engine + Explanation facility.")

    _reg(94,
         "Expert systems use rule-based reasoning (if-then production rules) mimicking human expert "
         "decision-making in narrow domains. ML learns from data; neural nets use weights; GA evolves solutions.",
         {"A": _wrong("Machine Learning", "learns patterns from data — not primarily explicit if-then rules."),
          "B": _right("Expert Systems", "rule-based symbolic AI with knowledge base."),
          "C": _wrong("Neural Networks", "connectionist learning — weighted nodes, not explicit rule bases."),
          "D": _wrong("Genetic Algorithms", "evolutionary optimization — not if-then expert reasoning.")},
         "Symbolic AI (expert systems) vs Subsymbolic (neural networks, deep learning).")

    _reg(95,
         "Lifelong/continual learning enables AI systems to adapt incrementally to new data/tasks "
         "without catastrophic forgetting — supports evolving environments.",
         {"A": _wrong("Reduced system performance", "goal is maintain/improve performance on new data."),
          "B": _right("Continuous adaptation to new data", "learn over time as environment changes."),
          "C": _wrong("Increased code complexity", "possible side effect but not the benefit being tested."),
          "D": _wrong("Limited application scope", "lifelong learning expands applicability — opposite.")},
         "Lifelong learning: adapt without retraining from scratch on all historical data.")

    _reg(96,
         "Supervised learning trains on labeled examples (input-output pairs). "
         "Unsupervised finds structure in unlabeled data (clustering, dimensionality reduction).",
         {"A": _right("Supervised learning uses labeled data, unsupervised does not", "fundamental ML taxonomy."),
          "B": _wrong("Unsupervised learning uses labeled data, supervised does not", "reversed — incorrect."),
          "C": _wrong("Supervised learning is faster than unsupervised", "speed depends on algorithm/data — not defining difference."),
          "D": _wrong("Unsupervised learning requires more data", "data requirements vary — not the core distinction.")},
         "Labeled → Supervised (classification/regression); Unlabeled → Unsupervised (clustering).")

    _reg(97,
         "Decision Trees classify by splitting features on thresholds — interpretable classification algorithm. "
         "K-Means clusters unlabeled data; Linear Regression predicts continuous values; PCA reduces dimensions.",
         {"A": _wrong("K-Means Clustering", "unsupervised clustering — not classification of labeled categories."),
          "B": _wrong("Linear Regression", "predicts continuous numeric output — regression, not classification."),
          "C": _right("Decision Trees", "widely used for classification (also regression trees exist)."),
          "D": _wrong("Principal Component Analysis", "unsupervised dimensionality reduction technique.")},
         "Classification: Decision Trees, SVM, k-NN; Clustering: K-Means; Regression: Linear Regression.")

    _reg(98,
         "Overfitting: model learns training data too closely including noise — high training accuracy "
         "but poor generalization on new test data. Underfitting is too simple; good generalization is goal.",
         {"A": _wrong("When a model performs well on new data", "that describes good generalization — opposite of overfitting."),
          "B": _right("When a model is too complex and fits noise in the training data", "overfitting definition."),
          "C": _wrong("When a model is too simple", "underfitting — high bias, can't capture pattern."),
          "D": _wrong("When a model fails to train", "training failure/error — different from overfitting.")},
         "Fight overfitting: regularization, dropout, more data, cross-validation, simpler model.")

    _reg(99,
         "Predicting house prices from labeled features (size, location) is supervised regression — "
         "learns mapping from inputs to known price outputs. Clustering/dimensionality reduction are unsupervised.",
         {"A": _wrong("Clustering customer data", "unsupervised grouping without predefined labels."),
          "B": _right("Predicting house prices based on features", "supervised learning with labeled price targets."),
          "C": _wrong("Reducing data dimensions", "unsupervised (PCA) or feature engineering — not supervised task label."),
          "D": _wrong("Finding patterns in unlabeled data", "unsupervised learning definition.")},
         "Supervised = labeled targets; Unsupervised = no labels.")

    _reg(100,
         "Training dataset teaches model parameters by presenting labeled/unlabeled examples "
         "for learning patterns. Test set evaluates generalization; validation tunes hyperparameters.",
         {"A": _wrong("To test the model's performance", "test/validation sets evaluate — training set teaches."),
          "B": _right("To train the model to learn patterns", "model fits parameters on training data."),
          "C": _wrong("To validate the model", "validation set used during development for hyperparameter tuning."),
          "D": _wrong("To deploy the model", "deployment puts trained model in production — post-training.")},
         "Train → learn; Validation → tune; Test → final unbiased evaluation.")


def _fallback_entry(q: dict) -> dict[str, Any]:
    """Generate explanation when handcrafted entry missing."""
    from generic_deep_builder import build_deep_entry
    return build_deep_entry(q)


def build_deep_entry(q: dict) -> dict[str, Any]:
    n = q["examNumber"]
    correct = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}

    if n not in BANK:
        _build_bank()
    base = BANK.get(n)
    if not base:
        return _fallback_entry(q)

    options_out = {}
    for key in "ABCD":
        text = opts.get(key, "")
        body = base["options"].get(key, "")
        options_out[key] = _opt(correct, key, text, body)

    return {
        "overview": base["overview"],
        "options": options_out,
        "studyTip": base["studyTip"],
    }


def main() -> None:
    _build_bank()
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for q in data["questions"]:
        num = str(q["examNumber"])
        out[num] = build_deep_entry(q)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} deep explanations -> {OUT_PATH}")
    missing = [i for i in range(1, 101) if i not in BANK]
    if missing:
        print(f"Warning: missing handcrafted entries for: {missing}")


if __name__ == "__main__":
    main()
