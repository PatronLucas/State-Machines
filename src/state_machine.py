"""
Core State Machine Framework

This module provides the fundamental building blocks for creating and working
with state machines as described in MIT's 6.1200J Mathematics for Computer Science.

A state machine consists of:
- A set of states
- An initial state
- Transition rules between states
"""

from typing import Any, Callable, List, Set, Tuple, Optional, Dict
from abc import ABC, abstractmethod


class StateMachine(ABC):
    """
    Abstract base class for state machines.
    
    Subclasses should implement:
    - get_initial_state(): Returns the initial state
    - get_transitions(state): Returns list of possible next states from current state
    """
    
    def __init__(self):
        self.current_state = self.get_initial_state()
        self.execution_history = [self.current_state]
    
    @abstractmethod
    def get_initial_state(self) -> Any:
        """Return the initial state of the state machine."""
        pass
    
    @abstractmethod
    def get_transitions(self, state: Any) -> List[Any]:
        """
        Return all possible states that can be reached from the given state.
        
        Args:
            state: The current state
            
        Returns:
            List of possible next states
        """
        pass
    
    def is_final_state(self, state: Any) -> bool:
        """
        Check if a state is a final state (no possible transitions).
        
        Args:
            state: The state to check
            
        Returns:
            True if the state has no possible transitions
        """
        return len(self.get_transitions(state)) == 0
    
    def step(self, next_state: Any) -> bool:
        """
        Take a single step in the state machine execution.
        
        Args:
            next_state: The state to transition to
            
        Returns:
            True if the transition was valid, False otherwise
        """
        possible_transitions = self.get_transitions(self.current_state)
        
        if next_state not in possible_transitions:
            return False
        
        self.current_state = next_state
        self.execution_history.append(next_state)
        return True
    
    def reset(self):
        """Reset the state machine to its initial state."""
        self.current_state = self.get_initial_state()
        self.execution_history = [self.current_state]
    
    def get_execution(self) -> List[Any]:
        """Return the complete execution history."""
        return self.execution_history.copy()
    
    def is_reachable(self, target_state: Any, max_depth: int = 1000) -> bool:
        """
        Check if a state is reachable using breadth-first search.
        
        Args:
            target_state: The state to check for reachability
            max_depth: Maximum search depth to prevent infinite loops
            
        Returns:
            True if the target state is reachable, False otherwise
        """
        visited = {self.get_initial_state()}
        queue = [(self.get_initial_state(), 0)]
        
        while queue:
            state, depth = queue.pop(0)
            
            if state == target_state:
                return True
            
            if depth >= max_depth:
                continue
            
            for next_state in self.get_transitions(state):
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, depth + 1))
        
        return False
    
    def find_path(self, target_state: Any, max_depth: int = 1000) -> Optional[List[Any]]:
        """
        Find a path from the initial state to the target state.
        
        Args:
            target_state: The state to reach
            max_depth: Maximum search depth
            
        Returns:
            List of states forming a path, or None if no path exists
        """
        visited = {self.get_initial_state()}
        queue = [(self.get_initial_state(), [self.get_initial_state()], 0)]
        
        while queue:
            state, path, depth = queue.pop(0)
            
            if state == target_state:
                return path
            
            if depth >= max_depth:
                continue
            
            for next_state in self.get_transitions(state):
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [next_state], depth + 1))
        
        return None


class Invariant:
    """
    Represents an invariant (preserved predicate) for a state machine.
    
    An invariant is a property that:
    1. Holds for the initial state
    2. Is preserved by all transitions
    """
    
    def __init__(self, predicate: Callable[[Any], bool], name: str = ""):
        """
        Initialize an invariant.
        
        Args:
            predicate: A function that returns True if the property holds for a state
            name: Optional name for the invariant (for debugging/display)
        """
        self.predicate = predicate
        self.name = name or "Unnamed Invariant"
    
    def holds(self, state: Any) -> bool:
        """Check if the invariant holds for a given state."""
        return self.predicate(state)
    
    def verify_initial_state(self, state_machine: StateMachine) -> bool:
        """Verify that the invariant holds for the initial state."""
        return self.holds(state_machine.get_initial_state())
    
    def verify_preserved(self, state_machine: StateMachine, state: Any) -> bool:
        """
        Verify that the invariant is preserved by all transitions from a state.
        
        Args:
            state_machine: The state machine
            state: The state to check transitions from
            
        Returns:
            True if the invariant is preserved by all transitions
        """
        if not self.holds(state):
            return True  # Vacuously true if invariant doesn't hold for current state
        
        transitions = state_machine.get_transitions(state)
        return all(self.holds(next_state) for next_state in transitions)


