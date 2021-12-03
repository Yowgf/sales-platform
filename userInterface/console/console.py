"""console class"""

import os

class console:
    def __init__(self):
        self.numLines = 0
    
    def clear(self, numLines):
        self.numLines -= numLines
        if self.numLines < 0:
            self.numLines = 0
        for i in range(numLines):
            print ("\033[A{}\033[A".format(" " * os.get_terminal_size().columns))

    def clearAll(self):
        return self.clear(self.numLines)
            
    def countLines(self, message):
        message = str(message)
        numSlashN = message.count("\n")
        if len(message) == 0:
            return numSlashN
        return numSlashN + ((len(message) - 1) // os.get_terminal_size().columns)
    
    # consolePrint prints a message and increments number of printed lines.
    def print(self, message):
        # +1 because `print` already inserts a newline
        self.numLines += self.countLines(message) + 1
        print(message)
    
    # Get input from console and adjust the number of lines printed.
    def input(self, ask_message):
        # +1 because `input` already inserts a newline
        self.numLines += self.countLines(ask_message) + 1
        return input(ask_message)