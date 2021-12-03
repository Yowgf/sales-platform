import pytest
from errors.InvalidLength import InvalidLength

class TestInvalidLengthExeceptionRaised:
    with pytest.raises(Exception):
      try:
        False
      except (ValueError, InvalidLength) as err:
        InvalidLength("10", [0,1])