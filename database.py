import sqlite3
from config import DEFAULT_POOL_BALANCE

conn = sqlite3.connect("bot.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def init_db():
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        telegram_id INTEGER PRIMARY KEY,
        username TEXT,
        pin TEXT,
        balance REAL DEFAULT 0,
        total_deposited REAL DEFAULT 0,
        total_withdrawn REAL DEFAULT 0,
        total_profit REAL DEFAULT 0,
        trades INTEGER DEFAULT 0,
        referrer_id INTEGER,
        referral_earnings REAL DEFAULT 0,
        tier TEXT DEFAULT 'STANDARD',
        kyc_status TEXT DEFAULT 'NONE'
    );

    CREATE TABLE IF NOT EXISTS pool(
        id INTEGER PRIMARY KEY,
        balance REAL DEFAULT 0,
        total_traded REAL DEFAULT 0,
        total_profit REAL DEFAULT 0,
        total_distributed REAL DEFAULT 0,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS pending_deposits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        asset TEXT,
        amount REAL,
        status TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS pending_withdrawals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        wallet TEXT,
        amount REAL,
        status TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pair TEXT,
        profit REAL,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS user_trades(
        user_id INTEGER,
        trade_id INTEGER,
        profit REAL
    );
    """)

    cur.execute(
        "INSERT OR IGNORE INTO pool (id, balance) VALUES (1, ?)",
        (DEFAULT_POOL_BALANCE,)
    )
    conn.commit()

def get_pool_balance():
    return cur.execute("SELECT balance FROM pool WHERE id=1").fetchone()["balance"]

def update_pool(amount):
    cur.execute("UPDATE pool SET balance = balance + ? WHERE id=1", (amount,))
    conn.commit()
