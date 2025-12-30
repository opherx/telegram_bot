import random
from database import get_all_users, update_balance
from telegram import ParseMode
from telegram.ext import ContextTypes

# List of pairs for demo trades
PAIRS = ["EUR/USD", "GBP/USD", "BTC/USDT", "ETH/USDT"]

async def send_trade(context: ContextTypes.DEFAULT_TYPE):
    """Send a trade signal to the channel and update users' balances."""
    
    # Pick random trade
    pair = random.choice(PAIRS)
    result = random.choice(["WIN", "LOSS"])
    amount = random.randint(5, 50)  # Trade amount for demo

    # Build message
    message = f"💹 Trade Signal\nPair: {pair}\nResult: {result}\nAmount: ${amount}"
    
    # Send to channel
    channel_id = context.bot_data.get("CHANNEL_ID")
    if channel_id:
        await context.bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Update all users' balances (demo logic)
    users = get_all_users()  # Returns list of dicts with 'id' and 'balance'
    for user in users:
        if result == "WIN":
            update_balance(user["id"], user["balance"] + amount)
        else:
            update_balance(user["id"], max(0, user["balance"] - amount))
