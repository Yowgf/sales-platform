import pytest

from utils.testutils import sampleConfig as sample

class TestConfig:
    @pytest.fixture
    def sampleConfig(self):
        return sample()

    def test_ConfigInitHost(self, sampleConfig):
        assert sampleConfig.host == "127.0.0.1"
    
    def test_ConfigInitPort(self, sampleConfig):
        assert sampleConfig.port == "1521"

    def test_ConfigInitDatabase(self, sampleConfig):
        assert sampleConfig.database == "exampleDatabase"

    def test_ConfigInitUser(self, sampleConfig):
        assert sampleConfig.user == "exampleUser"

    def test_ConfigInitPassword(self, sampleConfig):
        assert sampleConfig.password == "examplePassword"

    def test_ConfigInitConnOpts(self, sampleConfig):
        assert sampleConfig.connOpts == "sslmode=disable"
