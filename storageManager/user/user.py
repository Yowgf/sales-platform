"""user class"""

from numpy import mean

from ..rate.rate import rate

class user:
    dbCols = {
        "email": "varchar(50) primary key",
        "name": "varchar(50)",
        "type": "varchar(15)",
        "password": "varchar(20)",
    }

    def __init__(self, email, name, type, password):
        self.email = email
        self.name = name
        self.type = type
        self.password = password
        
        self.ratesList = []
        self.averageRate = None

    def __eq__(self, other):
        if other == None:
            return False
        
        return (
            self.email == other.email and
            self.name == other.name and
            self.type == other.type and
            self.password == other.password and
            self.ratesList == other.ratesList and
            self.averageRate == other.averageRate
        )

    def updateRate(self, caseId, rateVal):
        if not isinstance(rateVal, int):
            raise ValueError("rateVal has to be an integer")
            
        # The int(rateVal) here should not raise an exception. We expect this
        # check to be done earlier in the code.
        caseIdIndex = None
        try:
            caseIdIndex = [r.caseId for r in self.ratesList].index(caseId)
        except ValueError:
            self.ratesList.append(rate(caseId, rateVal))
            self.averageRate = mean([r.val for r in self.ratesList])
            return self
        
        self.ratesList[caseIdIndex].val = rateVal
        self.averageRate = mean([r.val for r in self.ratesList])
        
        return self
        
    def getPrettyAverageRate(self):
        if self.averageRate != None:
            return round(self.averageRate, 1)
        return None
