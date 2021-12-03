"""case class"""

from datetime import datetime
from utils import utils

from .caseStatus import caseStatus
from .caseComment import caseComment

class case:
    def __init__(self, createdBy):
        self.createdBy = createdBy
        self.assignedTo = None
        self.title = None
        self.category = None
        self.description = None
        
        self.titleValidRange = (1, 30)
        self.categoryValidRange = (1, 20)
        self.descriptionValidRange = (1, 1000)
        
        self.createdAt = utils.datetimeNow()
        self.status = caseStatus()
        self.comments = []
    
    def populate(self, title, category, description):
        self.title = title
        self.category = category
        self.description = description
    
    def checkTitle(self, title):
        utils.checkAttLenInRange("title", title, self.titleValidRange)
        
    def checkCategory(self, category):
        utils.checkAttLenInRange("category", category, self.categoryValidRange)
    
    def checkDescription(self, description):
        utils.checkAttLenInRange("description", description, self.descriptionValidRange)
    
    def addComment(self, user, comment):
        self.comments.append(caseComment(user.name, comment))
        
    def assignTo(self, salesUser):
        self.assignedTo = salesUser
    
    def __str__(self):
        stringifiedCase = ""
        
        # Date
        stringifiedCase += "\n{}\n\n".format(self.createdAt.prettyStr())

        # Please print the status first
        stringifiedCase += "Status: {}\n".format(self.status.get())

        stringifiedCase += "Title: {}\n".format(self.title)
        stringifiedCase += "Category: {}\n".format(self.category)
        stringifiedCase += "Description: {}\n".format(self.description)

        # Comments have to be printed out one by one
        stringifiedCase += "Comments:\n"
        if len(self.comments) > 0:
            stringifiedCase += "\n"
        for comment in self.comments:
            stringifiedCase += "{} ({}): {}\n".format(comment.createdBy,
                                                      comment.createdAt.prettyStr(),
                                                      comment.comment)

        return stringifiedCase
        