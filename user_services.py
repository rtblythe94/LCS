import sqlite3

class ManagePatron:
	## load and init ManagePatron class with data from users.csv
	def __init__(self, filepath="users.db"):
		self.filepath = filepath

##	def get_username
	
##	def search_patron
	
##	def add_patron
	
##	def update_phone_number
	
##	def update_patron_address
	
##	def update_patron_email
	
##	def delete_patron

	def verify_login(self, username, password):
		with self.connect_database() as con:
			user = con.execute("SELECT * FROM users WHERE username = ? AND password = ?",
			(username, password)).fetchone()
		return dict(user) if user else None
		
	def connect_database(self):
		## open user database
		users = sqlite3.connect("users.db")
		users.row_factory = sqlite3.Row
		return users
				
	def get_all_users(self):
		with self.connect_database() as con:
			cursor = con.execute("SELECT * FROM users")
			return cursor.fetchall()
			
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
