class Stack:

  def __init__(self):
    self.elements = []
    self.size = 0

  def is_empty(self):
    return self.size == 0

  def push(self, elem):
    self.elements.append(elem)
    self.size += 1

  def pop(self):
    if self.is_empty():
      raise Exception("Stack is empty :(")
    elem = self.elements.pop(self.size - 1)
    self.size -= 1
    return elem