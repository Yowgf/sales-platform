from sys import exit

from userInterface import consoleInterface
from storageManager import storageManager

def main():
    sm = storageManager()
    ui = consoleInterface(sm)
    ui.run()

main()