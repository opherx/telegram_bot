import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
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

def get_all_users():
    cursor.execute("SELECT telegram_id, username, password, balance FROM users")
    rows = cursor.fetchall()
    return [
        {"telegram_id": r[0], "username": r[1], "password": r[2], "balance": r[3]}
        for r in rows
    ]

def update_balance(tg_id, amount):
    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE telegram_id = ?",
        (amount, tg_id)
    )
    conn.commit()
