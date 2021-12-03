import pytest
from utils.utils import inRange
from utils.utils import checkAttLenInRange


class TestInRange:

  def test_isInRangeMid (self):
    rng = [0, 10]
    assert inRange(5, rng) is True

  def test_isInRangeLowerBound (self):
    rng = [0, 10]
    assert inRange(0, rng) is True

  def test_isInRangeUpperBound (self):
    rng = [0, 10]
    assert inRange(10, rng) is True

  def test_isNotInRange (self):
    rng = [0, 10]
    assert inRange(-1, rng) is False
    assert inRange(11, rng) is False

class TestCheckAttLenInRange:
    with pytest.raises(Exception):
        checkAttLenInRange("test value", 10, [0,5])