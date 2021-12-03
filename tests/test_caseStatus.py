import pytest

from utils import utils
from storageManager.case.caseStatus.caseStatus import caseStatus

class TestCaseStatus:
    def create_newCase():
        newCase = caseStatus()
        return newCase
    
    def test_DefaultStatusIsPendingAnalysis(self):
        newCase = TestCaseStatus.create_newCase()
        assert newCase.defaultStatus == "pending analysis"

    def test_CanSetStatusToPendingResponse(self):
        newCase = TestCaseStatus.create_newCase()
        newCase.set(newCase.pendingResponse)
        assert newCase.status == "pending response"

    def test_CanSetStatusToUnderAnalysis(self):
        newCase = TestCaseStatus.create_newCase()
        newCase.set(newCase.underAnalysis)
        assert newCase.status == "under analysis"
        
    def test_CanSetStatusToResolved(self):
        newCase = TestCaseStatus.create_newCase()
        newCase.set(newCase.resolved)
        assert newCase.status == "resolved"
    
    def test_InvalidCaseSetRaiseException(self):
        with pytest.raises(Exception):
            newCase = TestCaseStatus.create_newCase()
            invalidCase = "waiting for response"
            newCase.set(invalidCase)

    def test_GetReturnCurrentStatus(self):
        newCase = TestCaseStatus.create_newCase()
        newCase.set("resolved")
        assert newCase.get() == "resolved"