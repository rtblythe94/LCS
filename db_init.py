import sqlite3

conn = sqlite3.connect("users.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        user_type TEXT,
        email TEXT UNIQUE NOT NULL
        )
    """)
conn.execute(
    "INSERT OR IGNORE INTO users (username, password, user_type, email) VALUES (?, ?,?,?)",
    ("Mjin", "Password", "Librarian", "mjin@uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, password, user_type, email) VALUES (?, ?,?,?)",
    ("Rblythe", "Password", "Patron","rblythe@uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, password, user_type, email) VALUES (?, ?,?,?)",
    ("Rbasurto", "Password", "Patron&Librarian","rbasurto@broncos.uncfsu.edu")
     )
conn.commit()
conn.close()
