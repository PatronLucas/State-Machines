# State Machines Educational Repository - Project Summary

## Overview

This repository provides a comprehensive, code-based approach to learning state machine theory, based on MIT's 6.1200J Mathematics for Computer Science course (Lecture 04: State Machines).

## Repository Structure

```
State-Machines/
├── src/                          # Core framework
│   ├── state_machine.py         # Base classes and utilities
│   └── visualize.py             # Visualization utilities
├── lessons/                      # Educational lessons (Python scripts)
│   ├── lesson1_introduction.py  # Basics, deterministic vs non-deterministic
│   ├── lesson2_eight_puzzle.py  # Invariant principle
│   └── lesson3_simple_sort.py   # Termination proofs
├── demos/                        # Interactive Streamlit apps
│   ├── eight_puzzle_app.py      # Interactive 8-puzzle visualizer
│   └── simple_sort_app.py       # Sorting algorithm visualizer
├── examples/                     # Custom implementations
│   └── custom_state_machines.py # Door lock, bank account, etc.
├── test_all.py                   # Comprehensive test suite
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
├── GUIDE.md                      # Complete tutorial guide
└── QUICKSTART.md                 # Quick start guide
```

## Key Features

### 1. Core Framework (`src/state_machine.py`)

**StateMachine** (Abstract Base Class)
- `get_initial_state()`: Returns initial state
- `get_transitions(state)`: Returns possible next states
- `is_reachable(target)`: BFS to check reachability
- `find_path(target)`: Finds path to target state

**Invariant**
- Represents preserved predicates
- Verifies invariant principle
- Used to prove unreachability

**PotentialFunction**
- Maps states to real numbers
- Checks if strictly/weakly decreasing
- Used to prove termination

### 2. Educational Lessons

#### Lesson 1: Introduction
- Simple Counter (deterministic)
- Coin Flip (non-deterministic)
- Traffic Light (cycles)
- Reachability concepts

#### Lesson 2: The 8-Puzzle
- The classic impossibility proof
- Inversion counting
- Invariant principle demonstration
- Horizontal vs vertical move analysis

#### Lesson 3: Simple Sort
- Algorithm description
- Potential function (inversions)
- Termination proof
- Partial correctness

### 3. Interactive Demos

#### 8-Puzzle Visualizer (Streamlit)
- Visual puzzle representation
- Real-time inversion counting
- Solvability checker
- Educational explanations

#### Simple Sort Visualizer (Streamlit)
- Bar chart visualization
- Potential function graph
- Step-by-step execution
- Auto-run mode

### 4. Examples

Custom state machine implementations:
- **Door Lock**: Sequential with reset
- **Bank Account**: Constraints and invariants
- **Palindrome Builder**: String constraints

## How to Use

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run a lesson
python lessons/lesson1_introduction.py

# Launch interactive demo
streamlit run demos/eight_puzzle_app.py

# Run examples
python examples/custom_state_machines.py

# Run tests
python test_all.py
```

### Learning Path

1. Read `QUICKSTART.md` (5 minutes)
2. Run Lesson 1 (10 minutes)
3. Run Lesson 2 (15 minutes)
4. Run Lesson 3 (15 minutes)
5. Try interactive demos (20 minutes)
6. Explore examples (10 minutes)
7. Create your own state machine!

## Core Concepts Taught

### The Invariant Principle

**Theorem**: If property P:
1. Holds for initial state, AND
2. Is preserved by all transitions

Then P is an invariant (true for all reachable states).

**Application**: Prove state unreachable by finding invariant it violates.

**Example**: 8-Puzzle uses inversion parity as invariant.

### Termination via Potential Functions

**Theorem**: If potential function f:
1. Maps to natural numbers, AND
2. Is strictly decreasing

Then state machine terminates.

**Application**: Prove algorithm terminates.

**Example**: Simple sort uses inversion count as potential function.

## Key Educational Benefits

1. **Learn by Doing**: All concepts demonstrated with working code
2. **Visual Learning**: Interactive demos for visual understanding
3. **Progressive Complexity**: From simple examples to classic problems
4. **Mathematical Rigor**: Formal proofs implemented in code
5. **Practical Applications**: Real-world examples beyond theory

## Testing

Comprehensive test suite (`test_all.py`) verifies:
- All modules import correctly
- Core framework functions properly
- Lessons work as expected
- Examples run without errors

All tests pass with no security vulnerabilities.

## Technologies Used

- **Python 3.8+**: Core language
- **NumPy**: Numerical operations
- **Matplotlib**: Static visualizations
- **Plotly**: Interactive charts
- **Streamlit**: Web-based interactive demos
- **Jupyter**: Notebook support (planned)

## Based On

MIT OpenCourseWare
- Course: 6.1200J / 18.062J Mathematics for Computer Science
- Lecture 04: State Machines
- Instructors: Z. Abel, B. Chapman, E. Demaine
- Spring 2024

## License

See LICENSE file for details.

## Future Enhancements (Potential)

- [ ] Jupyter notebooks for each lesson
- [ ] Additional state machine examples
- [ ] Graph visualization of state spaces
- [ ] Manim animations for concepts
- [ ] More interactive demos
- [ ] Exercise problems with solutions

---

**Project Status**: Complete and Ready for Use

All planned features implemented, tested, and documented.
