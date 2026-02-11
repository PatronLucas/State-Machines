"""
Example State Machines
Based on MIT OCW 6.1200J Mathematics for Computer Science - Lecture 4

This module contains classic state machine examples commonly used in
computer science education.
"""

from state_machine import StateMachine


def create_turnstile():
    """
    Create a turnstile state machine.
    
    A turnstile is a classic example of a state machine with two states:
    - LOCKED: The turnstile is locked
    - UNLOCKED: The turnstile is unlocked
    
    Inputs:
    - 'coin': Insert a coin
    - 'push': Push the turnstile
    
    State Diagram:
    
        +--------+  coin   +-----------+
        | LOCKED | ------> | UNLOCKED  |
        |        | <------ |           |
        +--------+  push   +-----------+
           ^  |               |  ^
           |  +--- push ------+  |
           +------- coin ---------+
    
    Transitions:
    - From LOCKED: coin -> UNLOCKED, push -> LOCKED (stays locked)
    - From UNLOCKED: coin -> UNLOCKED (stays unlocked), push -> LOCKED
    
    Returns:
        StateMachine: A configured turnstile state machine
    """
    states = {'LOCKED', 'UNLOCKED'}
    initial_state = 'LOCKED'
    transitions = {
        ('LOCKED', 'coin'): 'UNLOCKED',
        ('LOCKED', 'push'): 'LOCKED',
        ('UNLOCKED', 'coin'): 'UNLOCKED',
        ('UNLOCKED', 'push'): 'LOCKED',
    }
    
    return StateMachine(states, initial_state, transitions)


def create_binary_divisible_by_3():
    """
    Create a state machine that recognizes binary numbers divisible by 3.
    
    This machine reads binary digits (0 or 1) and accepts if the number
    represented is divisible by 3.
    
    States represent the remainder when divided by 3:
    - S0: remainder 0 (divisible by 3) - accepting state
    - S1: remainder 1
    - S2: remainder 2
    
    State Diagram:
    
        +----+  0   +----+  1   +----+
        | S0 | <--- | S2 | <--- | S1 |
        +----+      +----+      +----+
          | ^         ^ |         ^ |
          | +-- 1 ----+ +--- 0 ---+ |
          +----------- 0 ------------+
    
    Mathematical basis:
    If n has remainder r when divided by 3, then:
    - 2n (append 0) has remainder 2r mod 3
    - 2n+1 (append 1) has remainder (2r+1) mod 3
    
    Returns:
        StateMachine: A configured divisibility checker
    """
    states = {'S0', 'S1', 'S2'}
    initial_state = 'S0'
    
    # Transitions based on remainder arithmetic
    transitions = {
        ('S0', '0'): 'S0',  # 0*2 + 0 = 0 mod 3
        ('S0', '1'): 'S1',  # 0*2 + 1 = 1 mod 3
        ('S1', '0'): 'S2',  # 1*2 + 0 = 2 mod 3
        ('S1', '1'): 'S0',  # 1*2 + 1 = 3 mod 3 = 0
        ('S2', '0'): 'S1',  # 2*2 + 0 = 4 mod 3 = 1
        ('S2', '1'): 'S2',  # 2*2 + 1 = 5 mod 3 = 2
    }
    
    accepting_states = {'S0'}  # Only accept when divisible by 3
    
    return StateMachine(states, initial_state, transitions, accepting_states)


def create_sequence_detector(sequence):
    """
    Create a state machine that detects a specific sequence of inputs.
    
    This is a general pattern for detecting sequences like "101" or "abc".
    
    Args:
        sequence: The sequence to detect (string or list)
        
    Returns:
        StateMachine: A state machine that accepts when the sequence is detected
    """
    sequence = list(sequence)
    n = len(sequence)
    
    # Create states S0, S1, ..., Sn where Si means we've matched i characters
    states = set(f'S{i}' for i in range(n + 1))
    initial_state = 'S0'
    accepting_states = {f'S{n}'}
    
    transitions = {}
    
    # For each state, define transitions
    for i in range(n + 1):
        current_state = f'S{i}'
        
        if i < n:
            # If we see the next expected character, advance
            next_char = sequence[i]
            transitions[(current_state, next_char)] = f'S{i + 1}'
            
            # For other characters, we need to find the longest prefix match
            # For simplicity, we'll just reset to S0 for non-matching chars
            # (A more sophisticated version would use KMP-like failure function)
        
        # If we're in the accepting state and see the first character again,
        # we might start a new match
        if i == n:
            transitions[(current_state, sequence[0])] = 'S1'
    
    return StateMachine(states, initial_state, transitions, accepting_states)


