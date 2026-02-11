# Quick Start Guide

Welcome to the State Machines repository! This guide will help you get started quickly.

## What You'll Find Here

This repository contains a comprehensive implementation of state machines based on **MIT OCW 6.1200J Mathematics for Computer Science - Lecture 4**.

## Quick Start (30 seconds)

```bash
# Clone the repository
git clone https://github.com/PatronLucas/State-Machines.git
cd State-Machines

# Run the interactive demo
python3 demo.py

# Run the examples
python3 examples.py

# Run the tests
python3 -m unittest test_state_machines.py
```

## Your First State Machine (2 minutes)

Create a file called `my_first_machine.py`:

```python
from state_machine import StateMachine

# Create a traffic light state machine
states = {'RED', 'YELLOW', 'GREEN'}
initial_state = 'RED'

transitions = {
    ('RED', 'next'): 'GREEN',
    ('GREEN', 'next'): 'YELLOW',
    ('YELLOW', 'next'): 'RED',
}

traffic_light = StateMachine(states, initial_state, transitions)

# Use it
print(f"Current: {traffic_light.current_state}")  # RED
traffic_light.transition('next')
print(f"Current: {traffic_light.current_state}")  # GREEN
traffic_light.transition('next')
print(f"Current: {traffic_light.current_state}")  # YELLOW
```

Run it:
```bash
python3 my_first_machine.py
```

## Learn More (5 minutes)

### 1. Check out the examples

```bash
python3 examples.py
```

This shows you:
- **Turnstile**: Classic locked/unlocked example
- **Binary Divisibility**: Check if binary numbers are divisible by 3
- **Even Ones Counter**: Count parity of 1s in binary strings
- **Modulo Counter**: Count events modulo n

### 2. Run the interactive demo

```bash
python3 demo.py
```

This provides:
- Visual state diagrams
- Step-by-step execution traces
- Multiple scenarios for each example

### 3. Read the documentation

- **README.md**: Full usage guide
- **THEORY.md**: Mathematical foundations and theory

## Common Use Cases

### Pattern Matching
```python
# Detect the sequence "101"
from examples import create_sequence_detector

detector = create_sequence_detector("101")
print(detector.accepts("101"))  # True
```

### Parity Checking
```python
# Check for even number of 1s
from examples import create_even_ones_counter

checker = create_even_ones_counter()
print(checker.accepts("1111"))  # True (4 ones)
print(checker.accepts("111"))   # False (3 ones)
```

### Modular Arithmetic
```python
# Count modulo 5
from examples import create_mod_counter

counter = create_mod_counter(5)
for i in range(7):
    counter.transition('tick')
print(counter.current_state)  # S2 (7 mod 5 = 2)
```

## File Structure

```
State-Machines/
├── state_machine.py          # Core implementation
├── examples.py               # Example state machines
├── demo.py                   # Interactive demonstration
├── test_state_machines.py    # Test suite
├── README.md                 # Full documentation
├── THEORY.md                 # Mathematical theory
└── QUICKSTART.md            # This file
```

## Next Steps

1. **Try the examples**: Run `python3 examples.py`
2. **Create your own**: Build a state machine for your use case
3. **Read the theory**: Check out `THEORY.md` for deeper understanding
4. **Explore the tests**: See `test_state_machines.py` for more examples

## Need Help?

- Check the comprehensive examples in `examples.py`
- Read the theory in `THEORY.md`
- Look at the tests in `test_state_machines.py` for usage patterns
- Review the MIT OCW lecture materials (referenced in the documentation)

## Contributing

Feel free to:
- Add more examples
- Improve documentation
- Add new features
- Fix bugs

This is an educational repository - contributions are welcome!

---

Happy learning! 🎓
