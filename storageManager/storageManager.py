"""storageManager class

This class is the high-level interface to data manipulation procedures in the
application. Sometimes, we will have functions, like 'newCase', just to avoid
having to import an internal package from the UI.
"""

from uuid import uuid4

from .case import case

class storageManager:
    # TODO: make users and cases data persistent in a database -aholmquist 2021-11-29
    def __init__(self):
        self.cases = {}
        
        self.userType_customer = "customer"
        self.userType_sales = "sales"
        self.userTypes = [self.userType_customer, self.userType_sales]
        
        self.users = {
            "daniel@email.com": {
                "name": "Daniel",
                "type": "customer",
                "password": "password321",
            },
            "joseph@email.com": {
                "name": "Joseph",
                "type": "sales",
                "password": "password123",
            },
            "c": {
                "name": "c",
                "type": "customer",
                "password": "c",
            },
            "s": {
                "name": "s",
                "type": "sales",
                "password": "s",
            },
        }
        
        self.currentUser = None


    # login returns True if login succeded, or False otherwise.
    def login(self, email, password):
        if (
            email in self.users.keys() and
            self.users[email]["password"] == password
        ):
            self.currentUser = self.users[email]
            return True
        else:
            return False

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
            
    def addCaseComment(self, caseId, comment):
        self.cases[caseId].addComment(comment)

    def getCasesByCurrentUser(self):
        return [self.cases[caseId]
                for caseId in self.cases.keys()
                if self.cases[caseId].createdBy == self.currentUser]
        