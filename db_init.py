import sqlite3

conn = sqlite3.connect("users.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        patron_phone INTEGER,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
        )
    """)
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Mjin", "Mingxian", "Jin", "9109876543", "Password", "Librarian", "mjin@uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Rblythe", "Robert", "Blythe", "3361234567","Password", "Patron","rblythe@uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Rbasurto", "Ricardo", "Basurto", "3369876543", "Password", "Patron&Librarian","rbasurto@broncos.uncfsu.edu")
     )
conn.commit()
conn.close()
