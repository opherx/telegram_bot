import random, asyncio
from datetime import datetime, time
from images.trade_open import generate_trade_open
from images.trade_close import generate_trade_close

ACTIVE_START = time(6, 0)
ACTIVE_END = time(23, 0)


async def run_trade(context):
    now = datetime.utcnow().time()
    if not (ACTIVE_START <= now <= ACTIVE_END):
        return

    win = random.random() < random.uniform(0.85, 0.9)
    pnl = random.uniform(400, 1600) * (1 if win else -1)

    data = {
        "pair": "BTC/USDT",
        "entry": random.uniform(87000, 89000),
        "direction": random.choice(["LONG", "SHORT"]),
        "leverage": random.choice([5, 10, 12, 15]),
        "pool": context.bot_data["POOL"],
        "participants": context.bot_data["USERS"],
        "qr": "https://t.me/YourBot"
    }

    open_img = generate_trade_open(data)
    await context.bot.send_photo(context.bot_data["CHANNEL"], open_img)

    await asyncio.sleep(random.randint(180, 1800))

    pool_before = context.bot_data["POOL"]
    pool_after = pool_before + pnl
    context.bot_data["POOL"] = pool_after

    close_data = {
        **data,
        "pnl": pnl,
        "win": win,
        "pool_before": pool_before,
        "pool_after": pool_after,
    }

    close_img = generate_trade_close(close_data)
    await context.bot.send_photo(context.bot_data["CHANNEL"], close_img)
