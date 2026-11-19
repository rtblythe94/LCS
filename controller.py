import sys
import userInterface
import csv
from CTkTable import CTkTable

class AppController:
	##initialize
	def __init__(self, view):
		self.view = view
		self.view.set_controller(self)
		self.app_state = "login"
		self.history = []
				
	def run(self):
		self.navigate("login")
		self.view.mainloop()
				
	## load csv file containing books and assemble table
	def load_book_database(self):
		with open("books.csv", mode='r', newline='') as file:
			return list(csv.reader(file))
	
	## button call to change app_state	
	def navigate(self, new_state):
		##self.userInterface.clear_window()
		self.app_state = new_state
		self.view.switchUI(new_state)
			
	## pop 1 from history to return to previous page on stack only if previous page exists
	def return_page(self):
		if len(self.history) > 1:
			self.history.pop()
			previous_page = self.history[-1]
			self.app_state = previous_page
			self.view.switchUI(previous_page)
			
	## save data before closing app
	def exit_app(self):
		self.view.destroy()
		
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
