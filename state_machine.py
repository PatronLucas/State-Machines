"""
State Machine Implementation
Based on MIT OCW 6.1200J Mathematics for Computer Science - Lecture 4

A state machine is a mathematical model of computation consisting of:
- A finite set of states
- An initial state
- A set of transitions between states based on inputs
- Optionally, a set of accepting/final states
"""


class StateMachine:
    """
    A general-purpose state machine implementation.
    
    A state machine processes a sequence of inputs and transitions between
    states according to a transition function.
    
    Attributes:
        states: Set of valid states
        initial_state: The starting state
        transitions: Dictionary mapping (state, input) -> next_state
        accepting_states: Set of states that are considered "accepting" or final
        current_state: The current state of the machine
    """
    
    def __init__(self, states, initial_state, transitions, accepting_states=None):
        """
        Initialize a state machine.
        
        Args:
            states: Set or list of valid state names
            initial_state: The initial state (must be in states)
            transitions: Dict mapping (current_state, input) -> next_state
            accepting_states: Set/list of accepting states (optional)
        """
        self.states = set(states)
        self.initial_state = initial_state
        self.transitions = transitions
        self.accepting_states = set(accepting_states) if accepting_states else set()
        self.current_state = initial_state
        
        # Validate initial state
        if initial_state not in self.states:
            raise ValueError(f"Initial state '{initial_state}' not in states")
        
        # Validate accepting states
        if not self.accepting_states.issubset(self.states):
            raise ValueError("Accepting states must be a subset of states")
    
    def reset(self):
        """Reset the state machine to its initial state."""
        self.current_state = self.initial_state
    
    def transition(self, input_symbol):
        """
        Process an input and transition to the next state.
        
        Args:
            input_symbol: The input to process
            
        Returns:
            The new current state
            
        Raises:
            ValueError: If no transition is defined for (current_state, input)
        """
        key = (self.current_state, input_symbol)
        if key not in self.transitions:
            raise ValueError(
                f"No transition defined for state '{self.current_state}' "
                f"with input '{input_symbol}'"
            )
        
        self.current_state = self.transitions[key]
        return self.current_state
    
    def process_sequence(self, input_sequence):
        """
        Process a sequence of inputs.
        
        Args:
            input_sequence: Iterable of inputs to process
            
        Returns:
            The final state after processing all inputs
        """
        for input_symbol in input_sequence:
            self.transition(input_symbol)
        return self.current_state
    
    def accepts(self, input_sequence):
        """
        Check if the machine accepts the given input sequence.
        
        Args:
            input_sequence: Iterable of inputs to process
            
        Returns:
            True if the final state is an accepting state, False otherwise
        """
        self.reset()
        final_state = self.process_sequence(input_sequence)
        return final_state in self.accepting_states
    
    def is_accepting(self):
        """Check if the current state is an accepting state."""
        return self.current_state in self.accepting_states
    
    def __repr__(self):
        return (
            f"StateMachine(states={self.states}, "
            f"current_state='{self.current_state}', "
            f"accepting_states={self.accepting_states})"
        )
