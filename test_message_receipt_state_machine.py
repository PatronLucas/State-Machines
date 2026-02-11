"""
Unit tests for the Message Receipt Confirmation State Machine
"""

import unittest
from datetime import datetime
from message_receipt_state_machine import (
    Message,
    MessageState,
    InvalidTransitionError
)


class TestMessageStateMachine(unittest.TestCase):
    """Test cases for the Message state machine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.message = Message(
            content="Test message",
            sender="Alice",
            recipient="Bob"
        )
    
    def test_initial_state(self):
        """Test that a new message has no state"""
        self.assertIsNone(self.message.state)
        self.assertIsNone(self.message.sent_at)
        self.assertIsNone(self.message.delivered_at)
        self.assertIsNone(self.message.read_at)
    
    def test_send_message(self):
        """Test sending a message"""
        self.message.send()
        
        self.assertEqual(self.message.state, MessageState.SENT)
        self.assertIsNotNone(self.message.sent_at)
        self.assertIsInstance(self.message.sent_at, datetime)
        self.assertIsNone(self.message.delivered_at)
        self.assertIsNone(self.message.read_at)
    
    def test_deliver_message(self):
        """Test delivering a message"""
        self.message.send()
        self.message.deliver()
        
        self.assertEqual(self.message.state, MessageState.DELIVERED)
        self.assertIsNotNone(self.message.sent_at)
        self.assertIsNotNone(self.message.delivered_at)
        self.assertIsNone(self.message.read_at)
        self.assertGreaterEqual(self.message.delivered_at, self.message.sent_at)
    
    def test_mark_as_read(self):
        """Test marking a message as read"""
        self.message.send()
        self.message.deliver()
        self.message.mark_as_read()
        
        self.assertEqual(self.message.state, MessageState.READ)
        self.assertIsNotNone(self.message.sent_at)
        self.assertIsNotNone(self.message.delivered_at)
        self.assertIsNotNone(self.message.read_at)
        self.assertGreaterEqual(self.message.read_at, self.message.delivered_at)
    
    def test_complete_flow(self):
        """Test the complete message flow"""
        # Start with no state
        self.assertIsNone(self.message.state)
        
        # Send
        self.message.send()
        self.assertEqual(self.message.state, MessageState.SENT)
        
        # Deliver
        self.message.deliver()
        self.assertEqual(self.message.state, MessageState.DELIVERED)
        
        # Read
        self.message.mark_as_read()
        self.assertEqual(self.message.state, MessageState.READ)
    
    def test_cannot_send_twice(self):
        """Test that a message cannot be sent twice"""
        self.message.send()
        
        with self.assertRaises(InvalidTransitionError) as context:
            self.message.send()
        
        self.assertIn("already in", str(context.exception))
    
    def test_cannot_deliver_unsent_message(self):
        """Test that an unsent message cannot be delivered"""
        with self.assertRaises(InvalidTransitionError) as context:
            self.message.deliver()
        
        self.assertIn("must be in SENT state", str(context.exception))
    
    def test_cannot_read_undelivered_message(self):
        """Test that an undelivered message cannot be read"""
        self.message.send()
        
        with self.assertRaises(InvalidTransitionError) as context:
            self.message.mark_as_read()
        
        self.assertIn("must be in DELIVERED state", str(context.exception))
    
    def test_cannot_deliver_read_message(self):
        """Test that a read message cannot be delivered again"""
        self.message.send()
        self.message.deliver()
        self.message.mark_as_read()
        
        with self.assertRaises(InvalidTransitionError) as context:
            self.message.deliver()
        
        self.assertIn("must be in SENT state", str(context.exception))
    
    def test_cannot_read_sent_message(self):
        """Test that a sent (but not delivered) message cannot be read"""
        self.message.send()
        
        with self.assertRaises(InvalidTransitionError) as context:
            self.message.mark_as_read()
        
        self.assertIn("must be in DELIVERED state", str(context.exception))
    
    def test_get_status_not_sent(self):
        """Test status string for unsent message"""
        status = self.message.get_status()
        self.assertEqual(status, "Not sent")
    
    def test_get_status_sent(self):
        """Test status string for sent message"""
        self.message.send()
        status = self.message.get_status()
        self.assertIn("✓ Sent at", status)
    
    def test_get_status_delivered(self):
        """Test status string for delivered message"""
        self.message.send()
        self.message.deliver()
        status = self.message.get_status()
        self.assertIn("✓✓ Delivered at", status)
    
    def test_get_status_read(self):
        """Test status string for read message"""
        self.message.send()
        self.message.deliver()
        self.message.mark_as_read()
        status = self.message.get_status()
        self.assertIn("✓✓ Read at", status)
    
    def test_message_attributes(self):
        """Test message attributes are set correctly"""
        msg = Message("Hello World", "User1", "User2")
        
        self.assertEqual(msg.content, "Hello World")
        self.assertEqual(msg.sender, "User1")
        self.assertEqual(msg.recipient, "User2")
    
    def test_repr(self):
        """Test string representation of message"""
        repr_str = repr(self.message)
        
        self.assertIn("Alice", repr_str)
        self.assertIn("Bob", repr_str)
        self.assertIn("unsent", repr_str)
        
        self.message.send()
        repr_str = repr(self.message)
        self.assertIn("sent", repr_str)


class TestMessageStateEnum(unittest.TestCase):
    """Test cases for MessageState enum"""
    
    def test_enum_values(self):
        """Test that enum values are correct"""
        self.assertEqual(MessageState.SENT.value, "sent")
        self.assertEqual(MessageState.DELIVERED.value, "delivered")
        self.assertEqual(MessageState.READ.value, "read")
    
    def test_enum_comparison(self):
        """Test enum comparison"""
        self.assertEqual(MessageState.SENT, MessageState.SENT)
        self.assertNotEqual(MessageState.SENT, MessageState.DELIVERED)


if __name__ == "__main__":
    unittest.main()
