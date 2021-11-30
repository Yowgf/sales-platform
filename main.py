from interaction_manager import interaction_manager
from storage_manager import storage_manager

def main():
    sm = storage_manager()
    im = interaction_manager(sm)
    im.run()

main()
