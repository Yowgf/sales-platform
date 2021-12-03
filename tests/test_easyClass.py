import pytest
from . import easyClass

class TestStack:

  @pytest.fixture
  def setUp(self):
    self.easyClass = easyClass()

  def test_EmptyStack(self):
    self.assertTrue(self.easyClass.is_empty())

  def test_NotEmptyStack(self):
    self.easyClass.push(10)
    self.assertFalse(self.easyClass.is_empty())

  def test_SizeStack(self):
    self.easyClass.push(10)
    self.easyClass.push(20)
    self.easyClass.push(30)
    size = self.easyClass.size
    self.assertEqual(3, size)

  def test_PushPopStack(self):
    self.easyClass.push(10)
    self.easyClass.push(20)
    self.easyClass.push(30)
    self.easyClass.pop()
    result = self.easyClass.pop()
    self.assertEqual(20, result)

  def test_EmptyStackException(self):
    self.easyClass.push(10)
    self.easyClass.pop()
    with self.assertRaises(Exception):
      self.easyClass.pop()
