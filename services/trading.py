import random
import asyncio
from datetime import datetime
from database import (
    get_pool_balance,
    update_pool,
    increment_trade,
    get_trade_number,
    get_trade_stats
)
from images.trade_open import generate_trade_open
from images.trade_close import generate_trade_close
from config import MIN_POOL_FOR_TRADING

PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

async def run_trade(context):
    pool_before = get_pool_balance()
    if pool_before < MIN_POOL_FOR_TRADING:
        return

    trade_no = get_trade_number()
    wins, losses = get_trade_stats()

    pair = random.choice(PAIRS)
    direction = random.choice(["LONG", "SHORT"])
    leverage = random.choice([5, 10, 12, 20])
    participants = random.randint(200, 600)
    entry = random.uniform(25000, 90000)

    open_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    open_data = {
        "pair": pair,
        "direction": direction,
        "leverage": leverage,
        "participants": participants,
        "entry": entry,
        "pool": pool_before,
        "trade_no": trade_no,
        "time": open_time
    }

    open_img = generate_trade_open(open_data)

    await context.bot.send_photo(
        chat_id=context.bot_data["CHANNEL_ID"],
        photo=open_img,
        caption=(
            f"🔔 NEW POOL TRADE OPENED 🔔\n\n"
            f"🪙 Pair: {pair}\n"
            f"📊 Direction: {direction}\n"
            f"💰 Pool Amount: {pool_before:,.2f} USDT\n"
            f"💵 Entry Price: {entry:,.2f}\n"
            f"🔧 Leverage: {leverage}x\n"
            f"👥 Participants: {participants}\n\n"
            f"📌 Trade #{trade_no}\n"
            f"🕒 {open_time}"
        )
    )

    await asyncio.sleep(random.randint(30, 90))

    win = random.random() < 0.88
    pnl_pct = random.uniform(0.001, 0.02)
    pnl = pool_before * pnl_pct
    if not win:
        pnl *= -0.4

    pool_after = pool_before + pnl
    update_pool(pnl)
    increment_trade(win)

    exit_price = entry * (1 - pnl_pct if direction == "SHORT" else 1 + pnl_pct)
    close_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    wins, losses = get_trade_stats()
    result_label = f"Win #{wins}" if win else f"Loss #{losses}"
    total_label = f"{wins + losses}"

    pnl_text = (
        f"+{pnl:,.2f} USDT ({pnl_pct*100:.2f}%)"
        if win else
        f"-{abs(pnl):,.2f} USDT ({pnl_pct*100:.2f}%)"
    )

    close_data = {
        "pair": pair,
        "entry": entry,
        "exit": exit_price,
        "pool_before": pool_before,
        "pool_after": pool_after,
        "trade_no": trade_no,
        "time": close_time,
        "win": win,
        "pnl": pnl_text
    }

    close_img = generate_trade_close(close_data)

    await context.bot.send_photo(
        chat_id=context.bot_data["CHANNEL_ID"],
        photo=close_img,
        caption=(
            f"🔔 POOL TRADE CLOSED 🔔\n\n"
            f"🪙 Pair: {pair}\n"
            f"📊 Direction: {direction}\n"
            f"💰 Initial Pool: {pool_before:,.2f} USDT\n"
            f"💰 Final Pool: {pool_after:,.2f} USDT\n"
            f"💵 Entry Price: {entry:,.2f}\n"
            f"💵 Exit Price: {exit_price:,.2f}\n"
            f"🔧 Leverage: {leverage}x\n"
            f"👥 Participants: {participants}\n\n"
            f"{'✅ PROFIT' if win else '❌ LOSS'}: {pnl_text}\n"
            f"📊 {result_label} / {total_label}\n"
            f"📌 Trade #{trade_no}\n"
            f"🕒 {close_time}"
        )
    )
