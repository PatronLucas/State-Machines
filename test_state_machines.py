"""
Unit tests for state machine implementation
"""

import unittest
from state_machine import StateMachine
from examples import (
    create_turnstile,
    create_binary_divisible_by_3,
    create_even_ones_counter,
    create_mod_counter,
)


class TestStateMachine(unittest.TestCase):
    """Test the basic StateMachine class."""
    
    def test_initialization(self):
        """Test state machine initialization."""
        sm = StateMachine(
            states={'A', 'B'},
            initial_state='A',
            transitions={('A', 'x'): 'B', ('B', 'y'): 'A'},
            accepting_states={'B'}
        )
        self.assertEqual(sm.current_state, 'A')
        self.assertIn('A', sm.states)
        self.assertIn('B', sm.states)
        self.assertIn('B', sm.accepting_states)
    
    def test_invalid_initial_state(self):
        """Test that invalid initial state raises error."""
        with self.assertRaises(ValueError):
            StateMachine(
                states={'A', 'B'},
                initial_state='C',
                transitions={}
            )
    
    def test_transition(self):
        """Test basic state transitions."""
        sm = StateMachine(
            states={'A', 'B'},
            initial_state='A',
            transitions={('A', 'x'): 'B', ('B', 'y'): 'A'}
        )
        self.assertEqual(sm.current_state, 'A')
        sm.transition('x')
        self.assertEqual(sm.current_state, 'B')
        sm.transition('y')
        self.assertEqual(sm.current_state, 'A')
    
    def test_invalid_transition(self):
        """Test that invalid transition raises error."""
        sm = StateMachine(
            states={'A', 'B'},
            initial_state='A',
            transitions={('A', 'x'): 'B'}
        )
        with self.assertRaises(ValueError):
            sm.transition('y')  # No transition defined for ('A', 'y')
    
    def test_reset(self):
        """Test resetting the state machine."""
        sm = StateMachine(
            states={'A', 'B'},
            initial_state='A',
            transitions={('A', 'x'): 'B', ('B', 'y'): 'A'}
        )
        sm.transition('x')
        self.assertEqual(sm.current_state, 'B')
        sm.reset()
        self.assertEqual(sm.current_state, 'A')
    
    def test_process_sequence(self):
        """Test processing a sequence of inputs."""
        sm = StateMachine(
            states={'A', 'B', 'C'},
            initial_state='A',
            transitions={
                ('A', 'x'): 'B',
                ('B', 'y'): 'C',
                ('C', 'z'): 'A'
            }
        )
        final_state = sm.process_sequence(['x', 'y', 'z'])
        self.assertEqual(final_state, 'A')
    
    def test_accepts(self):
        """Test the accepts method."""
        sm = StateMachine(
            states={'A', 'B'},
            initial_state='A',
            transitions={('A', 'x'): 'B', ('B', 'y'): 'A'},
            accepting_states={'B'}
        )
        self.assertTrue(sm.accepts(['x']))
        self.assertFalse(sm.accepts(['x', 'y']))
        self.assertTrue(sm.accepts(['x', 'y', 'x']))


class TestTurnstile(unittest.TestCase):
    """Test the turnstile state machine."""
    
    def setUp(self):
        self.turnstile = create_turnstile()
    
    def test_initial_state(self):
        """Turnstile should start locked."""
        self.assertEqual(self.turnstile.current_state, 'LOCKED')
    
    def test_coin_unlocks(self):
        """Inserting a coin should unlock the turnstile."""
        self.turnstile.transition('coin')
        self.assertEqual(self.turnstile.current_state, 'UNLOCKED')
    
    def test_push_when_unlocked_locks(self):
        """Pushing when unlocked should lock the turnstile."""
        self.turnstile.transition('coin')
        self.turnstile.transition('push')
        self.assertEqual(self.turnstile.current_state, 'LOCKED')
    
    def test_push_when_locked_stays_locked(self):
        """Pushing when locked should keep it locked."""
        self.turnstile.transition('push')
        self.assertEqual(self.turnstile.current_state, 'LOCKED')
    
    def test_coin_when_unlocked_stays_unlocked(self):
        """Inserting coin when unlocked should keep it unlocked."""
        self.turnstile.transition('coin')
        self.turnstile.transition('coin')
        self.assertEqual(self.turnstile.current_state, 'UNLOCKED')
    
    def test_sequence(self):
        """Test a sequence of operations."""
        sequence = ['coin', 'push', 'push', 'coin', 'coin', 'push']
        final = self.turnstile.process_sequence(sequence)
        self.assertEqual(final, 'LOCKED')


