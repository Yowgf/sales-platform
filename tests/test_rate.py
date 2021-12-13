import pytest

from storageManager.rate.rate import rate

class TestRate:

    @pytest.fixture
    def newRate(self):
        return rate("caseId", "val")

    def test_init(self, newRate):
        assert (
            newRate.caseId == "caseId" and
            newRate.val == "val"
        )
