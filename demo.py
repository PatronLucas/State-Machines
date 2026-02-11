#!/usr/bin/env python3
"""
Interactive demonstration of state machines
Run this script to see state machines in action!
"""

from state_machine import StateMachine
from examples import (
    create_turnstile,
    create_binary_divisible_by_3,
    create_even_ones_counter,
)


def demonstrate_turnstile():
    """Interactive turnstile demonstration."""
    print("=" * 60)
    print("TURNSTILE STATE MACHINE DEMONSTRATION")
    print("=" * 60)
    print("\nA turnstile starts LOCKED. You can:")
    print("  - Insert a 'coin' to UNLOCK it")
    print("  - 'push' to go through (locks it if unlocked)")
    print("\nState Diagram:")
    print("    +--------+  coin   +-----------+")
    print("    | LOCKED | ------> | UNLOCKED  |")
    print("    |        | <------ |           |")
    print("    +--------+  push   +-----------+")
    print()
    
    turnstile = create_turnstile()
    
    scenarios = [
        ("Initial state", []),
        ("Insert coin", ['coin']),
        ("Insert coin, then push", ['coin', 'push']),
        ("Insert coin, insert another coin", ['coin', 'coin']),
        ("Try to push when locked", ['push']),
        ("Complex: coin, push, push, coin, coin, push", 
         ['coin', 'push', 'push', 'coin', 'coin', 'push']),
    ]
    
    for description, sequence in scenarios:
        turnstile.reset()
        print(f"Scenario: {description}")
        print(f"  Sequence: {' -> '.join(sequence) if sequence else '(none)'}")
        
        for action in sequence:
            turnstile.transition(action)
        
        print(f"  Final state: {turnstile.current_state}")
        print()


def demonstrate_binary_divisibility():
    """Demonstrate binary divisibility checker."""
    print("=" * 60)
    print("BINARY DIVISIBILITY BY 3 DEMONSTRATION")
    print("=" * 60)
    print("\nThis machine checks if a binary number is divisible by 3.")
    print("It uses the mathematical property that:")
    print("  If n ≡ r (mod 3), then 2n ≡ 2r (mod 3) and 2n+1 ≡ 2r+1 (mod 3)")
    print("\nStates represent remainders: S0=0, S1=1, S2=2")
    print()
    
    div3 = create_binary_divisible_by_3()
    
    test_cases = [
        ('0', 0),
        ('11', 3),
        ('110', 6),
        ('1001', 9),
        ('1100', 12),
        ('1111', 15),
        ('101', 5),
        ('111', 7),
        ('1010', 10),
        ('10000', 16),
    ]
    
    print("Binary  | Decimal | Divisible by 3? | Result")
    print("-" * 55)
    
    for binary, decimal in test_cases:
        result = div3.accepts(binary)
        expected = (decimal % 3 == 0)
        status = "✓" if result == expected else "✗"
        div_str = "Yes" if decimal % 3 == 0 else "No"
        result_str = "ACCEPT" if result else "REJECT"
        print(f"{binary:7} | {decimal:7} | {div_str:15} | {result_str:6} {status}")


def demonstrate_even_ones():
    """Demonstrate even ones counter."""
    print("\n" + "=" * 60)
    print("EVEN ONES COUNTER DEMONSTRATION")
    print("=" * 60)
    print("\nThis machine accepts binary strings with an even number of 1s.")
    print("It's a parity checker - two states track odd/even count.")
    print("\nState Diagram:")
    print("    +------+  1   +-----+")
    print("    | EVEN | <--> | ODD |")
    print("    +------+  1   +-----+")
    print()
    
    even_ones = create_even_ones_counter()
    
    test_strings = [
        '',
        '0',
        '1',
        '00',
        '01',
        '10',
        '11',
        '0101',
        '1111',
        '111',
        '10101010',
    ]
    
    print("String    | Ones | Even? | Result")
    print("-" * 45)
    
    for s in test_strings:
        ones = s.count('1')
        result = even_ones.accepts(s)
        expected = (ones % 2 == 0)
        status = "✓" if result == expected else "✗"
        even_str = "Yes" if ones % 2 == 0 else "No"
        result_str = "ACCEPT" if result else "REJECT"
        string_display = s if s else "(empty)"
        print(f"{string_display:9} | {ones:4} | {even_str:5} | {result_str:6} {status}")


def trace_execution(sm, sequence, name="State Machine"):
    """Trace step-by-step execution of a state machine."""
    print(f"\n--- Tracing {name} ---")
    print(f"Initial: {sm.current_state}")
    
    for i, symbol in enumerate(sequence, 1):
        old_state = sm.current_state
        sm.transition(symbol)
        print(f"Step {i}: {old_state} --({symbol})--> {sm.current_state}")
    
    accepting = sm.is_accepting()
    print(f"Final: {sm.current_state} {'(ACCEPT)' if accepting else '(REJECT)'}")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  STATE MACHINES: Interactive Demonstration".center(58) + "║")
    print("║" + "  Based on MIT OCW 6.1200J - Lecture 4".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    demonstrate_turnstile()
    demonstrate_binary_divisibility()
    demonstrate_even_ones()
    
    print("\n" + "=" * 60)
    print("EXECUTION TRACE EXAMPLES")
    print("=" * 60)
    
    # Trace turnstile
    turnstile = create_turnstile()
    trace_execution(turnstile, ['coin', 'push', 'push', 'coin'], "Turnstile")
    
    # Trace binary divisibility
    div3 = create_binary_divisible_by_3()
    trace_execution(div3, '1001', "Binary Divisibility (1001 = 9)")
    
    print("\n" + "=" * 60)
    print("Try running the tests with: python3 -m unittest test_state_machines.py")
    print("=" * 60)
    print()


if __name__ == '__main__':
    main()
