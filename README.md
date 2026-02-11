# State Machines: An Interactive Learning Journey

An educational repository that teaches state machine theory through Python code, based on MIT's 6.1200J Mathematics for Computer Science course.

## Overview

This repository provides a comprehensive, code-based approach to understanding state machines, including:

- **Core Concepts**: States, transitions, executions, reachability
- **The Invariant Principle**: Proving properties using mathematical induction
- **Termination Proofs**: Using potential functions to prove algorithms terminate
- **Classic Problems**: The 8-Puzzle, Simple Sort, and more

## Course Structure

### **Lesson 1: Introduction to State Machines** (`lessons/lesson1_introduction.py`)
Learn the fundamentals through interactive examples:
- What is a state machine?
- Deterministic vs non-deterministic machines
- Reachability and executions
- Final states and cycles

**Run it:**
```bash
python lessons/lesson1_introduction.py
```

### **Lesson 2: The 8-Puzzle Problem** (`lessons/lesson2_eight_puzzle.py`)
Explore the famous 8-puzzle and learn how to prove impossibility:
- Implementing the 8-puzzle as a state machine
- Understanding inversions
- The Invariant Principle
- Proving certain configurations are unreachable

**Run it:**
```bash
python lessons/lesson2_eight_puzzle.py
```

### **Lesson 3: Simple Sort & Termination** (`lessons/lesson3_simple_sort.py`)
Understand how to prove algorithms terminate:
- Simple sorting algorithm
- Potential functions (derived variables)
- Proving termination
- Partial correctness

**Run it:**
```bash
python lessons/lesson3_simple_sort.py
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/PatronLucas/State-Machines.git
cd State-Machines
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run a lesson:
```bash
python lessons/lesson1_introduction.py
```

## Project Structure

```
State-Machines/
├── src/                          # Core state machine framework
│   ├── __init__.py
│   ├── state_machine.py         # Base classes and utilities
│   └── visualize.py             # Visualization utilities
├── lessons/                      # Educational lessons
│   ├── lesson1_introduction.py  # State machine basics
│   ├── lesson2_eight_puzzle.py  # The 8-Puzzle problem
│   └── lesson3_simple_sort.py   # Termination proofs
├── demos/                        # Interactive Streamlit apps
│   ├── eight_puzzle_app.py      # 8-Puzzle visualizer
│   └── simple_sort_app.py       # Simple sort visualizer
├── examples/                     # Example implementations
│   └── custom_state_machines.py # Custom state machine examples
├── notebooks/                    # Jupyter notebooks (coming soon)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── GUIDE.md                      # Complete tutorial guide
└── QUICKSTART.md                 # Quick start guide
```

## Core Framework

The `src/state_machine.py` module provides:

### `StateMachine` (Abstract Base Class)
```python
class StateMachine(ABC):
    def get_initial_state(self) -> Any
    def get_transitions(self, state) -> List[Any]
    def is_reachable(self, target_state) -> bool
    def find_path(self, target_state) -> Optional[List[Any]]
```

### `Invariant`
```python
class Invariant:
    def holds(self, state) -> bool
    def verify_preserved(self, state_machine, state) -> bool
```

### `PotentialFunction`
```python
class PotentialFunction:
    def evaluate(self, state) -> float
    def is_strictly_decreasing(self, state_machine, state) -> bool
```

## Key Concepts

### The Invariant Principle

**Definition**: If a property P:
1. Holds for the initial state, and
2. Is preserved by all transitions

Then P is an **invariant** (true for all reachable states).

**Application**: Prove a state is unreachable by finding an invariant it violates.

### The 8-Puzzle Impossibility

The 8-puzzle configuration:
```
1 2 3
4 5 6
8 7 *
```

Cannot reach:
```
1 2 3
4 5 6
7 8 *
```

**Proof**: The parity of inversions is an invariant!
- Initial: 1 inversion (odd)
- Target: 0 inversions (even)
- Therefore: IMPOSSIBLE!

### Termination via Potential Functions

**Theorem**: If a potential function with natural number values is strictly decreasing, the state machine terminates.

**Example**: Simple Sort
- Potential function: number of inversions
- Each swap reduces inversions by exactly 1
- Must reach 0 inversions (sorted state)
- Therefore: algorithm terminates!

## Creating Your Own State Machine

```python
from src.state_machine import StateMachine

class MyMachine(StateMachine):
    def get_initial_state(self):
        return "start"
    
    def get_transitions(self, state):
        if state == "start":
            return ["middle"]
        elif state == "middle":
            return ["end"]
        return []

# Use it
machine = MyMachine()
print(machine.is_reachable("end"))  # True
```

## Learning Path

1. **Read QUICKSTART.md**: Get set up in 5 minutes
2. **Start with Lesson 1**: Understand the basics
3. **Move to Lesson 2**: See invariants in action
4. **Complete Lesson 3**: Master termination proofs
5. **Try Interactive Demos**: Visualize the concepts
6. **Explore Examples**: See more use cases
7. **Experiment**: Create your own state machines!

## Interactive Demos

### 8-Puzzle Visualizer
```bash
streamlit run demos/eight_puzzle_app.py
```

### Simple Sort Visualizer
```bash
streamlit run demos/simple_sort_app.py
```

## Examples

See `examples/custom_state_machines.py` for:
- Door Lock state machine
- Bank Account model
- Palindrome Builder

Run all examples:
```bash
python examples/custom_state_machines.py
```

## Applications

State machines are everywhere in computer science:
- **Algorithms**: Sorting, searching, graph traversal
- **Formal Verification**: Proving correctness
- **Compilers**: Lexical analysis, parsing
- **Networks**: Protocol design
- **Games**: AI, game states
- **Hardware**: Digital circuit design

## Based on MIT Course Material

This repository is based on Lecture 04 from:
- **Course**: 6.1200J / 18.062J Mathematics for Computer Science
- **Institution**: Massachusetts Institute of Technology
- **Semester**: Spring 2024
- **Instructors**: Z. Abel, B. Chapman, E. Demaine

Original lecture notes available at [MIT OpenCourseWare](https://ocw.mit.edu).

## Contributing

This is an educational project. Feel free to:
- Add more examples
- Create visualizations
- Suggest improvements
- Report issues

## License

See [LICENSE](LICENSE) file for details.

## Acknowledgments

- MIT OpenCourseWare for the excellent course material
- The instructors of 6.1200J for making these concepts accessible
- The Python community for amazing tools and libraries

---

**Happy Learning!**

*"The only way to learn mathematics is to do mathematics." - Paul Halmos*
