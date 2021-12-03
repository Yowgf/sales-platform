from typing import ClassVar
import pytest

from utils import utils

from storageManager.case.case import case
from storageManager.user.user import user
from storageManager.case.caseComment.caseComment import caseComment

class TestCase:

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

    def test_NewCasesAreCreatedWithoutComments (self):
        newCase = case("Anyone")
        assert len(newCase.comments) == 0
    
    def test_NewCasesAreCreatedWithNoPersonAssinged (self):
        newCase = case("Anyone")
        assert newCase.assignedTo == None

    def test_NewCasesAreCreatedWithNoTitle (self):
        newCase = case("Anyone")
        assert newCase.title == None

    def test_NewCasesAreCreatedWithNoCategory (self):
        newCase = case("Anyone")
        assert newCase.category == None

    def test_NewCasesAreCreatedWithNoDescription (self):
        newCase = case("Anyone")
        assert newCase.description == None

    def test_CanCreateCommentsOnCases (self):
        newCase = case("Anyone")
        user1 = user("email", "name", "type", "password")
        comment1 = "Some comments..."
        newCase.addComment(user1, comment1)

        assert newCase.comments[0].createdBy == user1.name, "User that created the comment is diffenrent than expected"
        assert newCase.comments[0].comment == comment1, "Comment created is diffenrent than expected"
    
    def test_CanPopulateCases (self):
        newCase = case("Anyone")
        title = "Some title..."
        category = "Some category..."
        description = "Some description..."
        newCase.populate(title, category, description)

        assert newCase.title == title, "Case title is diffenrent than expected"
        assert newCase.category == category, "Case category is diffenrent than expected"
        assert newCase.description == description, "Case description is diffenrent than expected"
    
    def test_CanAssignPersonToCase (self):
        newCase = case("Anyone")
        person = "Zerima Asoit"
        newCase.assignedTo(person)
        assert newCase.assignedTo == person