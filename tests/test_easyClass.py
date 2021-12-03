import pytest
from easyClass import Stack

class TestStack:

  @pytest.fixture
  def setUp(self):
    self.stack = Stack()

  def test_EmptyStack(self):
    self.assertTrue(self.stack.is_empty())

  def test_NotEmptyStack(self):
    self.stack.push(10)
    self.assertFalse(self.stack.is_empty())

  def test_SizeStack(self):
    self.stack.push(10)
    self.stack.push(20)
    self.stack.push(30)
    size = self.stack.size
    self.assertEqual(3, size)

  def test_PushPopStack(self):
    self.stack.push(10)
    self.stack.push(20)
    self.stack.push(30)
    self.stack.pop()
    result = self.stack.pop()
    self.assertEqual(20, result)

  def test_EmptyStackException(self):
    self.stack.push(10)
    self.stack.pop()
    with self.assertRaises(Exception):
      self.stack.pop()
