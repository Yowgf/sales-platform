"""caseComment class"""

from utils import utils

class caseComment:
    def __init__(self, createdBy, comment, createdAt=utils.datetimeNow()):
        self.createdBy = createdBy
        self.comment = comment
        self.createdAt = createdAt
