"""storageManager class

This class is the high-level interface to data manipulation procedures in the
application. Sometimes, we will have functions, like 'newCase', just to avoid
having to import an internal package from the UI.
"""

from uuid import uuid4

from keys import keys
from .case import case
from .case.caseComment.caseComment import caseComment
from .rate import rate
from .case.caseStatus import caseStatus
from .user import user
from .dbi.dbi import dbi
from .errors.emailTaken import emailTaken

from utils.testutils import sampleUsers

class storageManager:

    def __init__(self, config):
        self.config = config
        self.cases = {}
        
        self.userType_customer = "customer"
        self.userType_sales = "sales"
        self.userType_all = "all" # Artificial wildcard user type
        self.userTypes = [self.userType_customer, self.userType_sales, self.userType_all]
        
        self.users = sampleUsers()
        
        self.currentUser = None

        self.db = None

    def __del__(self):
        if self.db != None:
            self.db.close()

    # login returns True if login succeded, or False otherwise.
    def login(self, email, password):
        if (
            email in self.users.keys() and
            self.users[email].password == password
        ):
            self.currentUser = self.users[email]
            return True
        else:
            return False
        
    def logout(self):
        self.currentUser = None

################################################################
# Utility functions
################################################################

    # Returns an unique object id -- one that not in the given array.
    def findIdNotIn(self, array):
        newId = uuid4().hex
        while newId in array:
            newId = uuid4().hex
        return newId

################################################################
# CRUD actions
################################################################

# CASES

    def newCase(self):
        caseId = self.findIdNotIn(self.cases.keys())
        c = case(caseId, self.users[self.currentUser.name])
        self.cases[caseId] = c
        return c

    def populateCase(self, case, *args):
        case.populate(*args)
        self.db.registerCase(case)
        return case
            
    def addCaseComment(self, case, comment):
        case.addComment(self.currentUser, comment)

    def getCasesByUserType(self, userType):
        if userType == self.userType_all:
            return [self.cases[caseId]
                    for caseId in self.cases.keys()]
        if userType == self.userType_customer:
            return [self.cases[caseId]
                    for caseId in self.cases.keys()
                    if self.cases[caseId].createdBy == self.currentUser]
        elif userType == self.userType_sales:
            return [self.cases[caseId]
                    for caseId in self.cases.keys()
                    if self.cases[caseId].assignedTo == self.currentUser]
        else:
            raise ValueError("Unsupported user type {}".format(userType))

    def assignCaseTo(self, case, salesUser):
        crate = case.getRate()
        if crate != None:
            salesUser.updateRate(case.caseId, crate.val)
        case.assignTo(salesUser)
        
    def getAllCaseStatuses(self):
        return caseStatus().allStatuses
    
    def setCaseStatus(self, case, status):
        return case.status.set(status)
    
    # Checks if rate is in valid range and sets it
    def setRate(self, case, rate):
        rate = int(rate)
        case.checkRate(rate)
        if case.assignedTo != None:
            case.updateUserRates(rate)
        return case.setRate(rate)

# USERS

    # TODO: make interface in console to register a user -aholmquist 2021-12-10
    def newUser(self, email, name, type, password):
        if email in [e for e in self.users.keys()]:
            raise emailTaken(email)
        u = user(email, name, type, password)
        self.db.registerUser(u)
        return u

# DATABASE STUFF

    def initFromDatabase(self):
        self.db = dbi(self.config)
        self.db.connect()
        self.createDatabaseTables(self.db)
        self.populateFromDatabase(self.db)

    def createDatabaseTables(self, db):
        db.createTable(keys.commentTable, caseComment.dbCols)
        db.createTable(keys.rateTable, rate.dbCols)
        db.createTable(keys.caseTable, case.dbCols)
        db.createTable(keys.userTable, user.dbCols)

    def populateFromDatabase(self, db):
        # self._fetchUsersFromDatabase(db)
        self._fetchCasesFromDatabase(db)

    def _fetchUsersFromDatabase(self, db):
        queryResults = db.selectStar(keys.userTable)
        for result in queryResults:
            userEmail = result[0]
            userName = result[1]
            userType = result[2]
            userPassword = result[3]
            self.users[userEmail] = user(userEmail, userName, userType, userPassword)

    def _fetchCasesFromDatabase(self, db):
        queryResults = db.selectStar(keys.caseTable)
        for result in queryResults:
            caseId = result[0]
            createdBy = result[1]
            self.cases[caseId] = case(caseId, createdBy)