def create_even_ones_counter():
    """
    Create a state machine that accepts binary strings with an even number of 1s.
    
    States:
    - EVEN: Even number of 1s seen (accepting state)
    - ODD: Odd number of 1s seen
    
    State Diagram:
    
        +------+  1   +-----+
        | EVEN | <--> | ODD |
        +------+  1   +-----+
          |  ^          |  ^
          +--+-- 0 -----+--+
    
    Returns:
        StateMachine: A state machine that checks for even number of 1s
    """
    states = {'EVEN', 'ODD'}
    initial_state = 'EVEN'  # Start with 0 ones (even)
    
    transitions = {
        ('EVEN', '0'): 'EVEN',  # 0 doesn't change parity
        ('EVEN', '1'): 'ODD',   # 1 flips parity
        ('ODD', '0'): 'ODD',    # 0 doesn't change parity
        ('ODD', '1'): 'EVEN',   # 1 flips parity
    }
    
    accepting_states = {'EVEN'}
    
    return StateMachine(states, initial_state, transitions, accepting_states)


def create_mod_counter(n):
    """
    Create a state machine that counts modulo n.
    
    This machine counts input events and keeps track of the count modulo n.
    
    Args:
        n: The modulus
        
    Returns:
        StateMachine: A modulo-n counter
    """
    states = set(f'S{i}' for i in range(n))
    initial_state = 'S0'
    
    # Single input type: 'tick' to increment
    transitions = {
        (f'S{i}', 'tick'): f'S{(i + 1) % n}'
        for i in range(n)
    }
    
    accepting_states = {'S0'}  # Accept when count is 0 mod n
    
    return StateMachine(states, initial_state, transitions, accepting_states)


if __name__ == '__main__':
    # Demonstrate the turnstile
    print("=== Turnstile Example ===")
    turnstile = create_turnstile()
    print(f"Initial state: {turnstile.current_state}")
    
    print("\nSequence: coin, push, push, coin, push")
    turnstile.transition('coin')
    print(f"After coin: {turnstile.current_state}")
    
    turnstile.transition('push')
    print(f"After push: {turnstile.current_state}")
    
    turnstile.transition('push')
    print(f"After push: {turnstile.current_state}")
    
    turnstile.transition('coin')
    print(f"After coin: {turnstile.current_state}")
    
    turnstile.transition('push')
    print(f"After push: {turnstile.current_state}")
    
    # Demonstrate binary divisibility by 3
    print("\n=== Binary Divisibility by 3 ===")
    div3 = create_binary_divisible_by_3()
    
    test_numbers = [
        ('0', 0),      # 0 is divisible by 3
        ('11', 3),     # 11 in binary = 3
        ('110', 6),    # 110 in binary = 6
        ('1001', 9),   # 1001 in binary = 9
        ('101', 5),    # 101 in binary = 5 (not divisible)
    ]
    
    for binary, decimal in test_numbers:
        result = div3.accepts(binary)
        print(f"{binary} (decimal {decimal}): {'ACCEPT' if result else 'REJECT'}")
    
    # Demonstrate even ones counter
    print("\n=== Even Ones Counter ===")
    even_ones = create_even_ones_counter()
    
    test_strings = ['0000', '0101', '1111', '1010', '111']
    
    for s in test_strings:
        result = even_ones.accepts(s)
        ones_count = s.count('1')
        print(f"{s} ({ones_count} ones): {'ACCEPT' if result else 'REJECT'}")
    
    # Demonstrate mod counter
    print("\n=== Mod 4 Counter ===")
    mod4 = create_mod_counter(4)
    
    print("Processing 7 ticks:")
    for i in range(7):
        mod4.transition('tick')
        status = "ACCEPT" if mod4.is_accepting() else "REJECT"
        print(f"After tick {i+1}: state={mod4.current_state}, {status}")
