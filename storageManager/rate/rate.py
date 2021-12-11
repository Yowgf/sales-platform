"""rate class"""

class rate:
    dbCols = {
        "id": "SERIAL primary key",
        "caseId": "varchar(32)",
        "val": "int",
    }

    def __init__(self, caseId, val):
        self.caseId = caseId
        self.val = val
