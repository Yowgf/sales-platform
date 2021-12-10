import pytest

from utils.testutils import sampleConfig as sample

class TestConfig:
    @pytest.fixture
    def sampleConfig(self):
        return sample()

    def test_ConfigInit(self, sampleConfig):
        assert sampleConfig.host == "127.0.0.1"
        assert sampleConfig.port == "1521"
        assert sampleConfig.database == "exampleDatabase"
        assert sampleConfig.user == "exampleUser"
        assert sampleConfig.password == "examplePassword"
        assert sampleConfig.connOpts == "sslmode=disable"
