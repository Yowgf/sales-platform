import pytest
from utils.utils import inRange
from utils.utils import checkAttLenInRange

from errors.InvalidLength import InvalidLength

class TestInRange:

    @pytest.fixture
    def sampleRange(self):
        return (0, 10)
    
    def test_isInRangeMid (self, sampleRange):
        assert inRange(5, sampleRange) is True

    def test_isInRangeLowerBound (self, sampleRange):
        assert inRange(0, sampleRange) is True

    def test_isInRangeUpperBound (self, sampleRange):
        assert inRange(10, sampleRange) is True

    def test_isNotInRange (self, sampleRange):
        assert inRange(-1, sampleRange) is False
        assert inRange(11, sampleRange) is False

class TestCheckAttLenInRange:
    
    @pytest.fixture
    def sampleRange(self):
        return (0, 10)
    
    def test_IsInRangeNoException(self, sampleRange):
        try:
            checkAttLenInRange("attribute", "1" * (sampleRange[1] - 1), sampleRange)
        except InvalidLength:
            assert False, "Should not raise invalid length exception when in range"
        
    def test_IsNotInRangeRaisesException(self, sampleRange):
        with pytest.raises(InvalidLength):
            checkAttLenInRange("attribute", "1" * (sampleRange[1] + 1), sampleRange)
