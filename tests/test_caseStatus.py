import pytest

from utils import utils
from storageManager.case.caseStatus.caseStatus import caseStatus

class TestCaseStatus:
    def create_newCase():
        newCase = caseStatus()
        return newCase
    
    def test_DefaultStatusIsPendingAnalysis():
        newCase = TestCaseStatus.create_newCase()
        assert newCase.defaultStatus == "pending analysis"

    def test_DefaultStatusIsPendingAnalysisOnInitialization():
        newCase = TestCaseStatus.create_newCase()
        assert newCase.status == "pending analysis"

    def test_CanSetStatusToPendingResponse():
        newCase = TestCaseStatus.create_newCase()
        newCase.set(newCase.pendingResponse)
        assert newCase.status == "pending response"

    def test_CanSetStatusToUnderAnalysis():
        newCase = TestCaseStatus.create_newCase()
        newCase.set(newCase.underAnalysis)
        assert newCase.status == "under analysis"
        
    def test_CanSetStatusToResolved():
        newCase = TestCaseStatus.create_newCase()
        newCase.set(newCase.resolved)
        assert newCase.status == "resolved"
    
    def test_InvalidCaseSetRaiseException():
        with pytest.raises(Exception):
            newCase = TestCaseStatus.create_newCase()
            invalidCase = "waiting for response"
            newCase.set(invalidCase)

    def test_GetReturnCurrentStatus():
        newCase = TestCaseStatus.create_newCase()
        newCase.set("resolved")
        assert newCase.get() == "resolved"