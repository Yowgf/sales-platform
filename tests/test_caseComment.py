import pytest

from utils import utils
from storageManager.case.caseComment.caseComment import caseComment

class TestCaseComment:

  def create_newCommmet():
   newComment = caseComment("Leona Vanessa", "Recomendo bastante", "2021-12-03 18:34:27.041293")
   return newComment

  def test_CanDefineCreatedBy (self):
    assert TestCaseComment.create_newCommmet().createdBy == "Leona Vanessa"

  def test_CanDefineComment (self):
    assert TestCaseComment.create_newCommmet().comment == "Recomendo bastante"

  def test_CanDefineCommentDatetime (self, createNewComment):
    assert TestCaseComment.create_newCommmet().createdAt.dt == "2021-12-01 18:32:45.623971"