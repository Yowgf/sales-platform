"""case class"""

from datetime import datetime
from utils import utils

from .caseStatus import caseStatus
from .caseComment import caseComment

class case:       
    titleValidRange = (1, 50)
    categoryValidRange = (1, 20)
    descriptionValidRange = (1, 1000)
    rateValidRange = (1, 5)

    dbCols = {
        "id": "varchar(32) primary key",
        "createdBy": "varchar(50)",
        "assignedTo": "varchar(50)",
        "title": "varchar({})".format(titleValidRange[1]),
        "description": "varchar({})".format(descriptionValidRange[1]),
        "rate": "int",
    }

    def __init__(self, caseId, createdBy):
        self.caseId = caseId
        self.createdBy = createdBy
        
        self.assignedTo = None
        self.title = None
        self.category = None
        self.description = None
        self.rate = None
 
        
        self.createdAt = utils.datetimeNow()
        self.status = caseStatus()
        self.comments = []
    
    def populate(self, title, category, description):
        self.title = title
        self.category = category
        self.description = description
        
        return self
    
    def checkTitle(self, title):
        utils.checkAttLenInRange("title", title, case.titleValidRange)
        
    def checkCategory(self, category):
        utils.checkAttLenInRange("category", category, case.categoryValidRange)
    
    def checkDescription(self, description):
        utils.checkAttLenInRange("description", description, case.descriptionValidRange)

    def checkRate(self, rate):
        utils.checkAttInRange("rate", rate, case.rateValidRange)
    
    def addComment(self, user, comment):
        self.comments.append(caseComment(user, comment))
        
    def assignTo(self, salesUser):
        self.assignedTo = salesUser

    def setRate(self, rate):
        self.rate = rate
        
    def updateUserRates(self, rate):
        self.assignedTo.updateRate(self.caseId, rate)
        for user in [comment.createdBy for comment in self.comments]:
            user.updateRate(self.caseId, rate)
    
    def __str__(self):
        stringifiedCase = ""
        
        # Date
        stringifiedCase += "\n{}\n\n".format(self.createdAt.prettyStr())

        # Please print the status first
        stringifiedCase += "Status: {}\n".format(self.status.get())
        
        assignedName = None
        if self.assignedTo != None:
            assignedName = self.assignedTo.name
        stringifiedCase += "Asignee: {}\n".format(assignedName)
        stringifiedCase += "Satisfaction rate: {}\n".format(self.rate)

        stringifiedCase += "Title: {}\n".format(self.title)
        stringifiedCase += "Category: {}\n".format(self.category)
        stringifiedCase += "Description: {}\n".format(self.description)

        # Comments have to be printed out one by one
        stringifiedCase += "Comments:\n"
        if len(self.comments) > 0:
            stringifiedCase += "\n"
        for comment in self.comments:
            stringifiedCase += "{} -- rate {} ({}): {}\n".format(
                comment.createdBy.name,
                comment.createdBy.getPrettyAverageRate(),
                comment.createdAt.prettyStr(),
                comment.comment
            )

        return stringifiedCase
        