class TestBinaryDivisibleBy3(unittest.TestCase):
    """Test the binary divisibility by 3 state machine."""
    
    def setUp(self):
        self.div3 = create_binary_divisible_by_3()
    
    def test_zero(self):
        """0 is divisible by 3."""
        self.assertTrue(self.div3.accepts('0'))
    
    def test_three(self):
        """11 (binary) = 3 (decimal) is divisible by 3."""
        self.assertTrue(self.div3.accepts('11'))
    
    def test_six(self):
        """110 (binary) = 6 (decimal) is divisible by 3."""
        self.assertTrue(self.div3.accepts('110'))
    
    def test_nine(self):
        """1001 (binary) = 9 (decimal) is divisible by 3."""
        self.assertTrue(self.div3.accepts('1001'))
    
    def test_twelve(self):
        """1100 (binary) = 12 (decimal) is divisible by 3."""
        self.assertTrue(self.div3.accepts('1100'))
    
    def test_five(self):
        """101 (binary) = 5 (decimal) is not divisible by 3."""
        self.assertFalse(self.div3.accepts('101'))
    
    def test_seven(self):
        """111 (binary) = 7 (decimal) is not divisible by 3."""
        self.assertFalse(self.div3.accepts('111'))


class TestEvenOnesCounter(unittest.TestCase):
    """Test the even ones counter state machine."""
    
    def setUp(self):
        self.even_ones = create_even_ones_counter()
    
    def test_empty_string(self):
        """Empty string has 0 ones (even)."""
        self.assertTrue(self.even_ones.accepts(''))
    
    def test_all_zeros(self):
        """String of all 0s has 0 ones (even)."""
        self.assertTrue(self.even_ones.accepts('0000'))
    
    def test_two_ones(self):
        """String with 2 ones should be accepted."""
        self.assertTrue(self.even_ones.accepts('0101'))
        self.assertTrue(self.even_ones.accepts('1010'))
    
    def test_four_ones(self):
        """String with 4 ones should be accepted."""
        self.assertTrue(self.even_ones.accepts('1111'))
    
    def test_one_one(self):
        """String with 1 one should be rejected."""
        self.assertFalse(self.even_ones.accepts('1'))
        self.assertFalse(self.even_ones.accepts('0010'))
    
    def test_three_ones(self):
        """String with 3 ones should be rejected."""
        self.assertFalse(self.even_ones.accepts('111'))
        self.assertFalse(self.even_ones.accepts('0111'))


class TestModCounter(unittest.TestCase):
    """Test the modulo counter state machine."""
    
    def test_mod_3_counter(self):
        """Test a mod-3 counter."""
        mod3 = create_mod_counter(3)
        
        # Start at S0 (accepting)
        self.assertTrue(mod3.is_accepting())
        
        # After 1 tick: S1 (not accepting)
        mod3.transition('tick')
        self.assertFalse(mod3.is_accepting())
        
        # After 2 ticks: S2 (not accepting)
        mod3.transition('tick')
        self.assertFalse(mod3.is_accepting())
        
        # After 3 ticks: S0 (accepting)
        mod3.transition('tick')
        self.assertTrue(mod3.is_accepting())
    
    def test_mod_5_counter(self):
        """Test a mod-5 counter."""
        mod5 = create_mod_counter(5)
        
        # Process 12 ticks
        for _ in range(12):
            mod5.transition('tick')
        
        # 12 mod 5 = 2, so should be in state S2
        self.assertEqual(mod5.current_state, 'S2')
        self.assertFalse(mod5.is_accepting())


if __name__ == '__main__':
    unittest.main()
