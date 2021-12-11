"""
caseStatus class
"""

# Examples of status:
#   "resolved",
#   "under analysis",
#   "pending response" (waiting for customer to respond),
#   "pending analysis" (waiting for sales person to analyze the case). This is the status with which a case is created.
class caseStatus:
    dbCols = {
        "id": "SERIAL primary key",
        "status": "varchar(50)",
    }

    def __init__(self):
        self.pendingAnalysis = "pending analysis"
        self.pendingResponse = "pending response"
        self.underAnalysis = "under analysis"
        self.resolved = "resolved"
        self.allStatuses = [
            self.pendingAnalysis,
            self.pendingResponse,
            self.underAnalysis,
            self.resolved
        ]
        
        self.defaultStatus = self.pendingAnalysis
        
        self.status = self.defaultStatus

    def set(self, newStatus):
        if newStatus not in self.allStatuses:
            raise ValueError("invalid case status '{}'".format(newStatus))
        self.status = newStatus
        
    def get(self):
        return self.status
