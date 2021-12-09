import pytest

from config.config import config
from storageManager.storageManager import storageManager

class TestStorageManager:
    @pytest.fixture
    def sampleSM(self):
        return storageManager(config.sampleConfig())
    
    def test_init(self, sampleSM):
        assert sampleSM.userType_customer == "customer"
        assert sampleSM.userType_sales == "sales"
        assert sampleSM.userType_all == "all"
