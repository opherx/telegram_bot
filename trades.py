import random
from database import get_db

PAIRS = ["BTC/USDT", "ETH/USDT", "XAUUSD"]

def generate_trade():
    pair = random.choice(PAIRS)
    entry = round(random.uniform(100, 50000), 2)
    exit = entry + random.uniform(-500, 800)
    result = "WIN" if exit > entry else "LOSS"

    db = get_db()
    c = db.cursor()

    c.execute(
        "INSERT INTO trades (pair, entry, exit, result) VALUES (?, ?, ?, ?)",
        (pair, entry, exit, result)
    )

    db.commit()
    db.close()

    return pair, entry, exit, result
