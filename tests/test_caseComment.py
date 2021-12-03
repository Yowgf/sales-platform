import pytest

from utils import utils
from storageManager.case.caseComment.caseComment import caseComment

class TestCaseComment:
    datetime = utils.datetime.now()
    
    @pytest.fixture
    def create_newCommmet(self):
        self.newComment = caseComment("Leona Vanessa", "Recomendo bastante", TestCaseComment.datetime)

    # def create_newCommmet(create_newCommmet):
    #     newComment = caseComment("Leona Vanessa", "Recomendo bastante", TestCaseComment.datetime)
    #     return newComment

    def test_CanDefineCreatedBy (self, create_newCommmet):
        assert self.newComment.createdBy == "Leona Vanessa"

    def test_CanDefineComment (self):
        assert self.newComment .comment == "Recomendo bastante"

    def test_CanDefineCommentDatetime (self):
        assert self.newComment .createdAt == TestCaseComment.datetime
