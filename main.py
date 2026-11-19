from controller import AppController
from userInterface import ManageUserInterface
import sys
	
def main(args):
	UI = ManageUserInterface()
	app = AppController(UI)
	app.run()
	
	return 
	
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
