from sys import argv

from config.config import config
from userInterface import consoleInterface
from storageManager import storageManager

def main():
    cfg = config(argv)
    sm = storageManager(cfg)
    ui = consoleInterface(cfg, sm)
    ui.run()
    
main()