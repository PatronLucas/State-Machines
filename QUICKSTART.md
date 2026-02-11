# Quick Start Guide

Get started with State Machines in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run Your First Lesson

```bash
python lessons/lesson1_introduction.py
```

You should see output explaining state machine basics with examples.

## 3. Try the Interactive Demo

```bash
streamlit run demos/eight_puzzle_app.py
```

This will open a web browser with an interactive 8-puzzle visualizer!

## 4. Explore the Code

Open `src/state_machine.py` to see the core framework:

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

# Use it!
machine = MyMachine()
print(machine.is_reachable("end"))  # True
path = machine.find_path("end")
print(path)  # ['start', 'middle', 'end']
```

## 5. Learning Path

Follow these lessons in order:

1. **Lesson 1**: Introduction (`lessons/lesson1_introduction.py`)
   - Basics of state machines
   - ~10 minutes

2. **Lesson 2**: The 8-Puzzle (`lessons/lesson2_eight_puzzle.py`)
   - Invariant principle
   - ~15 minutes

3. **Lesson 3**: Simple Sort (`lessons/lesson3_simple_sort.py`)
   - Termination proofs
   - ~15 minutes

## Next Steps

- Read the complete [GUIDE.md](GUIDE.md) for in-depth explanations
- Try the exercises in each lesson
- Experiment with the interactive demos
- Create your own state machines!

## Need Help?

Check the [README.md](README.md) for:
- Full documentation
- Detailed examples
- Troubleshooting tips

**Happy Learning! 🚀**
