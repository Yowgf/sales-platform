from sys import argv

from userInterface import consoleInterface
from storageManager import storageManager

def main():
    sm = storageManager(argv)
    ui = consoleInterface(sm)
    ui.run()
    
main()