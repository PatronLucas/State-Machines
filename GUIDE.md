# State Machines Tutorial - Complete Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Course Structure](#course-structure)
3. [Installation & Setup](#installation--setup)
4. [Lessons](#lessons)
5. [Interactive Demos](#interactive-demos)
6. [Core Concepts](#core-concepts)
7. [Exercises](#exercises)

## Introduction

This repository provides a comprehensive, code-based approach to learning state machine theory, based on MIT's 6.1200J Mathematics for Computer Science course (Lecture 04: State Machines).

### What You'll Learn

- **Fundamentals**: States, transitions, executions, and reachability
- **The Invariant Principle**: Using mathematical induction to prove properties
- **Termination Proofs**: Using potential functions to prove algorithms terminate
- **Classic Problems**: The 8-Puzzle impossibility proof and simple sort algorithm

## Course Structure

### Lesson 1: Introduction to State Machines
**File**: `lessons/lesson1_introduction.py`

**Topics Covered**:
- What is a state machine?
- Deterministic vs non-deterministic machines
- States, transitions, and executions
- Reachability
- Final states and cycles

**Key Examples**:
- Simple Counter (deterministic)
- Coin Flip (non-deterministic)
- Traffic Light (cycles)

**Run it**:
```bash
python lessons/lesson1_introduction.py
```

---

### Lesson 2: The 8-Puzzle Problem
**File**: `lessons/lesson2_eight_puzzle.py`

**Topics Covered**:
- The 8-puzzle problem
- Counting inversions
- The Invariant Principle
- Proving unreachability

**Key Concepts**:
- **Inversion**: A pair (i, j) where i < j but a[i] > a[j]
- **Invariant**: A property preserved by all transitions
- **Impossibility Proof**: Using parity of inversions

**The Classic Puzzle**:
```
Initial:          Target:
1 2 3            1 2 3
4 5 6            4 5 6
8 7 *            7 8 *

Question: Can we reach the target?
Answer: NO! Different inversion parities.
```

**Run it**:
```bash
python lessons/lesson2_eight_puzzle.py
```

---

### Lesson 3: Simple Sort & Termination
**File**: `lessons/lesson3_simple_sort.py`

**Topics Covered**:
- Simple sorting algorithm
- Potential functions (derived variables)
- Proving termination
- Partial correctness

**Algorithm**:
```python
While there exists i where a[i] > a[i+1]:
    Swap a[i] and a[i+1]
```

**Termination Proof**:
- Potential function: f(state) = number of inversions
- Each swap decreases inversions by exactly 1
- Natural numbers can't decrease forever
- Therefore: algorithm terminates!

**Run it**:
```bash
python lessons/lesson3_simple_sort.py
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/PatronLucas/State-Machines.git
cd State-Machines

# Install required packages
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test that everything works
python lessons/lesson1_introduction.py
```

## Interactive Demos

### 8-Puzzle Visualizer
**File**: `demos/eight_puzzle_app.py`

An interactive Streamlit app to:
- Visualize puzzle states
- Try different configurations
- See inversions calculated in real-time
- Understand why some puzzles are impossible

**Run it**:
```bash
streamlit run demos/eight_puzzle_app.py
```

**Features**:
- Interactive puzzle board
- Real-time inversion counting
- Solvability checker
- Educational explanations

---

### Simple Sort Visualizer
**File**: `demos/simple_sort_app.py`

An interactive Streamlit app to:
- Watch the sorting algorithm step-by-step
- Visualize the potential function decreasing
- Understand termination proofs

**Run it**:
```bash
streamlit run demos/simple_sort_app.py
```

**Features**:
- Bar chart visualization
- Potential function graph
- Step-by-step execution
- Auto-run mode

## Core Concepts

### 1. State Machine Definition

A state machine consists of:
1. **States**: A collection of possible configurations
2. **Initial State**: The starting configuration
3. **Transitions**: Rules for moving between states
4. **Execution**: A sequence of states following the transition rules

### 2. Types of State Machines

**Deterministic**:
- Each state has at most one transition
- Example: Simple counter (0 → 1 → 2 → 3 → ...)

**Non-deterministic**:
- States can have multiple possible transitions
- Example: Coin flips (can go heads OR tails)

### 3. Reachability

**Definition**: A state is **reachable** if there exists an execution that reaches it from the initial state.

**Key Question**: How do we prove a state is NOT reachable?

**Answer**: Use the Invariant Principle!

### 4. The Invariant Principle

**Theorem**: If a property P:
1. Holds for the initial state, AND
2. Is preserved by all transitions (if P(s) then P(t) for all s → t)

Then P is an **invariant** (true for all reachable states).

**Corollary**: If P is an invariant and P(target) is false, then target is unreachable!

**Example** (8-Puzzle):
- P(state) = "state has odd number of inversions"
- Initial state: 1 inversion (odd) ✓
- All moves preserve parity ✓
- Target state: 0 inversions (even) ✗
- Therefore: target is UNREACHABLE!

### 5. Termination via Potential Functions

**Definition**: A **potential function** is a function f mapping states to real numbers.

**Theorem**: If f:
1. Maps to natural numbers (0, 1, 2, ...), AND
2. Is strictly decreasing (f(t) < f(s) for all s → t)

Then the state machine **terminates** (reaches a final state).

**Proof Idea**: Natural numbers can't decrease forever!

**Example** (Simple Sort):
- f(state) = number of inversions
- Each swap reduces inversions by 1
- f is natural-number valued and strictly decreasing
- Therefore: algorithm terminates!

## Exercises

### Exercise 1: Create Your Own State Machine

Create a state machine for a vending machine that:
- Starts with $0
- Can accept quarters ($0.25)
- Dispenses item when $1.00 is reached

```python
from src.state_machine import StateMachine

class VendingMachine(StateMachine):
    def get_initial_state(self):
        return 0.00  # Start with $0
    
    def get_transitions(self, state):
        if state < 1.00:
            return [state + 0.25]  # Insert quarter
        return []  # Dispense item (final state)

# Try it!
vm = VendingMachine()
print(vm.is_reachable(1.00))  # True
print(vm.find_path(1.00))  # [0.0, 0.25, 0.5, 0.75, 1.0]
```

### Exercise 2: Find an Invariant

For the 8-puzzle, we used inversion parity. Can you think of other invariants?

Hint: Think about the sum of all numbers, or the position of specific tiles.

### Exercise 3: Design a Potential Function

Consider a state machine where states are strings and transitions remove one character at a time.

Design a potential function to prove it terminates.

```python
class StringShortener(StateMachine):
    def __init__(self, initial_string):
        self.initial_string = initial_string
        super().__init__()
    
    def get_initial_state(self):
        return self.initial_string
    
    def get_transitions(self, state):
        if len(state) > 0:
            # Can remove any character
            return [state[:i] + state[i+1:] for i in range(len(state))]
        return []

# What's a good potential function?
# Answer: f(state) = len(state)
```

## Tips for Success

1. **Start with Lesson 1**: Build a strong foundation
2. **Run the Code**: Don't just read—execute and experiment!
3. **Use the Interactive Demos**: Visual learning is powerful
4. **Try the Exercises**: Practice makes perfect
5. **Modify Examples**: Change parameters and see what happens

## Additional Resources

### From the Lectures
- MIT 6.1200J/18.062J Mathematics for Computer Science
- Lecture 04: State Machines
- Spring 2024

### Further Reading
- State machines in compiler design
- Finite automata theory
- Model checking and formal verification

## Common Pitfalls

### Pitfall 1: Confusing Reachability with Possibility
Just because a state "looks" achievable doesn't mean it's reachable!
The 8-puzzle teaches us this lesson.

### Pitfall 2: Forgetting to Check Initial State
An invariant must hold for the initial state AND be preserved.
Both conditions are necessary!

### Pitfall 3: Weakly vs Strictly Decreasing
For termination, the potential function must be **strictly** decreasing.
Weakly decreasing isn't enough (could cycle forever at same value).

## Troubleshooting

### ImportError
```bash
# Make sure you're in the right directory
cd State-Machines

# And install dependencies
pip install -r requirements.txt
```

### Streamlit Not Working
```bash
# Reinstall streamlit
pip install --upgrade streamlit

# Run with full path
python -m streamlit run demos/eight_puzzle_app.py
```

## Contributing

This is an educational project. Feel free to:
- Add more examples
- Create new visualizations
- Suggest improvements
- Report issues

## Acknowledgments

Based on MIT OpenCourseWare:
- Course: 6.1200J / 18.062J Mathematics for Computer Science
- Instructors: Z. Abel, B. Chapman, E. Demaine
- Spring 2024

## License

See LICENSE file for details.

---

**Happy Learning! **

Remember: *"The only way to learn mathematics is to do mathematics."* - Paul Halmos
