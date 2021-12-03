"""caseComment class"""
import datetime
from utils import utils

class caseComment:
    def __init__(self, createdBy, comment):
        self.createdBy = createdBy
        self.comment = comment
        
        self.createdAt = datetime.datetime.now()
