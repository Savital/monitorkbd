# Savital https://github.com/Savital
# main.py launch script

from manager import Manager

def main():
    controller = Manager()
    controller.runApp()
    Manager.runApp(Manager)

main()
