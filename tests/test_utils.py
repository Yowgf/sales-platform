import pytest
from utils.utils import inRange
from utils.utils import checkAttLenInRange
from utils.utils import setIfExists

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

class TestSetIfExists:
    @pytest.fixture
    def M(self):
        return {"k": "v1"}
    def test_NeverRaisesException(self):
        try:
            setIfExists("vdefault", {}, "unexistant_key")
            setIfExists("vdefault", {"existant_key": "existant_val"}, "existant_key")
        except:
            assert False, "set if exists (utility) should never raise exception"

    def test_ReturnValIfKeyExists(self, M):
        res = setIfExists("vdefault", M, "k")
        assert res == "v1"

    def test_ReturnDefaultIfNoKey(self, M):
        res = setIfExists("vdefault", M, "unexistant_key")
        assert res == "vdefault"
