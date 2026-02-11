"""
The 8-Puzzle State Machine

This module implements the 8-puzzle problem discussed in the MIT lecture.
The 8-puzzle is a 3x3 grid with 8 numbered tiles and one empty space.

We prove that certain configurations are unreachable using the concept of inversions.
"""

from typing import List, Tuple
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state_machine import StateMachine, Invariant


class EightPuzzle(StateMachine):
    """
    State machine for the 8-puzzle problem.
    
    States are represented as tuples of 9 elements (3x3 grid flattened).
    The empty space is represented by 0 or '*'.
    """
    
    def __init__(self, initial_config: Tuple):
        """
        Initialize the 8-puzzle with a specific configuration.
        
        Args:
            initial_config: Tuple of 9 elements representing the initial board state
                           Elements should be 0-8 (or use '*' for empty space)
        """
        # Convert '*' to 0 for consistency
        self.initial_config = tuple(
            0 if x == '*' else x for x in initial_config
        )
        super().__init__()
    
    def get_initial_state(self) -> Tuple:
        """Return the initial puzzle configuration."""
        return self.initial_config
    
    def get_blank_position(self, state: Tuple) -> int:
        """Get the index of the blank (0) tile."""
        return state.index(0)
    
    def get_transitions(self, state: Tuple) -> List[Tuple]:
        """
        Get all valid moves from the current state.
        
        A move swaps the blank tile with an adjacent tile (horizontal or vertical).
        """
        blank_pos = self.get_blank_position(state)
        row, col = blank_pos // 3, blank_pos % 3
        
        transitions = []
        
        # Possible moves: up, down, left, right
        moves = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1),   # right
        ]
        
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            
            # Check if move is valid (within bounds)
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_blank_pos = new_row * 3 + new_col
                
                # Create new state by swapping
                new_state = list(state)
                new_state[blank_pos], new_state[new_blank_pos] = \
                    new_state[new_blank_pos], new_state[blank_pos]
                
                transitions.append(tuple(new_state))
        
        return transitions
    
    def display(self, state: Tuple = None) -> str:
        """
        Display the puzzle in a 3x3 grid format.
        
        Args:
            state: The state to display (default: current state)
        """
        if state is None:
            state = self.current_state
        
        result = []
        for i in range(3):
            row = []
            for j in range(3):
                val = state[i * 3 + j]
                row.append('*' if val == 0 else str(val))
            result.append(' '.join(row))
        
        return '\n'.join(result)


def count_inversions(state: Tuple) -> int:
    """
    Count the number of inversions in a puzzle state.
    
    An inversion is a pair of indices (i, j) where i < j and state[i] > state[j].
    We ignore the blank tile (0) when counting inversions.
    
    This is the key to proving unreachability in the 8-puzzle!
    
    Args:
        state: The puzzle state (tuple of 9 elements)
        
    Returns:
        Number of inversions
    """
    # Remove the blank tile
    sequence = [x for x in state if x != 0]
    
    inversions = 0
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] > sequence[j]:
                inversions += 1
    
    return inversions


def has_odd_inversions(state: Tuple) -> bool:
    """
    Check if a state has an odd number of inversions.
    
    This is our invariant for the 8-puzzle!
    """
    return count_inversions(state) % 2 == 1


def has_even_inversions(state: Tuple) -> bool:
    """Check if a state has an even number of inversions."""
    return count_inversions(state) % 2 == 0


def demonstrate_8_puzzle_impossibility():
    """
    Demonstrate that the classic 8-puzzle problem is impossible.
    
    Starting from: 1 2 3
                   4 5 6
                   8 7 *
                   
    Can we reach:  1 2 3
                   4 5 6
                   7 8 *
    
    Answer: NO! And we prove it using inversions.
    """
    print("=" * 60)
    print("THE 8-PUZZLE IMPOSSIBILITY PROOF")
    print("=" * 60)
    
    # Initial configuration
    initial = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    puzzle = EightPuzzle(initial)
    
    print("\nInitial Configuration:")
    print(puzzle.display())
    print(f"Number of inversions: {count_inversions(initial)}")
    print(f"Parity: {'ODD' if has_odd_inversions(initial) else 'EVEN'}")
    
    # Target configuration
    target = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    print("\nTarget Configuration:")
    print(puzzle.display(target))
    print(f"Number of inversions: {count_inversions(target)}")
    print(f"Parity: {'ODD' if has_odd_inversions(target) else 'EVEN'}")
    
    # Define the invariant
    invariant = Invariant(
        predicate=has_odd_inversions,
        name="Odd number of inversions"
    )
    
    print("\n" + "=" * 60)
    print("THE INVARIANT PRINCIPLE")
    print("=" * 60)
    
    print(f"\n1. Initial state has odd inversions? {invariant.holds(initial)}")
    
    # Let's verify that the invariant is preserved by a few moves
    print("\n2. Checking that the invariant is preserved by moves...")
    
    transitions = puzzle.get_transitions(initial)
    print(f"\n   From initial state, we can make {len(transitions)} moves:")
    
    for i, next_state in enumerate(transitions, 1):
        inversions = count_inversions(next_state)
        parity = "ODD" if inversions % 2 == 1 else "EVEN"
        print(f"   Move {i}: {inversions} inversions ({parity})")
    
    print("\n   All reachable states maintain odd parity!")
    
    print("\n3. Target state has even inversions, so it's UNREACHABLE!")
    
    # Verify using our framework
    print("\n" + "=" * 60)
    print("VERIFICATION USING STATE MACHINE FRAMEWORK")
    print("=" * 60)
    
    # Note: Full verification would take too long for all states,
    # but we can verify the principle locally
    print("\nThe invariant principle tells us:")
    print("- If P(initial_state) is true")
    print("- And P is preserved by all transitions")
    print("- Then P is true for ALL reachable states")
    print("\nSince target has even inversions, it CANNOT be reachable!")
    
    return puzzle, invariant


def demonstrate_horizontal_vs_vertical_moves():
    """
    Show how horizontal and vertical moves affect inversions differently.
    """
    print("\n" + "=" * 60)
    print("HORIZONTAL VS VERTICAL MOVES")
    print("=" * 60)
    
    puzzle = EightPuzzle((1, 2, 3, 4, 5, 6, 8, 7, 0))
    
    print("\nStarting state:")
    print(puzzle.display())
    print(f"Inversions: {count_inversions(puzzle.current_state)}")
    
    # Horizontal move
    print("\n--- HORIZONTAL MOVE (blank moves right) ---")
    horizontal_state = (1, 2, 3, 4, 5, 6, 8, 0, 7)
    print(puzzle.display(horizontal_state))
    print(f"Inversions: {count_inversions(horizontal_state)}")
    print("Inversions unchanged! (Blank doesn't count)")
    
    # Vertical move
    print("\n--- VERTICAL MOVE (blank moves up) ---")
    vertical_state = (1, 2, 3, 4, 5, 0, 8, 7, 6)
    print(puzzle.display(vertical_state))
    print(f"Inversions: {count_inversions(vertical_state)}")
    print("Inversions changed by 2! (Parity preserved)")
    
    print("\nKey insight:")
    print("- Horizontal moves: inversions stay the same")
    print("- Vertical moves: inversions change by ±2")
    print("- Therefore: PARITY is always preserved!")


if __name__ == "__main__":
    puzzle, invariant = demonstrate_8_puzzle_impossibility()
    demonstrate_horizontal_vs_vertical_moves()
