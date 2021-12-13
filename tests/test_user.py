import pytest

from storageManager.user.user import user

class TestUser:
    
    @pytest.fixture
    def newUser(self):
        return user("email", "name", "type", "password")
    
    def test_prettyAverageIsRoundedCorrectly(self, newUser):
        newUser = newUser.updateRate("caseId1", 3)
        newUser = newUser.updateRate("caseId2", 5)
        newUser = newUser.updateRate("caseId3", 5)
        assert newUser.getPrettyAverageRate() == 4.3

    def test_eq_True(self, newUser):
        assert newUser == user("email", "name", "type", "password")

    def test_eq_False(self, newUser):
        # Change type
        assert newUser != user("email", "name", "type2", "password")
