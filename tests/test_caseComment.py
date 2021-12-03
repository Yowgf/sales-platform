import pytest

# from utils import utils
from storageManager.case.caseComment.caseComment import caseComment

class TestCaseComment:

  @pytest.fixture
  def create_newCommmet():
   newComment = caseComment.caseComment("Leona Vanessa", "Recomendo bastante")
   return newComment

  def test_CanDefineCreatedBy (self, create_newCommmet):
    assert create_newCommmet.createdBy == "Leona Vanessa"

  def test_CanDefineComment (self, create_newCommmet):
    assert create_newCommmet.comment == "Recomendo bastante"

  # def test_CanDefineCommentDatetime (self, createNewComment):
  #   assert createNewComment.newComment.createdAt.formalStr == createNewComment.createdAt.formalStr
  #   assert createNewComment.newComment.createdAt.prettyStr == createNewComment.createdAt.prettyStr