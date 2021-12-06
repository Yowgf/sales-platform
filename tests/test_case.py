from typing import ClassVar
import pytest

from utils import utils

from storageManager.case.case import case
from storageManager.user.user import user
from storageManager.case.caseComment.caseComment import caseComment

from errors.InvalidLength import InvalidLength
from errors.InvalidValue import InvalidValue

class TestCase:

    @pytest.fixture
    def newCase(self):
        return case("caseId", "Anyone")
    
    def makeWord(size):
        return '1'*size
    
    def checkNotRaiseException(val, func):
        try:
            func(val)
        except (InvalidLength, InvalidValue) as err:
            assert False, "Should not have raised the exception"
            
    def checkRaiseExceptionIL(word, func):
        with pytest.raises(InvalidLength):
            func(word)
            
    def checkRaiseExceptionIV(val, func):
        with pytest.raises(InvalidValue):
            func(val)
            
    def test_normalTitleNotRaiseException(self, newCase):
        TestCase.checkNotRaiseException(TestCase.makeWord(newCase.titleValidRange[1] - 1),
                               newCase.checkTitle)
    
    def test_smallTitleRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIL(TestCase.makeWord(newCase.titleValidRange[0] - 1),
                                    newCase.checkTitle)
            
    def test_longTitleRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIL(TestCase.makeWord(newCase.titleValidRange[1] + 1),
                                    newCase.checkTitle)
    
    def test_normalCategoryNotRaiseException(self, newCase):
        TestCase.checkNotRaiseException(TestCase.makeWord(newCase.categoryValidRange[1] - 1),
                               newCase.checkCategory)
            
    def test_smallCategoryRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIL(TestCase.makeWord(newCase.categoryValidRange[0] - 1),
                               newCase.checkCategory)
            
    def test_longCategoryRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIL(TestCase.makeWord(newCase.categoryValidRange[1] + 1),
                               newCase.checkCategory)
        
    def test_normalDescriptionRaiseException(self, newCase):
        TestCase.checkNotRaiseException(TestCase.makeWord(newCase.descriptionValidRange[1] - 1),
                               newCase.checkDescription)
            
    def test_smallDescriptionRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIL(TestCase.makeWord(newCase.descriptionValidRange[0] - 1),
                               newCase.checkDescription)
        
    def test_longDescriptionRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIL(TestCase.makeWord(newCase.descriptionValidRange[1] + 1),
                               newCase.checkDescription)
        
    def test_normalRateRaiseException(self, newCase):
        TestCase.checkNotRaiseException(newCase.rateValidRange[1] - 1, newCase.checkRate)
            
    def test_smallRateRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIV(newCase.rateValidRange[0] - 1, newCase.checkRate)
        
    def test_longRateRaiseException(self, newCase):
        TestCase.checkRaiseExceptionIV(newCase.rateValidRange[1] + 1, newCase.checkRate)
        
    def test_NewCasesAreCreatedWithoutComments (self, newCase):
        assert len(newCase.comments) == 0
    
    def test_NewCasesAreCreatedWithNoPersonAssinged (self, newCase):
        assert newCase.assignedTo == None

    def test_NewCasesAreCreatedWithNoTitle (self, newCase):
        assert newCase.title == None

    def test_NewCasesAreCreatedWithNoCategory (self, newCase):
        assert newCase.category == None

    def test_NewCasesAreCreatedWithNoDescription (self, newCase):
        assert newCase.description == None
        
    def test_NewCasesAreCreatedWithNoRate (self, newCase):
        assert newCase.rate == None

    def test_CanCreateCommentsOnCases (self, newCase):
        user1 = user("email", "name", "type", "password")
        comment1 = "Some comments..."
        newCase.addComment(user1, comment1)

        assert newCase.comments[0].createdBy.name == user1.name, "User that created the comment is different than expected"
        assert newCase.comments[0].comment == comment1, "Comment created is different than expected"
    
    def test_CanPopulateCases (self, newCase):
        title = "Some title..."
        category = "Some category..."
        description = "Some description..."
        newCase.populate(title, category, description)

        assert newCase.title == title, "Case title is different than expected"
        assert newCase.category == category, "Case category is different than expected"
        assert newCase.description == description, "Case description is different than expected"
    
    def test_CanAssignPersonToCase (self, newCase):
        person = "Zerima Asoit"
        newCase.assignTo(person)
        assert newCase.assignedTo == person
        
    def test_CanUpdateUserRates (self, newCase):
        # Add comment and assign to someone
        sampleUser = user("email", "name", "type", "password")
        newCase.addComment(sampleUser, "comment")
        newCase.assignTo(sampleUser)
        
        # Before
        assert newCase.assignedTo.averageRate == None
        
        # Rate case
        newCase.updateUserRates(5)
        
        # After
        assert newCase.assignedTo.averageRate == 5
        assert newCase.comments[0].createdBy.averageRate == 5
        
    def test_StringifyContainsEssentialSubstrings(self, newCase):
        for word in ["Status", "Title", "Category", "Description", "Comments"]:
            assert word in newCase.__str__()
    