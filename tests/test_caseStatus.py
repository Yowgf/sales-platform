import pytest

from utils import utils
from storageManager.case.caseStatus.caseStatus import caseStatus

class TestCaseStatus:
    @pytest.fixture
    def newCase(self):
        return caseStatus()
    
    def test_DefaultStatusIsPendingAnalysis(self, newCase):
        assert newCase.defaultStatus == "pending analysis"

    def test_CanSetStatusToPendingResponse(self, newCase):
        newCase.set(newCase.pendingResponse)
        assert newCase.status == "pending response"

    def test_CanSetStatusToUnderAnalysis(self, newCase):
        newCase.set(newCase.underAnalysis)
        assert newCase.status == "under analysis"
        
    def test_CanSetStatusToResolved(self, newCase):
        newCase.set(newCase.resolved)
        assert newCase.status == "resolved"
    
    def test_InvalidCaseSetRaiseException(self, newCase):
        with pytest.raises(Exception):
            invalidCase = "waiting for response"
            newCase.set(invalidCase)

    def test_GetReturnCurrentStatus(self, newCase):
        newCase.set("resolved")
        assert newCase.get() == "resolved"
