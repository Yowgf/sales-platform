import pytest
from sys import argv
import psycopg2

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
    def test_initUserType_customer(self, sampleSM):
        assert sampleSM.userType_customer == "customer"

    def test_initUserType_sales(self, sampleSM):
        assert sampleSM.userType_sales == "sales"
        
    def test_initUserType_all(self, sampleSM):
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
    
    def test_wrongLogin(self, sampleSM):
        assert sampleSM.login("wrong email", "wrong password") == False

# Integration tests. These require that 'config.yaml' exists and is configured
# properly. Also, there has to be a live database on the configured endpoint.

    # This one includes a configured database. It restarts the tables afresh,
    # to make sure we don't see remnants from previous runs.
    @pytest.fixture
    def fullSample(self):
        sm = storageManager(config([]))
        sm.initDatabase()
        sm.dropDatabaseTables(sm.db)
        sm.createDatabaseTables(sm.db)
        sm.populateFromDatabase(sm.db)
        return sm

    @pytest.mark.integtest
    def test_initDatabase(self, fullSample):

        try:
            for table in keys.allTables:
                fullSample.db.pingTable(table)
        except psycopg2.errors.UndefinedTable as e:
            assert False, "Expected that table would exist: {}".format(e)

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

    # When we create a case, a case status is also created, by default
    @pytest.mark.integtest
    def test_newCase_createsCaseStatusRecord(self, fullSample):
        su = sampleUser()
        c = fullSample.newCase(usr=su)
        status = c.getStatus()
        result = fullSample.db.selectStarWhereEqual(keys.caseStatusTable, {
            "id": 1,
            "status": status.status,
        })
        assert len(result) == 1
        assert list(result[0]) == [
            1,
            status.status,
        ]

    @pytest.mark.integtest
    def test_populateCase(self, fullSample):
        c = sampleCase()
        c = fullSample.populateCase(c, "examleTitle", "exampleCategory", "exampleDescription")
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
    
    @pytest.mark.integtest
    def test_addCaseComment(self, fullSample):
        commentStr = "exampleComment"
        scase = sampleCase()
        comm = fullSample.addCaseComment(scase, commentStr, user=scase.createdBy)
        result = fullSample.db.selectStarWhereEqual(keys.commentTable, {
            "id": 1,
            "createdBy": comm.createdBy.email,
            "createdAt": comm.createdAt.formalStr(),
            "comment": comm.comment,
        })
        assert len(result) == 1
        assert list(result[0]) == [
            1,
            comm.createdBy.email,
            comm.createdAt.formalStr(),
            comm.comment,
        ]
