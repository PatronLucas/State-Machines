# Message Receipt Confirmation State Machine Diagram

This document provides a visual representation of the message receipt confirmation state machine.

## State Transition Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  Message Receipt Confirmation State Machine                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

    ┌─────────┐
    │  Start  │
    │ (None)  │
    └────┬────┘
         │
         │ send()
         │
         ▼
    ┌─────────┐
    │  SENT   │  ✓
    │         │
    └────┬────┘
         │
         │ deliver()
         │
         ▼
    ┌──────────┐
    │DELIVERED │  ✓✓
    │          │
    └────┬─────┘
         │
         │ mark_as_read()
         │
         ▼
    ┌─────────┐
    │  READ   │  ✓✓
    │         │
    └─────────┘


## State Descriptions

| State       | Symbol | Description                                    |
|-------------|--------|------------------------------------------------|
| None        | -      | Message has been created but not yet sent      |
| SENT        | ✓      | Message sent but not delivered                 |
| DELIVERED   | ✓✓     | Message delivered to recipient's device        |
| READ        | ✓✓     | Message has been read by the recipient         |


## Valid Transitions

| From State  | Action          | To State    |
|-------------|-----------------|-------------|
| None        | send()          | SENT        |
| SENT        | deliver()       | DELIVERED   |
| DELIVERED   | mark_as_read()  | READ        |


## Invalid Transitions (will raise InvalidTransitionError)

| From State  | Invalid Action  | Why Invalid                                  |
|-------------|-----------------|----------------------------------------------|
| SENT        | send()          | Message is already sent                      |
| DELIVERED   | send()          | Message is already sent                      |
| READ        | send()          | Message is already sent                      |
| None        | deliver()       | Message must be sent first                   |
| DELIVERED   | deliver()       | Message is already delivered                 |
| READ        | deliver()       | Message is already delivered and read        |
| None        | mark_as_read()  | Message must be delivered first              |
| SENT        | mark_as_read()  | Message must be delivered first              |
| READ        | mark_as_read()  | Message is already read                      |


## Example Flow

```python
from message_receipt_state_machine import Message

# Step 1: Create message
msg = Message(
    content="Did you get my last message?",
    sender="Alice",
    recipient="Bob"
)
# State: None
# Status: "Not sent"

# Step 2: Send message
msg.send()
# State: SENT
# Status: "✓ Sent at 2026-02-11 12:00:00"

# Step 3: Message is delivered
msg.deliver()
# State: DELIVERED  
# Status: "✓✓ Delivered at 2026-02-11 12:00:05"

# Step 4: Recipient reads message
msg.mark_as_read()
# State: READ
# Status: "✓✓ Read at 2026-02-11 12:01:00"
```


## Real-World Applications

This state machine pattern is used in many messaging applications:

- **WhatsApp**: Single checkmark (sent), double checkmark (delivered), blue double checkmark (read)
- **Telegram**: Single checkmark (sent), double checkmark (delivered), no visual indicator for read
- **iMessage**: "Delivered" and "Read" receipts
- **SMS**: Delivery reports in some carriers
- **Email**: Read receipts

Each implementation may have slight variations, but the core state machine concept remains the same.
