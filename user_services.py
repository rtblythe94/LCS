import sqlite3

class ManagePatron:
	## load and init ManagePatron class with data from users.csv
	def __init__(self, filepath="users.db"):
		self.filepath = filepath
		self.active_user = None
			
	def search_patrons(self, query):
		## search database for patron names
		search_term = f"%{query.strip()}%"
		with self.connect_database() as con:
			results = con.execute("SELECT * FROM users WHERe username LIKE ? AND user_type = 'patron'",
			(search_term,)).fetchall()
			return [tuple(row) for row in results]
	
##	def add_patron
	
##	def update_phone_number
	
##	def update_patron_address
	
##	def update_patron_email
	
##	def delete_patron

	def verify_login(self, username, password):
		with self.connect_database() as con:
			user = con.execute("SELECT * FROM users WHERE username = ? AND password = ?",
			(username, password)).fetchone()
		self.active_user = user["username"]
		return dict(user)
		
	def connect_database(self):
		## open user database
		users = sqlite3.connect("users.db")
		users.row_factory = sqlite3.Row
		return users
						
	def get_all_users(self):
		with self.connect_database() as con:
			cursor = con.execute("SELECT * FROM users")
			return cursor.fetchall()
		
	def get_active_user(self):
		## query active user
		return self.active_user
		
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
