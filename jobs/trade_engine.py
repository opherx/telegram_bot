import random
from database import get_user, update_balance

# List of demo trading pairs
PAIRS = ["EUR/USD", "GBP/USD", "BTC/USDT", "ETH/USDT"]

async def send_trade(context):
    """Send a trade signal to the channel and update users' balances."""
    
    pair = random.choice(PAIRS)
    result = random.choice(["WIN", "LOSS"])
    amount = random.randint(5, 50)  # Demo trade amount

    message = f"💹 Trade Signal\nPair: {pair}\nResult: {result}\nAmount: ${amount}"

    channel_id = context.bot_data.get("CHANNEL_ID")
    if channel_id:
        await context.bot.send_message(
            chat_id=channel_id,
            text=message
        )

    # Update all registered users
    # Since get_all_users was removed, we manually query users from DB
    # But using get_user requires IDs; so keep a simple user_id list in bot memory
    user_ids = list(context.bot_data.get("USERS", []))
    for uid in user_ids:
        user = get_user(uid)
        if not user:
            continue
        if result == "WIN":
            update_balance(uid, amount)
        else:
            update_balance(uid, -amount)
