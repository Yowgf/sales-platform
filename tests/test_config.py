import pytest
import tempfile

from utils.testutils import sampleConfig
from config.config import *

def sampleConfigList():
    return [
        "-host=127.0.0.1",
        "-port=1521",
        "-database=exampleDatabase",
        "-user=exampleUser",
        "-password=examplePassword",
        "-connOpts=sslmode=disable",
    ]

class TestConfig:
    @pytest.fixture
    def sample(self):
        return sampleConfig()

    def test_ConfigInitHost(self, sample):
        assert sample.host == "127.0.0.1"
    
    def test_ConfigInitPort(self, sample):
        assert sample.port == "1521"

    def test_ConfigInitDatabase(self, sample):
        assert sample.database == "exampleDatabase"

    def test_ConfigInitUser(self, sample):
        assert sample.user == "exampleUser"

    def test_ConfigInitPassword(self, sample):
        assert sample.password == "examplePassword"

    def test_ConfigInitConnOpts(self, sample):
        assert sample.connOpts == "sslmode=disable"

    def test_checkMissingFlagsNoRaiseMissingFlags(self, sample):
        C = sample.C
        try:
            config.checkMissingFlags(C)
        except missingFlags:
            assert False, "Should not have raised the missingFlags exception"

    def test_checkMissingFlagsRaisesMissingFlags(self, sample):
        C = sample.C
        C.pop("host") # Remove required flag, should raise an exception
        with pytest.raises(missingFlags):
            config.checkMissingFlags(C)

    def test_cliOverridesFile(self):
        tempFile = tempfile.NamedTemporaryFile(mode='w+t', prefix="sales-platform-configTest_",
            suffix=".yaml")
        tempFile.write(
"""
host: hostFromFile
database: databaseFromFile
user: userFromFile
password: passwordFromFile
"""
        )
        tempFile.close()

        cliArgs = sampleConfigList()
        allArgs = cliArgs
        list.append(allArgs, "-config-file={}".format(tempFile.name))
        cfg = config(allArgs)

        expectedC = config.parseList(allArgs)
        actualC = cfg.C
        # Assert that none of the CLI arguments were overriden by file config
        for k in expectedC.keys():
            assert expectedC[k] == actualC[k]