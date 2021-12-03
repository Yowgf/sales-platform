import pytest
from easyClass.easyClass import easyClass

class TestEasyClass:

    @pytest.fixture
    def setUp(self):
        self.easyClass = easyClass()

    def test_EmptyStack(self, setUp):
        assert self.easyClass.is_empty() is True

    def test_NotEmptyStack(self, setUp):
        self.easyClass.push(10)
        assert self.easyClass.is_empty() is False
