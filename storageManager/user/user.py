"""user class"""

from numpy import mean

from .userRate.userRate import userRate

class user:
    def __init__(self, email, name, type, password):
        self.email = email
        self.name = name
        self.type = type
        self.password = password
        
        self.ratesList = []
        self.averageRate = None

    def updateRate(self, caseId, rate):
        if not isinstance(rate, int):
            raise ValueError("rate has to be an integer")
            
        # The int(rate) here should not raise an exception. We expect this
        # check to be done earlier in the code.
        caseIdIndex = None
        try:
            caseIdIndex = [r.caseId for r in self.ratesList].index(caseId)
        except ValueError:
            self.ratesList.append(userRate(caseId, rate))
            self.averageRate = mean([r.rate for r in self.ratesList])
            return self
        
        self.ratesList[caseIdIndex].rate = rate
        self.averageRate = mean([r.rate for r in self.ratesList])
        
        return self
        
    def getPrettyAverageRate(self):
        if self.averageRate != None:
            return round(self.averageRate, 1)
        return None
