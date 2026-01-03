import random
from datetime import datetime
from database import cur, conn, get_pool_balance, update_pool
from config import MIN_POOL_FOR_TRADING
from images.generator import generate_card

PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

async def run_trade(context):
    pool = get_pool_balance()
    if pool < MIN_POOL_FOR_TRADING:
        return

    pair = random.choice(PAIRS)
    profit = pool * random.uniform(0.005, 0.02)
    update_pool(profit)

    cur.execute(
        "INSERT INTO trades (pair, profit, created_at) VALUES (?, ?, ?)",
        (pair, profit, datetime.utcnow().isoformat())
    )
    trade_id = cur.lastrowid

    distributed = profit * 0.02
    users = cur.execute("SELECT telegram_id, balance FROM users WHERE balance>0").fetchall()

    for u in users:
        gain = distributed * (u["balance"] / pool)
        cur.execute("""
            UPDATE users
            SET balance=balance+?, total_profit=total_profit+?, trades=trades+1
            WHERE telegram_id=?
        """, (gain, gain, u["telegram_id"]))
        cur.execute("INSERT INTO user_trades VALUES (?, ?, ?)",
                    (u["telegram_id"], trade_id, gain))

    cur.execute("""
        UPDATE pool SET
            total_traded=total_traded+?,
            total_profit=total_profit+?,
            total_distributed=total_distributed+?,
            wins=wins+1
    """, (pool, profit, distributed))
    conn.commit()

    img = generate_card("POOL TRADE CLOSED",
                        [f"{pair}", f"Profit: +{profit:.2f} USDT"],
                        "trade_close.png")
    await context.bot.send_photo(chat_id=context.bot_data["CHANNEL_ID"], photo=img)
