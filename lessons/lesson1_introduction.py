"""
Lesson 1: Introduction to State Machines

This lesson introduces the fundamental concepts of state machines as described in
MIT's 6.1200J Mathematics for Computer Science course.

Key Concepts:
1. What is a state machine?
2. States, transitions, and executions
3. Deterministic vs non-deterministic state machines
4. Reachability
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state_machine import StateMachine
from typing import List, Tuple


class SimpleCounter(StateMachine):
    """
    A simple counter that counts from 0 to max_value.
    
    This is a basic example of a deterministic state machine.
    """
    
    def __init__(self, max_value: int = 10):
        """
        Initialize a counter.
        
        Args:
            max_value: The maximum value to count to
        """
        self.max_value = max_value
        super().__init__()
    
    def get_initial_state(self) -> int:
        """Initial state is 0."""
        return 0
    
    def get_transitions(self, state: int) -> List[int]:
        """
        From any state n < max_value, we can transition to n+1.
        From max_value, there are no transitions (final state).
        """
        if state < self.max_value:
            return [state + 1]
        return []


class CoinFlip(StateMachine):
    """
    A non-deterministic state machine representing coin flips.
    
    At each state (number of flips), we can transition to two states:
    - Heads count + 1
    - Tails count + 1
    
    States are represented as (heads, tails) tuples.
    """
    
    def __init__(self, max_flips: int = 3):
        """
        Initialize a coin flip state machine.
        
        Args:
            max_flips: Maximum number of flips
        """
        self.max_flips = max_flips
        super().__init__()
    
    def get_initial_state(self) -> Tuple[int, int]:
        """Initial state: no flips yet."""
        return (0, 0)
    
    def get_transitions(self, state: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        From (heads, tails), we can transition to:
        - (heads+1, tails) if we flip heads
        - (heads, tails+1) if we flip tails
        
        Unless we've already made max_flips flips.
        """
        heads, tails = state
        total_flips = heads + tails
        
        if total_flips >= self.max_flips:
            return []  # Final state
        
        return [
            (heads + 1, tails),  # Flip heads
            (heads, tails + 1),  # Flip tails
        ]


def demonstrate_basic_concepts():
    """Demonstrate basic state machine concepts."""
    print("=" * 60)
    print("LESSON 1: INTRODUCTION TO STATE MACHINES")
    print("=" * 60)
    
    print("\n" + "=" * 60)
    print("WHAT IS A STATE MACHINE?")
    print("=" * 60)
    
    print("""
A state machine is a mathematical model consisting of:

1. STATES: A collection of possible configurations
   Example: Numbers 0, 1, 2, 3, 4, 5

2. INITIAL STATE: Where we start
   Example: 0

3. TRANSITIONS: Rules for moving between states
   Example: From n, we can move to n+1

4. EXECUTION: A sequence of states following the rules
   Example: 0 → 1 → 2 → 3 → 4 → 5
""")


def demonstrate_deterministic():
    """Demonstrate a deterministic state machine."""
    print("\n" + "=" * 60)
    print("DETERMINISTIC STATE MACHINE: SIMPLE COUNTER")
    print("=" * 60)
    
    counter = SimpleCounter(max_value=5)
    
    print(f"\nInitial state: {counter.current_state}")
    print("\nExecution:")
    
    step = 0
    while not counter.is_final_state(counter.current_state):
        print(f"  Step {step}: State = {counter.current_state}")
        
        # Get possible transitions
        transitions = counter.get_transitions(counter.current_state)
        print(f"           Possible transitions: {transitions}")
        
        # In a deterministic machine, there's exactly one transition (or none)
        if transitions:
            counter.step(transitions[0])
        
        step += 1
    
    print(f"  Step {step}: State = {counter.current_state} (FINAL)")
    
    print(f"\nComplete execution history: {counter.get_execution()}")
    
    print("\nDETERMINISTIC: At each state, there is exactly ONE possible next state")


def demonstrate_nondeterministic():
    """Demonstrate a non-deterministic state machine."""
    print("\n" + "=" * 60)
    print("NON-DETERMINISTIC STATE MACHINE: COIN FLIPS")
    print("=" * 60)
    
    coin = CoinFlip(max_flips=3)
    
    print(f"\nInitial state: {coin.current_state} (heads, tails)")
    print("\nState space exploration:")
    
    # Explore all possible executions using BFS
    visited = set()
    queue = [(coin.get_initial_state(), [coin.get_initial_state()])]
    all_executions = []
    
    while queue:
        state, path = queue.pop(0)
        
        if state in visited:
            continue
        visited.add(state)
        
        if coin.is_final_state(state):
            all_executions.append(path)
            continue
        
        for next_state in coin.get_transitions(state):
            queue.append((next_state, path + [next_state]))
    
    print(f"\nTotal reachable states: {len(visited)}")
    print(f"Total possible executions: {len(all_executions)}")
    
    print("\nAll possible executions:")
    for i, execution in enumerate(all_executions, 1):
        print(f"  {i}. {' → '.join(str(s) for s in execution)}")
    
    print("\nNON-DETERMINISTIC: At each state, there are MULTIPLE possible next states")


