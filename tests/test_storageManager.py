import pytest

from utils.testutils import sampleConfig, sampleCase, sampleUser
from storageManager.storageManager import storageManager

class TestStorageManager:
    @pytest.fixture
    def sampleSM(self):
        return storageManager(sampleConfig())
    
    # Unit tests
    def test_init(self, sampleSM):
        assert sampleSM.userType_customer == "customer"
        assert sampleSM.userType_sales == "sales"
        assert sampleSM.userType_all == "all"

    def test_setRate_CaseNotAssigned(self, sampleSM):
        scase = sampleCase()
        sampleSM.setRate(scase, 4)
        assert scase.rate == 4

    def test_setRate_CaseAssigned(self, sampleSM):
        scase = sampleCase()
        suser = sampleUser()
        sampleSM.assignCaseTo(scase, suser)
        sampleSM.setRate(scase, 4)
        assert scase.rate == 4
        assert suser.averageRate == 4

    # Integration tests
    def test_initDatabase(self, sampleSM):
        # TODO
        pass