class PotentialFunction:
    """
    Represents a potential function (derived variable) for proving termination.
    
    A potential function maps states to real numbers and can be used to prove
    that a state machine terminates by showing it strictly decreases.
    """
    
    def __init__(self, function: Callable[[Any], float], name: str = ""):
        """
        Initialize a potential function.
        
        Args:
            function: A function that maps states to real numbers
            name: Optional name for the potential function
        """
        self.function = function
        self.name = name or "Unnamed Potential Function"
    
    def evaluate(self, state: Any) -> float:
        """Evaluate the potential function at a given state."""
        return self.function(state)
    
    def is_strictly_decreasing(self, state_machine: StateMachine, state: Any) -> bool:
        """
        Check if the potential function strictly decreases for all transitions.
        
        Args:
            state_machine: The state machine
            state: The state to check transitions from
            
        Returns:
            True if the potential function strictly decreases for all transitions
        """
        current_value = self.evaluate(state)
        transitions = state_machine.get_transitions(state)
        
        if not transitions:  # Final state
            return True
        
        return all(self.evaluate(next_state) < current_value 
                  for next_state in transitions)
    
    def is_weakly_decreasing(self, state_machine: StateMachine, state: Any) -> bool:
        """
        Check if the potential function weakly decreases (non-increasing) for all transitions.
        
        Args:
            state_machine: The state machine
            state: The state to check transitions from
            
        Returns:
            True if the potential function weakly decreases for all transitions
        """
        current_value = self.evaluate(state)
        transitions = state_machine.get_transitions(state)
        
        if not transitions:  # Final state
            return True
        
        return all(self.evaluate(next_state) <= current_value 
                  for next_state in transitions)


def verify_invariant_principle(state_machine: StateMachine, 
                               invariant: Invariant,
                               max_states: int = 10000) -> Tuple[bool, str]:
    """
    Verify the invariant principle for a state machine.
    
    The Invariant Principle states that if:
    1. P(initial_state) is true, and
    2. P is a preserved predicate
    Then P is an invariant (true for all reachable states).
    
    Args:
        state_machine: The state machine to verify
        invariant: The invariant to check
        max_states: Maximum number of states to check (for finite verification)
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Check initial state
    if not invariant.verify_initial_state(state_machine):
        return False, f"Invariant '{invariant.name}' does not hold for initial state"
    
    # BFS to check all reachable states
    visited = {state_machine.get_initial_state()}
    queue = [state_machine.get_initial_state()]
    states_checked = 0
    
    while queue and states_checked < max_states:
        state = queue.pop(0)
        states_checked += 1
        
        # Check if invariant holds for this state
        if not invariant.holds(state):
            return False, f"Invariant '{invariant.name}' does not hold for state: {state}"
        
        # Check if invariant is preserved
        if not invariant.verify_preserved(state_machine, state):
            return False, f"Invariant '{invariant.name}' is not preserved from state: {state}"
        
        # Add transitions to queue
        for next_state in state_machine.get_transitions(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    if states_checked >= max_states:
        return True, f"Invariant verified for {states_checked} reachable states (limit reached)"
    
    return True, f"Invariant verified for all {states_checked} reachable states"


def verify_termination(state_machine: StateMachine,
                      potential_function: PotentialFunction,
                      max_states: int = 10000) -> Tuple[bool, str]:
    """
    Verify that a state machine terminates using a potential function.
    
    If a potential function with natural number values is strictly decreasing,
    then the state machine must terminate.
    
    Args:
        state_machine: The state machine to verify
        potential_function: The potential function to use
        max_states: Maximum number of states to check
        
    Returns:
        Tuple of (terminates, message)
    """
    visited = {state_machine.get_initial_state()}
    queue = [state_machine.get_initial_state()]
    states_checked = 0
    
    while queue and states_checked < max_states:
        state = queue.pop(0)
        states_checked += 1
        
        # Check if potential function is strictly decreasing
        if not potential_function.is_strictly_decreasing(state_machine, state):
            return False, f"Potential function '{potential_function.name}' is not strictly decreasing from state: {state}"
        
        # Add transitions to queue
        for next_state in state_machine.get_transitions(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    return True, f"Termination verified using potential function for {states_checked} states"