def demonstrate_reachability():
    """Demonstrate the concept of reachability."""
    print("\n" + "=" * 60)
    print("REACHABILITY")
    print("=" * 60)
    
    print("""
A state is REACHABLE if there exists an execution that reaches it.

Key questions:
1. Is state X reachable from the initial state?
2. Can we prove that certain states are NOT reachable?
""")
    
    # Counter example
    counter = SimpleCounter(max_value=5)
    
    print("\nCounter example (max_value=5):")
    print(f"  Is state 3 reachable? {counter.is_reachable(3)}")
    print(f"  Is state 5 reachable? {counter.is_reachable(5)}")
    print(f"  Is state 10 reachable? {counter.is_reachable(10)}")
    
    # Coin flip example
    coin = CoinFlip(max_flips=3)
    
    print("\nCoin flip example (max_flips=3):")
    print(f"  Is state (1, 1) reachable? {coin.is_reachable((1, 1))}")
    print(f"  Is state (2, 1) reachable? {coin.is_reachable((2, 1))}")
    print(f"  Is state (3, 0) reachable? {coin.is_reachable((3, 0))}")
    print(f"  Is state (4, 0) reachable? {coin.is_reachable((4, 0))}")
    print(f"  Is state (2, 2) reachable? {coin.is_reachable((2, 2))}")
    
    # Find paths
    print("\nPath to state (2, 1):")
    path = coin.find_path((2, 1))
    if path:
        print(f"  {' → '.join(str(s) for s in path)}")


class TrafficLight(StateMachine):
    """
    A simple traffic light state machine.
    
    States: Green → Yellow → Red → Green (cycle)
    """
    
    def get_initial_state(self) -> str:
        return "Green"
    
    def get_transitions(self, state: str) -> List[str]:
        transitions = {
            "Green": ["Yellow"],
            "Yellow": ["Red"],
            "Red": ["Green"]
        }
        return transitions.get(state, [])


def demonstrate_cycles():
    """Demonstrate state machines with cycles."""
    print("\n" + "=" * 60)
    print("STATE MACHINES WITH CYCLES")
    print("=" * 60)
    
    traffic = TrafficLight()
    
    print("\nTraffic light state machine:")
    print("  Green → Yellow → Red → Green → ...")
    
    print("\nExecution (10 steps):")
    for i in range(10):
        print(f"  Step {i}: {traffic.current_state}")
        transitions = traffic.get_transitions(traffic.current_state)
        if transitions:
            traffic.step(transitions[0])
    
    print("\nThis state machine has a CYCLE - no final state!")
    print("It can run forever (infinite execution)")


def demonstrate_final_states():
    """Demonstrate final states."""
    print("\n" + "=" * 60)
    print("FINAL STATES")
    print("=" * 60)
    
    print("""
A FINAL STATE is a state with no possible transitions.

Examples:
- Counter reaching max_value
- Coin flip after max_flips flips
- Sorted sequence in a sorting algorithm
- Solution state in a puzzle
""")
    
    counter = SimpleCounter(max_value=3)
    
    print("\nCounter states:")
    for i in range(5):
        transitions = counter.get_transitions(i)
        is_final = len(transitions) == 0
        print(f"  State {i}: {len(transitions)} transitions {'(FINAL)' if is_final else ''}")


def main():
    """Run all demonstrations."""
    demonstrate_basic_concepts()
    demonstrate_deterministic()
    demonstrate_nondeterministic()
    demonstrate_reachability()
    demonstrate_cycles()
    demonstrate_final_states()
    
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
1. State machines model algorithms and systems
2. They consist of states, initial state, and transitions
3. Deterministic: one transition per state
4. Non-deterministic: multiple transitions possible
5. Reachability: can we reach a specific state?
6. Final states: states with no transitions
7. State machines can have cycles (infinite executions)

Next lesson: The 8-Puzzle Problem
  → We'll use invariants to prove unreachability!
""")


if __name__ == "__main__":
    main()
