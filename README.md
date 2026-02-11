# State Machines

A comprehensive implementation of state machines for educational purposes, based on concepts from **MIT OCW 6.1200J Mathematics for Computer Science - Lecture 4**.

## Overview

A **state machine** (also called a finite automaton) is a mathematical model of computation consisting of:
- A finite set of **states**
- An **initial state** where the machine starts
- A **transition function** that maps (current_state, input) → next_state
- Optionally, a set of **accepting states** (final states)

State machines are fundamental in computer science and are used in:
- Compiler design (lexical analysis)
- Protocol design (network protocols, communication)
- Hardware design (digital circuits)
- Software engineering (workflow management, UI state)
- Regular expressions and pattern matching

## Installation

No external dependencies required! Just Python 3.x.

```bash
git clone https://github.com/PatronLucas/State-Machines.git
cd State-Machines
```

## Usage

### Basic State Machine

```python
from state_machine import StateMachine

# Create a simple state machine
states = {'A', 'B', 'C'}
initial_state = 'A'
transitions = {
    ('A', 'x'): 'B',
    ('B', 'y'): 'C',
    ('C', 'z'): 'A'
}
accepting_states = {'C'}

sm = StateMachine(states, initial_state, transitions, accepting_states)

# Process inputs
sm.transition('x')  # A -> B
sm.transition('y')  # B -> C
print(sm.is_accepting())  # True

# Process a sequence
sm.reset()
result = sm.accepts(['x', 'y'])  # Returns True (ends in state C)
```

### Example: Turnstile

A classic example of a two-state machine:

```python
from examples import create_turnstile

turnstile = create_turnstile()
print(turnstile.current_state)  # LOCKED

turnstile.transition('coin')    # Insert coin
print(turnstile.current_state)  # UNLOCKED

turnstile.transition('push')    # Push through
print(turnstile.current_state)  # LOCKED
```

**State Diagram:**
```
    +--------+  coin   +-----------+
    | LOCKED | ------> | UNLOCKED  |
    |        | <------ |           |
    +--------+  push   +-----------+
```

### Example: Binary Number Divisibility by 3

This machine recognizes binary numbers divisible by 3:

```python
from examples import create_binary_divisible_by_3

div3 = create_binary_divisible_by_3()

print(div3.accepts('11'))    # True  (3 in decimal)
print(div3.accepts('110'))   # True  (6 in decimal)
print(div3.accepts('1001'))  # True  (9 in decimal)
print(div3.accepts('101'))   # False (5 in decimal)
```

**How it works:** The machine maintains the remainder when the number is divided by 3. States S0, S1, S2 represent remainders 0, 1, 2 respectively.

### Example: Even Number of Ones

Counts the parity of 1s in a binary string:

```python
from examples import create_even_ones_counter

even_ones = create_even_ones_counter()

print(even_ones.accepts('0101'))  # True  (2 ones)
print(even_ones.accepts('1111'))  # True  (4 ones)
print(even_ones.accepts('111'))   # False (3 ones)
```

### Example: Modulo Counter

A counter that keeps track of count modulo n:

```python
from examples import create_mod_counter

mod4 = create_mod_counter(4)

for i in range(5):
    mod4.transition('tick')
    print(f"Count: {i+1}, State: {mod4.current_state}")
```

## Running Examples

```bash
# Run all example demonstrations
python3 examples.py

# Run tests
python3 -m unittest test_state_machines.py -v
```

## File Structure

```
State-Machines/
├── state_machine.py          # Core StateMachine class
├── examples.py               # Classic state machine examples
├── test_state_machines.py    # Comprehensive test suite
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## Theory and Concepts

### State Machine Components

1. **States (Q)**: A finite set of states the machine can be in
2. **Alphabet (Σ)**: A finite set of input symbols
3. **Transition Function (δ)**: Maps Q × Σ → Q
4. **Initial State (q₀)**: The starting state
5. **Accepting States (F)**: Subset of Q where computation successfully terminates

### Formal Definition

A deterministic finite automaton (DFA) is a 5-tuple (Q, Σ, δ, q₀, F) where:
- Q is a finite set of states
- Σ is a finite alphabet
- δ: Q × Σ → Q is the transition function
- q₀ ∈ Q is the initial state
- F ⊆ Q is the set of accepting states

### Applications

**Lexical Analysis**: Tokenizing source code
```python
# Example: Recognizing identifiers vs keywords
# States: START, IDENTIFIER, KEYWORD
```

**Protocol Validation**: Network protocols like TCP
```python
# States: CLOSED, LISTEN, SYN_SENT, ESTABLISHED, etc.
```

**Pattern Matching**: Regular expression matching
```python
# Example: Detecting the pattern "101" in a bit stream
```

## Learning Resources

- **MIT OCW 6.1200J Mathematics for Computer Science**
  - Lecture 4: State Machines
  - Covers formal definitions, examples, and applications

- **Recommended Topics to Explore:**
  - Non-deterministic Finite Automata (NFA)
  - Regular languages and their properties
  - Pumping lemma
  - State machine minimization

## Contributing

This is an educational repository. Feel free to:
- Add more example state machines
- Improve documentation
- Add visualizations
- Extend functionality (e.g., NFA support)

## License

MIT License - See LICENSE file for details

## Author

Lucas Patron

---

*This repository was created for learning purposes only, inspired by MIT's Mathematics for Computer Science course.*
