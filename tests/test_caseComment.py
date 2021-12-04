import pytest

from utils import utils
from storageManager.case.caseComment.caseComment import caseComment

class TestCaseComment:
    datetime = utils.datetime.now()

    @pytest.fixture
    def newComment(self):
        return caseComment("Leona Vanessa", "Recomendo bastante", TestCaseComment.datetime)

    def test_CanDefineCreatedBy (self, newComment):
        assert newComment.createdBy == "Leona Vanessa"

    def test_CanDefineComment (self, newComment):
        assert newComment.comment == "Recomendo bastante"

    def test_CanDefineCommentDatetime (self, newComment):
        assert newComment.createdAt == TestCaseComment.datetime
