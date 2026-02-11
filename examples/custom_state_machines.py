"""
Example: Creating Custom State Machines

This file demonstrates how to create your own state machines
using the framework provided in this repository.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state_machine import StateMachine, Invariant, PotentialFunction
from typing import List


# Example 1: Door Lock State Machine
class DoorLock(StateMachine):
    """
    A simple door lock with a 3-digit code: 1-2-3
    
    States: (d1, d2, d3) where each di is the i-th digit entered
    Special state: "UNLOCKED"
    """
    
    def get_initial_state(self):
        return ()  # No digits entered
    
    def get_transitions(self, state):
        if state == "UNLOCKED":
            return []  # Final state
        
        if len(state) == 3:
            # Check if correct code (1, 2, 3)
            if state == (1, 2, 3):
                return ["UNLOCKED"]
            else:
                return [()]  # Reset on wrong code
        
        # Can enter any digit 0-9
        return [state + (digit,) for digit in range(10)]


# Example 2: Bank Account State Machine
class BankAccount(StateMachine):
    """
    Simplified bank account model.
    
    States: (balance, is_open)
    Transitions:
    - Deposit: add money
    - Withdraw: remove money (if sufficient balance)
    - Close: close account (if balance is 0)
    """
    
    def __init__(self, initial_balance=0):
        self.initial_balance = initial_balance
        super().__init__()
    
    def get_initial_state(self):
        return (self.initial_balance, True)  # (balance, is_open)
    
    def get_transitions(self, state):
        balance, is_open = state
        
        if not is_open:
            return []  # Closed accounts have no transitions
        
        transitions = []
        
        # Can deposit $10, $20, or $50
        for amount in [10, 20, 50]:
            transitions.append((balance + amount, True))
        
        # Can withdraw $10, $20 if sufficient balance
        for amount in [10, 20]:
            if balance >= amount:
                transitions.append((balance - amount, True))
        
        # Can close if balance is 0
        if balance == 0:
            transitions.append((0, False))
        
        return transitions


# Example 3: Palindrome Checker State Machine
class PalindromeBuilder(StateMachine):
    """
    Build palindromes by adding characters to a string.
    
    States: strings
    Transitions: add a character that maintains palindrome property
    """
    
    def __init__(self, max_length=5):
        self.max_length = max_length
        super().__init__()
    
    def get_initial_state(self):
        return ""  # Empty string (trivially a palindrome)
    
    def is_palindrome(self, s):
        return s == s[::-1]
    
    def get_transitions(self, state):
        if len(state) >= self.max_length:
            return []
        
        transitions = []
        
        # Try adding each letter a-c
        for char in ['a', 'b', 'c']:
            new_state = state + char
            if self.is_palindrome(new_state):
                transitions.append(new_state)
        
        return transitions


def demo_door_lock():
    """Demonstrate the door lock state machine."""
    print("=" * 60)
    print("EXAMPLE 1: DOOR LOCK STATE MACHINE")
    print("=" * 60)
    
    lock = DoorLock()
    
    print("\nCorrect code: 1-2-3")
    print(f"Initial state: {lock.current_state}")
    print(f"Is 'UNLOCKED' reachable? {lock.is_reachable('UNLOCKED')}")
    
    # Find path to unlock
    path = lock.find_path("UNLOCKED")
    if path:
        print(f"\nShortest path to unlock:")
        for i, state in enumerate(path):
            print(f"  Step {i}: {state}")
    
    # Try wrong code
    print("\nWhat happens with wrong code (9-9-9)?")
    wrong_path = [(), (9,), (9, 9), (9, 9, 9), ()]
    print(f"  {' → '.join(str(s) for s in wrong_path)}")
    print("  Resets to initial state!")


def demo_bank_account():
    """Demonstrate the bank account state machine."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: BANK ACCOUNT STATE MACHINE")
    print("=" * 60)
    
    account = BankAccount(initial_balance=0)
    
    print(f"\nInitial state: {account.current_state}")
    
    # Can we close immediately?
    print(f"Can close immediately? {account.is_reachable((0, False))}")
    
    # Deposit some money
    print("\nSimulation:")
    print(f"  Start: {account.current_state}")
    
    account.step((10, True))  # Deposit $10
    print(f"  After deposit $10: {account.current_state}")
    
    account.step((30, True))  # Deposit $20
    print(f"  After deposit $20: {account.current_state}")
    
    account.step((10, True))  # Withdraw $20
    print(f"  After withdraw $20: {account.current_state}")
    
    account.step((0, True))  # Withdraw $10
    print(f"  After withdraw $10: {account.current_state}")
    
    account.step((0, False))  # Close
    print(f"  After close: {account.current_state}")
    
    # Define an invariant: balance is always non-negative
    def non_negative_balance(state):
        if isinstance(state, tuple):
            return state[0] >= 0
        return True
    
    invariant = Invariant(non_negative_balance, "Balance is non-negative")
    print(f"\nInvariant: {invariant.name}")
    print(f"Holds for initial state? {invariant.verify_initial_state(account)}")


def demo_palindrome_builder():
    """Demonstrate the palindrome builder state machine."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: PALINDROME BUILDER STATE MACHINE")
    print("=" * 60)
    
    builder = PalindromeBuilder(max_length=5)
    
    print(f"\nBuilding palindromes (max length {builder.max_length})")
    print(f"Available characters: a, b, c")
    
    # Explore all reachable palindromes
    visited = set()
    queue = [builder.get_initial_state()]
    visited.add(builder.get_initial_state())
    
    while queue:
        state = queue.pop(0)
        
        for next_state in builder.get_transitions(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    # Group by length
    by_length = {}
    for palindrome in visited:
        length = len(palindrome)
        if length not in by_length:
            by_length[length] = []
        by_length[length].append(palindrome)
    
    print(f"\nTotal palindromes found: {len(visited)}")
    for length in sorted(by_length.keys()):
        palindromes = sorted(by_length[length])
        print(f"\nLength {length} ({len(palindromes)} palindromes):")
        print(f"  {', '.join(repr(p) if p else 'empty' for p in palindromes)}")
    
    # Check specific palindrome
    target = "aba"
    print(f"\nIs '{target}' reachable? {builder.is_reachable(target)}")
    if builder.is_reachable(target):
        path = builder.find_path(target)
        print(f"Path: {' → '.join(repr(s) if s else 'empty' for s in path)}")


if __name__ == "__main__":
    demo_door_lock()
    demo_bank_account()
    demo_palindrome_builder()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
These examples show how to create state machines for various problems:

1. Door Lock: Sequential state machine with reset
2. Bank Account: State machine with constraints (balance ≥ 0)
3. Palindrome Builder: State machine with a maintained invariant

Key takeaways:
- State machines can model many different systems
- Invariants help reason about what's possible
- Potential functions help prove termination
- The framework is flexible and powerful!

Try creating your own state machines!
""")
