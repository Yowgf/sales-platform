import pytest

from utils import utils
from storageManager.case.caseComment.caseComment import caseComment

class TestCaseComment:
    datetime = utils.datetime.now()

    def create_newCommmet():
        newComment = caseComment("Leona Vanessa", "Recomendo bastante", TestCaseComment.datetime)
        return newComment

    def test_CanDefineCreatedBy (self):
        assert TestCaseComment.create_newCommmet().createdBy == "Leona Vanessa"

    def test_CanDefineComment (self):
        assert TestCaseComment.create_newCommmet().comment == "Recomendo bastante"

    def test_CanDefineCommentDatetime (self):
        assert TestCaseComment.create_newCommmet().createdAt == TestCaseComment.datetime
