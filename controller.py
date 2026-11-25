import sys
import userInterface
import csv
from CTkTable import CTkTable
import sqlite3
import user_services
import book_services

class AppController:
	##initialize
	def __init__(self, view):
		self.view = view
		self.view.set_controller(self)
		self.app_state = "login"
		self.patron_manager = user_services.ManagePatron()
		self.history = []
				
	def run(self):
		self.navigate("login")
		self.view.mainloop()
	
	## login	
	def login(self, username, password):
		user = self.patron_manager.verify_login(username, password)
		
		if user:
			self.history.clear()
			role = (user["user_type"]).strip().lower()

			if role  == "patron":
				self.navigate("patron_main")
			elif role  == "librarian":
				self.navigate("librarian_main")
			else:
				self.navigate("dual_usertype")
			return user
		
		self.view.error_popup("Invalid username or password.")
		return None
	
	## logout
	def logout(self):
		self.history.clear()
		self.navigate("login")
		
	## button call to change app_state	
	def navigate(self, new_state):
		self.app_state = new_state
		self.history.append(new_state)
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
