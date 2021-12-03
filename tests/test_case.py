import pytest

from utils import utils

from storageManager.case.case import case
from storageManager.case.caseComment.caseComment import caseComment

class TestCase:
    def create_newCase():
        newCase = case()
        return newCase
    
    def test_longTitleRaiseException(self):
        with pytest.raises(Exception):
            case.checkTitle("1,2,3,4,5,6,7,8,9,10,11,12,13,14,15.")