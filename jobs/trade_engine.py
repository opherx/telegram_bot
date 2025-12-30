import random
from database import get_all_users, update_balance
from telegram.constants import ParseMode  # <-- fixed import

PAIRS = ["EUR/USD", "GBP/USD", "BTC/USDT", "ETH/USDT"]

async def send_trade(context):
    """Send a rich trade signal and update balances"""

    pair = random.choice(PAIRS)
    entry = round(random.uniform(100, 50000), 2)
    exit_price = entry + round(random.uniform(-500, 800), 2)
    result = "✅ WIN" if exit_price > entry else "❌ LOSS"
    amount = random.randint(5, 50)

    message = (
        f"📊 *New Trade Signal!*\n\n"
        f"💹 Pair: *{pair}*\n"
        f"🚀 Entry: `{entry}`\n"
        f"🎯 Target/Exit: `{exit_price}`\n"
        f"💰 Amount: `${amount}`\n"
        f"📌 Result: *{result}*"
    )

    channel_id = context.bot_data.get("CHANNEL_ID")
    if channel_id:
        await context.bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )

    # Update balances
    users = get_all_users()
    for user in users:
        if "WIN" in result:
            update_balance(user["telegram_id"], amount)
        else:
            update_balance(user["telegram_id"], -amount)
