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
    ("Mjin", "Mingxian", "Jin", "(336) 111-2222", "Password", "Librarian", "mjin@uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Rblythe", "Robert", "Blythe", "(336) 111-2222","Password", "Patron","rblythe@uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Rbasurto", "Ricardo", "Basurto", "(910) 333-4444", "Password", "Patron&Librarian","rbasurto@broncos.uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Aamjad", "Afifah", "amjad", "(910) 333-4444", "Password", "Librarian","aamjad@broncos.uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Nbowser", "Nyrell", "Bowser", "(434) 555-6666", "Password", "Patron","nbowser@broncos.uncfsu.edu")
     )
conn.execute(
    "INSERT OR IGNORE INTO users (username, first_name, last_name, patron_phone, password, user_type, email) VALUES (?, ?,?,?,?,?,?)",
    ("Ztaylor", "Zaquan", "Taylor", "(434) 555-6666", "Password", "Patron&Librarian","ztaylor3@broncos.uncfsu.edu")
     )
conn.commit()
conn.close()
