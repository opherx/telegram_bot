import sqlite3

conn = sqlite3.connect("demo.db", check_same_thread=False)
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    balance REAL DEFAULT 100
)
""")
conn.commit()

# Functions
def add_user(user_id, username, password):
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, username, password, balance) VALUES (?, ?, ?, ?)",
        (user_id, username, password, 100)
    )
    conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

def update_balance(user_id, new_balance):
    cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn.commit()
