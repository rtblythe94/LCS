import sys
import userInterface
import csv
from CTkTable import CTkTable
import sqlite3

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
		
####################################################################################
############## login/logout ########################################################
####################################################################################			
	def login(self, username, password):
		data = self.connect_database()
		user = data.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
		data.close()
		
		if user and user["password"] == password:
			self.history.clear()			
			if user["user_type"] =="Patron":
				self.navigate("patron_main")
			elif user["user_type"] == "Librarian":
				self.navigate("librarian_main")
			else:
				self.navigate("dual_usertype")
			return user

		self.view.error_popup("Invalid username or password.")
		return None
		
	## open user database
	def connect_database(self):	
		users = sqlite3.connect("users.db")
		users.row_factory = sqlite3.Row
		users.execute("""
			CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT UNIQUE NOT NULL,
			password TEXT NOT NULL,
			user_type TEXT DEFAULT 'patron'
			)
			""")
		users.commit()
		return users
							
	## log user out
	def logout(self):
		self.history.clear()
		self.navigate("login")
		

	## load csv file containing books and assemble table
	def load_book_database(self):
		with open("books.csv", mode='r', newline='') as file:
			return list(csv.reader(file))
	
	## button call to change app_state	
	def navigate(self, new_state):
		##self.userInterface.clear_window()
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
