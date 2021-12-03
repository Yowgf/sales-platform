from sys import exit

from userInterface import consoleInterface
from storageManager import storageManager

def main():
    sm = storageManager()
    ui = consoleInterface(sm)
    ui.run()

if __name__ == "__main__":
    main()
else:
    print("Only console mode is supported", file=sys.stderr)
    exit(1)
