"""Complete answer key for BDU Model Exit Exam (examNumber 1-99)."""

# Derived from CS/SE curriculum, cross-exam matching, and OCR question review.
ANSWERS: dict[int, str] = {
    1: "B",   # Big-Oh worst case
    2: "D",   # Binary search O(log n)
    3: "B",   # O(n^2) dominant term
    4: "B",   # O(n) append at end with head-only pointer
    5: "C",   # Circular linked list
    6: "A",   # new operator
    7: "A",   # Stack for recursion
    8: "A",   # Tree hierarchical
    9: "B",   # valid identifier (not keyword int)
    10: "D",  # output question — partial OCR
    11: "B",  # reference parameter 25
    12: "B",  # sum(num1, num2) function call
    13: "D",  # All true about arrays
    14: "C",  # arrayname[index] access
    15: "A",  # Runtime polymorphism via virtual functions
    16: "A",  # Incorrect: constructor having return type
    17: "B",  # Superclass changes affect subclasses
    18: "B",  # Wrong interface vs abstract class statement
    19: "A",  # Overloading unique among binding types
    20: "B",  # OCR damaged page — placeholder
    21: "A",  # CSS body {color: black}
    22: "A",  # PHP is NOT client-side like JS (false statement question)
    23: "D",  # Hypertext link
    24: "C",  # Web server
    25: "C",  # <strong> bold
    26: "D",  # RESET input clears form
    27: "D",  # JS multi-line comment /* */
    28: "A",  # Service lifecycle onCreate/onStartCommand/onDestroy
    29: "B",  # /res/layout
    30: "D",  # ViewGroup superclass
    31: "A",  # Manifest.xml application info
    32: "C",  # onClick handler
    33: "C",  # Linux kernel
    34: "B",  # Non-recoverable schedule
    35: "A",  # None — all listed factors affect join performance
    36: "A",  # False: linear search more efficient on ordered file
    37: "C",  # Shrinking phase
    38: "C",  # Dirty read
    39: "B",  # Deferred modification
    40: "D",  # /29 subnet mask
    41: "C",  # OCR damaged — placeholder
    42: "B",  # Threat = potential danger
    43: "B",  # Pattern matching (AI/knowledge)
    44: "D",  # Reference model
    45: "A",  # AI definition — All of the above
    46: "C",  # Initiation phase — OCR damaged stem
    47: "C",  # Boundary value → Black box
    48: "D",  # Scalability NFR
    49: "A",  # Presentation layer encryption
    50: "D",  # DoS affects availability
    51: "C",  # WBS contains work packages
    52: "C",  # Smoke testing
    53: "B",  # Escape queries prevent SQL injection
    54: "B",  # IPv6 128 bits
    55: "A",  # Memento pattern for undo
    56: "C",  # Big Data velocity = speed of data
    57: "B",  # MVC model stores program state
    58: "B",  # Escape user input prevents XSS
    59: "C",  # Biometric authentication
    60: "C",  # Data mining predicts trends
    61: "C",  # Informed search explores promising first
    62: "C",  # SRS avoids implementation algorithms
    63: "B",  # Vulnerability
    64: "A",  # PERT = Review Technique
    65: "B",  # Multiplexing
    66: "B",  # TDMA channel partitioning
    67: "B",  # Rapid Application Development
    68: "C",  # Decision coverage formula
    69: "B",  # NoSQL unstructured data
    70: "A",  # Test planning → determine approach
    71: "D",  # Research-oriented → technology problems
    72: "C",  # State attribute value
    73: "B",  # Composition relationship
    74: "D",  # Interface design model
    75: "B",  # Most complex agent environment
    76: "B",  # Equivalence partitioning black box all levels
    77: "D",  # Project planning after feasibility
    78: "C",  # All Big Data benefits
    79: "A",  # All relate to evolutionary model (trick question)
    80: "A",  # SQL Server is not NoSQL
    81: "D",  # Use case not structural diagram
    82: "B",  # Should NOT specify qualitatively only
    83: "A",  # Test cases count is not coverage metric
    84: "D",  # Function-related metrics
    85: "B",  # Incorrect agile: contract over collaboration
    86: "D",  # Testing evaluates deliverables for errors
    87: "A",  # Transport layer process addressing (ports)
    88: "B",  # Data warehouse definition
    89: "C",  # Client-server odd among module structures
    90: "A",  # Greedy/informed minimizes cost (best available option)
    91: "B",  # Knowledge representation storage format
    92: "A",  # Data flow testing white box
    93: "C",  # Backward to requirements traceability
    94: "D",  # void pthread_exit(void *retval)
    95: "D",  # ssize_t not standard primitive in same sense
    96: "A",  # lseek signature
    97: "B",  # close returns -1 not NULL on error
    98: "B",  # times struct field typo not true
    99: "B",  # exit(main(...)) startup pattern
}
