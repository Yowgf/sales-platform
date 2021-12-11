"""caseComment class"""

from utils import utils

class caseComment:
    dbCols = {
        "id": "SERIAL primary key",
        "createdBy": "varchar(50)",
        # TODO: make this attribute of time type -aholmquist 2021-12-10
        "createdAt": "varchar(50)",
        "comment": "varchar(1000)",
    }

    def __init__(self, createdBy, comment, createdAt = utils.datetimeNow()):
        self.createdBy = createdBy
        self.comment = comment
        self.createdAt = createdAt
