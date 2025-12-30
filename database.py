import sqlite3

DB_FILE = "bot.db"

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

# --- Existing code ---
conn = get_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    balance REAL DEFAULT 0
)
""")

conn.commit()

def add_user(tg_id, username, password):
    cursor.execute(
        "INSERT OR REPLACE INTO users (telegram_id, username, password, balance) VALUES (?, ?, ?, ?)",
        (tg_id, username, password, 0)
    )
    conn.commit()

def get_user(tg_id):
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (tg_id,))
    return cursor.fetchone()

def update_balance(tg_id, amount):
    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE telegram_id = ?",
        (amount, tg_id)
    )
    conn.commit()
