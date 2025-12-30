import random
from telegram.ext import ContextTypes
from database import get_all_users, update_balance

PAIRS = ["BTC/USDT", "ETH/USDT", "XAUUSD", "BNB/USDT"]

async def send_trade(context: ContextTypes.DEFAULT_TYPE):
    """Send trade updates to the channel and users."""

    # Generate a trade
    pair = random.choice(PAIRS)
    entry = round(random.uniform(100, 50000), 2)
    tp = round(entry + random.uniform(50, 500), 2)
    sl = round(entry - random.uniform(50, 500), 2)
    result = random.choice(["WIN", "LOSS"])

    trade_message = (
        f"💹 *New Trade Signal!*\n"
        f"📌 Pair: *{pair}*\n"
        f"▶️ Entry: `{entry}`\n"
        f"🏁 Take Profit: `{tp}`\n"
        f"⛔ Stop Loss: `{sl}`\n"
        f"📊 Result: *{result}*\n"
        f"⚡ Stay tuned!"
    )

    # Send to the channel
    channel_id = context.bot_data.get("CHANNEL_ID")
    if channel_id:
        await context.bot.send_message(chat_id=channel_id, text=trade_message, parse_mode="Markdown")

    # Update users and send DM
    amount = random.randint(5, 50) if result == "WIN" else -random.randint(5, 50)
    for user in get_all_users():
        update_balance(user["telegram_id"], amount)
        try:
            await context.bot.send_message(
                chat_id=user["telegram_id"],
                text=f"📢 Trade Update:\n{trade_message}\n💰 Demo Balance Change: {amount}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Failed to send trade to {user['telegram_id']}: {e}")
