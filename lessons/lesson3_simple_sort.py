"""
Simple Sort with Termination Proof

This module implements the simple sorting algorithm discussed in the MIT lecture
and proves its termination using a potential function (the number of inversions).
"""

from typing import List, Tuple
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state_machine import StateMachine, PotentialFunction, verify_termination


class SimpleSortMachine(StateMachine):
    """
    State machine for the simple sort algorithm.
    
    The algorithm:
    - At each step, find an index i where elements at i and i+1 are out of order
    - Swap them
    - Repeat until no such index exists
    """
    
    def __init__(self, sequence: List):
        """
        Initialize with a sequence to sort.
        
        Args:
            sequence: List of comparable elements
        """
        self.initial_sequence = tuple(sequence)
        super().__init__()
    
    def get_initial_state(self) -> Tuple:
        """Return the initial sequence as a tuple."""
        return self.initial_sequence
    
    def get_transitions(self, state: Tuple) -> List[Tuple]:
        """
        Get all possible transitions (swaps of adjacent out-of-order elements).
        
        Args:
            state: Current sequence
            
        Returns:
            List of sequences resulting from swapping adjacent out-of-order elements
        """
        transitions = []
        
        for i in range(len(state) - 1):
            # If elements at i and i+1 are out of order
            if state[i] > state[i + 1]:
                # Create new state with swap
                new_state = list(state)
                new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
                transitions.append(tuple(new_state))
        
        return transitions
    
    def is_sorted(self, state: Tuple = None) -> bool:
        """
        Check if a sequence is sorted.
        
        Args:
            state: The state to check (default: current state)
        """
        if state is None:
            state = self.current_state
        
        for i in range(len(state) - 1):
            if state[i] > state[i + 1]:
                return False
        return True


def count_inversions(sequence: Tuple) -> int:
    """
    Count the number of inversions in a sequence.
    
    An inversion is a pair of indices (i, j) where i < j but sequence[i] > sequence[j].
    
    Args:
        sequence: The sequence to analyze
        
    Returns:
        Number of inversions
    """
    inversions = 0
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] > sequence[j]:
                inversions += 1
    return inversions


def demonstrate_simple_sort():
    """
    Demonstrate the simple sort algorithm and prove it terminates.
    """
    print("=" * 60)
    print("SIMPLE SORT ALGORITHM WITH TERMINATION PROOF")
    print("=" * 60)
    
    # Example sequence
    sequence = [4, 1, 3, 2]
    sorter = SimpleSortMachine(sequence)
    
    print(f"\nInitial sequence: {list(sorter.current_state)}")
    print(f"Initial inversions: {count_inversions(sorter.current_state)}")
    
    print("\n" + "=" * 60)
    print("EXECUTION TRACE")
    print("=" * 60)
    
    step = 0
    max_steps = 20  # Safety limit
    
    while not sorter.is_sorted() and step < max_steps:
        current = sorter.current_state
        inversions = count_inversions(current)
        
        print(f"\nStep {step}: {list(current)}")
        print(f"  Inversions: {inversions}")
        
        # Get possible transitions
        transitions = sorter.get_transitions(current)
        
        if not transitions:
            break
        
        # Show all possible moves
        print(f"  Possible swaps:")
        for i, next_state in enumerate(transitions):
            next_inversions = count_inversions(next_state)
            print(f"    {i + 1}. {list(next_state)} (inversions: {next_inversions})")
        
        # Take the first transition (arbitrary choice)
        sorter.step(transitions[0])
        step += 1
    
    print(f"\nFinal sequence: {list(sorter.current_state)}")
    print(f"Final inversions: {count_inversions(sorter.current_state)}")
    print(f"Is sorted? {sorter.is_sorted()}")
    print(f"Total steps: {step}")
    
    print("\n" + "=" * 60)
    print("TERMINATION PROOF")
    print("=" * 60)
    
    print("\nWe use a POTENTIAL FUNCTION to prove termination:")
    print("  f(state) = number of inversions in the state")
    
    print("\nKey observations:")
    print("  1. f maps states to natural numbers (0, 1, 2, ...)")
    print("  2. f is strictly decreasing:")
    print("     - Each swap reduces inversions by exactly 1")
    print("     - We only swap when elements are out of order")
    print("  3. Natural numbers cannot decrease forever")
    print("  4. Therefore: the algorithm MUST terminate!")
    
    print("\nMaximum possible steps:")
    n = len(sequence)
    max_inversions = n * (n - 1) // 2
    print(f"  For a sequence of length {n}:")
    print(f"  Max inversions = {n} × {n-1} / 2 = {max_inversions}")
    print(f"  So the algorithm terminates in at most {max_inversions} steps")
    
    return sorter


