"""
Message Receipt Confirmation State Machine

This module demonstrates a state machine for tracking message delivery status.
Common use case in messaging applications (like WhatsApp, Telegram, etc.)

States:
- SENT: Message has been sent but not yet delivered
- DELIVERED: Message has been delivered to recipient's device
- READ: Message has been read by the recipient

Transitions:
- send() -> SENT
- deliver() -> DELIVERED (from SENT)
- read() -> READ (from DELIVERED)
"""

from enum import Enum
from typing import Optional
from datetime import datetime


class MessageState(Enum):
    """Enumeration of possible message states"""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


class InvalidTransitionError(Exception):
    """Raised when an invalid state transition is attempted"""
    pass


class Message:
    """
    Represents a message with receipt confirmation tracking.
    
    This class implements a state machine for message delivery status.
    
    State Machine Behavior:
    ----------------------
    States: None -> SENT -> DELIVERED -> READ
    
    Valid Transitions:
    - send(): None -> SENT (initial state transition)
    - deliver(): SENT -> DELIVERED (message reaches recipient)
    - mark_as_read(): DELIVERED -> READ (recipient reads message)
    
    Invalid Transitions (will raise InvalidTransitionError):
    - Calling send() when already in any state
    - Calling deliver() when not in SENT state
    - Calling mark_as_read() when not in DELIVERED state
    
    Example:
    --------
    >>> msg = Message("Hello", "Alice", "Bob")
    >>> msg.send()
    >>> msg.deliver()
    >>> msg.mark_as_read()
    >>> print(msg.state)
    MessageState.READ
    """
    
    def __init__(self, content: str, sender: str, recipient: str):
        """
        Initialize a new message.
        
        Args:
            content: The message content
            sender: The sender identifier
            recipient: The recipient identifier
        """
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self._state = None
        self.sent_at: Optional[datetime] = None
        self.delivered_at: Optional[datetime] = None
        self.read_at: Optional[datetime] = None
    
    @property
    def state(self) -> Optional[MessageState]:
        """Get the current state of the message"""
        return self._state
    
    def send(self) -> None:
        """
        Send the message.
        
        Transitions the message to SENT state.
        
        Raises:
            InvalidTransitionError: If message has already been sent
        """
        if self._state is not None:
            raise InvalidTransitionError(
                f"Cannot send message that is already in {self._state.value} state"
            )
        
        self._state = MessageState.SENT
        self.sent_at = datetime.now()
    
    def deliver(self) -> None:
        """
        Mark the message as delivered.
        
        Transitions the message from SENT to DELIVERED state.
        
        Raises:
            InvalidTransitionError: If message is not in SENT state
        """
        if self._state != MessageState.SENT:
            raise InvalidTransitionError(
                f"Cannot deliver message in {self._state} state. Message must be in SENT state."
            )
        
        self._state = MessageState.DELIVERED
        self.delivered_at = datetime.now()
    
    def mark_as_read(self) -> None:
        """
        Mark the message as read.
        
        Transitions the message from DELIVERED to READ state.
        
        Raises:
            InvalidTransitionError: If message is not in DELIVERED state
        """
        if self._state != MessageState.DELIVERED:
            raise InvalidTransitionError(
                f"Cannot mark message as read in {self._state} state. "
                f"Message must be in DELIVERED state."
            )
        
        self._state = MessageState.READ
        self.read_at = datetime.now()
    
    def get_status(self) -> str:
        """
        Get a human-readable status string.
        
        Returns:
            A string describing the current message status
        """
        if self._state is None:
            return "Not sent"
        elif self._state == MessageState.SENT:
            return f"✓ Sent at {self.sent_at.strftime('%Y-%m-%d %H:%M:%S')}"
        elif self._state == MessageState.DELIVERED:
            return f"✓✓ Delivered at {self.delivered_at.strftime('%Y-%m-%d %H:%M:%S')}"
        elif self._state == MessageState.READ:
            return f"✓✓ Read at {self.read_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def __repr__(self) -> str:
        """String representation of the message"""
        return (
            f"Message(from={self.sender}, to={self.recipient}, "
            f"state={self._state.value if self._state else 'unsent'}, "
            f"content='{self.content[:20]}...')"
        )


if __name__ == "__main__":
    # Example usage
    print("=== Message Receipt Confirmation State Machine Demo ===\n")
    
    # Create a new message
    msg = Message(
        content="Did you get my last message?",
        sender="Alice",
        recipient="Bob"
    )
    
    print(f"Initial state: {msg.get_status()}")
    print(f"{msg}\n")
    
    # Send the message
    msg.send()
    print(f"After sending: {msg.get_status()}")
    print(f"{msg}\n")
    
    # Deliver the message
    import time
    time.sleep(1)  # Simulate network delay
    msg.deliver()
    print(f"After delivery: {msg.get_status()}")
    print(f"{msg}\n")
    
    # Mark as read
    time.sleep(1)  # Simulate user reading the message
    msg.mark_as_read()
    print(f"After reading: {msg.get_status()}")
    print(f"{msg}\n")
    
    # Demonstrate invalid transitions
    print("=== Testing Invalid Transitions ===\n")
    
    try:
        msg.send()  # Can't send again
    except InvalidTransitionError as e:
        print(f"❌ Error: {e}\n")
    
    # Create another message and try to read before delivery
    msg2 = Message("Hello!", "Bob", "Alice")
    msg2.send()
    
    try:
        msg2.mark_as_read()  # Can't read before delivery
    except InvalidTransitionError as e:
        print(f"❌ Error: {e}\n")
    
    print("Demo complete!")
