# State-Machines
Repository for documenting various use cases of state machines (for learning purposes only)

## Examples

### 1. Message Receipt Confirmation State Machine

A practical implementation of a state machine for tracking message delivery status, similar to messaging apps like WhatsApp or Telegram.

**File:** `message_receipt_state_machine.py`

#### States
- **SENT**: Message has been sent but not yet delivered
- **DELIVERED**: Message has been delivered to recipient's device  
- **READ**: Message has been read by the recipient

#### State Transitions
```
[None] --send()--> [SENT] --deliver()--> [DELIVERED] --mark_as_read()--> [READ]
```

#### Features
- Clear state transitions with validation
- Timestamps for each state transition
- Error handling for invalid transitions
- Human-readable status messages with checkmarks (✓, ✓✓)

#### Usage

```python
from message_receipt_state_machine import Message

# Create a message
msg = Message(
    content="Did you get my last message",
    sender="Alice",
    recipient="Bob"
)

# Send the message
msg.send()
print(msg.get_status())  # ✓ Sent at 2026-02-11 05:12:51

# Mark as delivered
msg.deliver()
print(msg.get_status())  # ✓✓ Delivered at 2026-02-11 05:12:52

# Mark as read
msg.mark_as_read()
print(msg.get_status())  # ✓✓ Read at 2026-02-11 05:12:53
```

#### Running the Demo
```bash
python message_receipt_state_machine.py
```

#### Running Tests
```bash
python test_message_receipt_state_machine.py
```

## Learning Resources

State machines are a fundamental concept in computer science used to model systems with well-defined states and transitions. Common use cases include:
- Message delivery tracking
- Order processing workflows
- Game character states
- Network protocol implementations
- UI navigation flows