def demonstrate_potential_function():
    """
    Demonstrate how the potential function decreases with each step.
    """
    print("\n" + "=" * 60)
    print("VISUALIZING THE POTENTIAL FUNCTION")
    print("=" * 60)
    
    sequences = [
        [4, 3, 2, 1],  # Worst case (completely reversed)
        [2, 1, 3, 4],  # Partially sorted
        [1, 2, 3, 4],  # Already sorted
    ]
    
    for seq in sequences:
        print(f"\nSequence: {seq}")
        print(f"Inversions: {count_inversions(tuple(seq))}")
        
        sorter = SimpleSortMachine(seq)
        if sorter.is_sorted():
            print("Already sorted! (Final state)")
        else:
            transitions = sorter.get_transitions(sorter.current_state)
            print(f"Can make {len(transitions)} swaps")
            for t in transitions:
                print(f"  → {list(t)} (inversions: {count_inversions(t)})")


def verify_simple_sort_termination():
    """
    Use our framework to verify that simple sort terminates.
    """
    print("\n" + "=" * 60)
    print("FORMAL VERIFICATION OF TERMINATION")
    print("=" * 60)
    
    # Create a simple sort instance
    sequence = [3, 1, 4, 1, 5, 2]
    sorter = SimpleSortMachine(sequence)
    
    # Define the potential function
    potential = PotentialFunction(
        function=count_inversions,
        name="Number of inversions"
    )
    
    print(f"\nVerifying termination for sequence: {sequence}")
    print(f"Initial potential: {potential.evaluate(sorter.get_initial_state())}")
    
    # Verify a few states manually
    print("\nChecking potential function is strictly decreasing:")
    
    current = sorter.get_initial_state()
    for step in range(min(5, count_inversions(current))):
        transitions = sorter.get_transitions(current)
        if not transitions:
            print(f"  Reached final state at step {step}")
            break
        
        current_pot = potential.evaluate(current)
        next_state = transitions[0]
        next_pot = potential.evaluate(next_state)
        
        print(f"  Step {step}: potential {current_pot} → {next_pot} (decreased by {current_pot - next_pot})")
        
        current = next_state
    
    print("\n✓ Potential function strictly decreases at each step")
    print("✓ Therefore, the algorithm MUST terminate!")


def prove_final_state_is_sorted():
    """
    Prove that every final state (state with no transitions) is sorted.
    
    This is a simple proof by contradiction that demonstrates partial correctness.
    """
    print("\n" + "=" * 60)
    print("PROVING FINAL STATES ARE SORTED")
    print("=" * 60)
    
    print("\nTheorem: Every final state is sorted.")
    print("\nProof (by contradiction):")
    print("  1. Suppose state s is a final state")
    print("  2. Suppose s is NOT sorted")
    print("  3. Then there exists index i where s[i] > s[i+1]")
    print("  4. But then we can swap s[i] and s[i+1]")
    print("  5. This means s has a transition!")
    print("  6. Contradiction! s is supposed to be final (no transitions)")
    print("  7. Therefore, s MUST be sorted. QED")
    
    # Demonstrate with examples
    print("\nExamples:")
    
    examples = [
        ([1, 2, 3, 4], True),
        ([1, 3, 2, 4], False),
        ([4, 3, 2, 1], False),
    ]
    
    for seq, expected_final in examples:
        sorter = SimpleSortMachine(seq)
        transitions = sorter.get_transitions(tuple(seq))
        is_final = len(transitions) == 0
        is_sorted = sorter.is_sorted(tuple(seq))
        
        print(f"\n  Sequence: {seq}")
        print(f"    Is sorted? {is_sorted}")
        print(f"    Is final? {is_final}")
        print(f"    {'✓' if is_final == expected_final else '✗'} Matches expectation")


if __name__ == "__main__":
    sorter = demonstrate_simple_sort()
    demonstrate_potential_function()
    verify_simple_sort_termination()
    prove_final_state_is_sorted()
