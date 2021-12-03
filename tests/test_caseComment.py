import pytest

from utils import utils
from storageManager.case.caseComment.caseComment import caseComment

class TestCaseComment:

  @pytest.fixture
  def createNewComment ():
    createdBy = "Leona Vanessa"
    comment = "Recomendo bastante"
    # createdAt = utils.datetimeNow()
    newComment = caseComment(createdBy, comment)

  def test_CanDefineCreatedBy (self, createNewComment):
    assert createNewComment.newComment.createdBy == createNewComment.createdBy

  def test_CanDefineCommentMessage (self, createNewComment):
    assert createNewComment.newComment.comment == createNewComment.comment

  # def test_CanDefineCommentDatetime (self, createNewComment):
  #   assert createNewComment.newComment.createdAt.formalStr == createNewComment.createdAt.formalStr
  #   assert createNewComment.newComment.createdAt.prettyStr == createNewComment.createdAt.prettyStr