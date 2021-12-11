import pytest
from sys import argv

from config.config import config
from utils.testutils import sampleConfig, sampleCase, sampleUser
from storageManager.storageManager import storageManager
from storageManager.case.case import case
from keys import keys

class TestStorageManager:
    @pytest.fixture
    def sampleSM(self):
        return storageManager(sampleConfig())

    # Unit tests
    def test_init(self, sampleSM):
        assert sampleSM.userType_customer == "customer"
        assert sampleSM.userType_sales == "sales"
        assert sampleSM.userType_all == "all"

    def test_assignCaseTo(self, sampleSM):
        scase = sampleCase()
        suser = sampleUser()
        sampleSM.assignCaseTo(scase, suser)
        assert scase.assignedTo == suser      

    def test_setRate_CaseNotAssigned(self, sampleSM):
        scase = sampleCase()
        sampleSM.setRate(scase, 4)
        assert scase.rate.val == 4

    def test_setRate_CaseAssigned(self, sampleSM):
        scase = sampleCase()
        suser = sampleUser()
        sampleSM.assignCaseTo(scase, suser)
        sampleSM.setRate(scase, 4)
        assert scase.rate.val == 4
        assert suser.averageRate == 4

# Integration tests. These require that 'config.yaml' exists and is configured
# properly. Also, there has to be a live database on the configured endpoint.

    # This one includes a configured database
    @pytest.fixture
    def fullSample(self):
        sm = storageManager(config([]))
        sm.initFromDatabase()
        return sm

    @pytest.mark.integtest
    def test_initDatabase(self, fullSample):
        # TODO: verify at least that the tables exist in the database, after
        # initialization
        pass

    @pytest.mark.integtest
    def test_newUser(self, fullSample):
        origUser = sampleUser()
        userAttList = [origUser.email, origUser.name, origUser.type, origUser.password]
        newUser = fullSample.newUser(*userAttList)
        assert origUser == newUser
        # Now for the integration part. Let's check if the user has
        # been registered in the database.
        result = fullSample.db.selectStarWhereEqual(keys.userTable, {
            "email": newUser.email,
            "name": newUser.name,
            "type": newUser.type,
            "password": newUser.password,
        })
        assert len(result) == 1
        assert list(result[0]) == userAttList

    @pytest.mark.integtest
    def test_newCase(self, fullSample):
        su = sampleUser()
        c = case("exampleId", su)
        c = fullSample.populateCase(c, "exampleTitle", "exampleCategory", "exampleDescription")
        result = fullSample.db.selectStarWhereEqual(keys.caseTable, {
            "id": c.caseId,
            "createdBy": c.createdBy.email,
            "title": c.title,
            "category": c.category,
            "description": c.description,
        })
        assert len(result) == 1
        assert list(result[0]) == [
            c.caseId,
            c.createdBy.email,
            "", # When case starts, it is not assigned to anyone
            c.title,
            c.category,
            c.description,
        ]
