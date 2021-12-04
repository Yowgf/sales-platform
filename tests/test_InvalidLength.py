import pytest
from errors.InvalidLength import InvalidLength

class TestInvalidLengthException:
    
    @pytest.fixture
    def sampleInvalidException(self):
        return InvalidLength("attribute", (0, 1))
    
    def test_InvalidLengthExceptionContainsGivenParameters(self, sampleInvalidException):
        for subStr in ["attribute", "(0, 1)"]:
            assert subStr in sampleInvalidException.__str__()
