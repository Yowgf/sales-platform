import pytest
from errors.InvalidLength import InvalidLength

class TestInvalidLengthExeceptionRaised:
    with pytest.raises(Exception):
      raise InvalidLength("10", [0,1])