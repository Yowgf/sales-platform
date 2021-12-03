"""storageManager class

This class is the high-level interface to data manipulation procedures in the
application. Sometimes, we will have functions, like 'newCase', just to avoid
having to import an internal package from the UI.
"""

from uuid import uuid4

from .case import case
from .case.caseStatus import caseStatus
from .user import user

class storageManager:
    # TODO: make users and cases data persistent in a database -aholmquist 2021-11-29
    def __init__(self):
        self.cases = {}
        
        self.userType_customer = "customer"
        self.userType_sales = "sales"
        self.userType_all = "all" # Artificial wildcard user type
        self.userTypes = [self.userType_customer, self.userType_sales, self.userType_all]
        
        self.users = {
            "daniel@email.com": user("daniel@email.com", "Daniel", "customer", "password321"),
            "joseph@email.com": user("joseph@email.com", "Joseph", "sales", "password123"),
            "c": user("c", "c", "customer", "c"),
            "s": user("s", "s", "sales", "s"),
        }
        
        self.currentUser = None

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

    def newCase(self):
        caseId = self.findIdNotIn(self.cases.keys())
        c = case(self.currentUser)
        self.cases[caseId] = c
        return c
            
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
        case.assignTo(salesUser)
        
    def getAllCaseStatuses(self):
        return caseStatus().allStatuses
    
    def setCaseStatus(self, case, status):
        return case.status.set(status)
        