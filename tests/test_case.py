import pytest

from utils import utils

from storageManager.case.case import case
from storageManager.case.caseComment.caseComment import caseComment

class TestCase:
    def create_newCase():
        newCase = case()
        return newCase
    
    def makeLongWord(size):
        return '1'*size
    
    def test_longTitleRaiseException(self):
        with pytest.raises(Exception):
            longTitle = TestCase.makeLongWord(30)
            case.checkTitle(longTitle)
    
    
    def test_longCategoryRaiseException(self):
        with pytest.raises(Exception):
            longCategory = TestCase.makeLongWord(20)
            case.checkCategory(longCategory)

    def test_longDescriptionRaiseException(self):
        with pytest.raises(Exception):
            longDescription = TestCase.makeLongWord(1000)
            case.checkCategory(longDescription)