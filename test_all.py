"""
Comprehensive Test Suite for State Machines Repository

This script tests all the main components to ensure everything works.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.state_machine import StateMachine, Invariant, PotentialFunction
        print("  PASS: Core framework imports successful")
    except Exception as e:
        print(f"  FAIL: Core framework import failed: {e}")
        return False
    
    try:
        from src.visualize import visualize_puzzle_state, visualize_sequence
        print("  PASS: Visualization module imports successful")
    except Exception as e:
        print(f"  FAIL: Visualization module import failed: {e}")
        return False
    
    return True


def test_lessons():
    """Test that lessons can be imported and run."""
    print("\nTesting lessons...")
    
    # Test lesson imports
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from lessons.lesson2_eight_puzzle import EightPuzzle, count_inversions
        from lessons.lesson3_simple_sort import SimpleSortMachine
        print("  PASS: Lesson modules import successfully")
    except Exception as e:
        print(f"  FAIL: Lesson import failed: {e}")
        return False
    
    # Test 8-puzzle
    try:
        puzzle = EightPuzzle((1, 2, 3, 4, 5, 6, 8, 7, 0))
        inversions = count_inversions((1, 2, 3, 4, 5, 6, 8, 7, 0))
        assert inversions == 1, f"Expected 1 inversion, got {inversions}"
        print("  PASS: 8-Puzzle works correctly")
    except Exception as e:
        print(f"  FAIL: 8-Puzzle test failed: {e}")
        return False
    
    # Test simple sort
    try:
        sorter = SimpleSortMachine([4, 1, 3, 2])
        assert not sorter.is_sorted(), "Should not be sorted initially"
        print("  PASS: Simple Sort works correctly")
    except Exception as e:
        print(f"  FAIL: Simple Sort test failed: {e}")
        return False
    
    return True


def test_core_framework():
    """Test the core state machine framework."""
    print("\nTesting core framework...")
    
    from src.state_machine import StateMachine, Invariant, PotentialFunction
    
    # Test simple state machine
    class Counter(StateMachine):
        def __init__(self, max_val=5):
            self.max_val = max_val
            super().__init__()
        
        def get_initial_state(self):
            return 0
        
        def get_transitions(self, state):
            if state < self.max_val:
                return [state + 1]
            return []
    
    try:
        counter = Counter(max_val=3)
        assert counter.current_state == 0
        assert counter.is_reachable(3)
        assert not counter.is_reachable(10)
        print("  PASS: State machine creation and reachability works")
    except Exception as e:
        print(f"  FAIL: State machine test failed: {e}")
        return False
    
    # Test invariant
    try:
        def is_non_negative(state):
            return state >= 0
        
        inv = Invariant(is_non_negative, "Non-negative")
        assert inv.holds(5)
        assert not inv.holds(-1)
        print("  PASS: Invariant works correctly")
    except Exception as e:
        print(f"  FAIL: Invariant test failed: {e}")
        return False
    
    # Test potential function
    try:
        def potential(state):
            return 10 - state
        
        pot = PotentialFunction(potential, "Decreasing")
        assert pot.evaluate(0) == 10
        assert pot.evaluate(5) == 5
        print("  PASS: Potential function works correctly")
    except Exception as e:
        print(f"  FAIL: Potential function test failed: {e}")
        return False
    
    return True


def test_examples():
    """Test custom examples."""
    print("\nTesting examples...")
    
    try:
        from examples.custom_state_machines import DoorLock, BankAccount, PalindromeBuilder
        
        # Test door lock
        lock = DoorLock()
        assert lock.is_reachable("UNLOCKED")
        
        # Test bank account
        account = BankAccount(initial_balance=0)
        assert account.current_state == (0, True)
        
        # Test palindrome builder
        builder = PalindromeBuilder(max_length=3)
        assert builder.is_reachable("a")
        
        print("  PASS: All examples work correctly")
        return True
    except Exception as e:
        print(f"  FAIL: Examples test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Core Framework", test_core_framework()))
    results.append(("Lessons", test_lessons()))
    results.append(("Examples", test_examples()))
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
