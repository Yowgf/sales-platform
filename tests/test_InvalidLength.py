import pytest
from errors.InvalidLength import InvalidLength

class TestInvalidLengthExeceptionRaised:
    with pytest.raises(Exception):
        InvalidLength("testing value", [0,1])