import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
)

# -------- HANDLERS --------
from handlers.users import (
    register_start,
    register_username,
    register_password,
    USERNAME,
    PASSWORD,
)

from handlers.payments import (
    deposit,
    withdraw_start,
    withdraw_wallet,
    withdraw_amount,
    WALLET,
    AMOUNT,
)

from handlers.trade import trade

# -------- JOBS --------
from jobs.trade_engine import send_trade

# -------- ENV VARIABLES --------
TOKEN = os.environ.get("RAILWAY_BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # your Telegram channel id

def main():
    if not TOKEN:
        raise RuntimeError("RAILWAY_BOT_TOKEN not set")

    app = ApplicationBuilder().token(TOKEN).build()

    # Store channel id globally for trades
    app.bot_data["CHANNEL_ID"] = CHANNEL_ID

    # -------- REGISTER --------
    register_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register_start)],
        states={
            USERNAME: [register_username],
            PASSWORD: [register_password],
        },
        fallbacks=[],
    )

    # -------- WITHDRAW --------
    withdraw_handler = ConversationHandler(
        entry_points=[CommandHandler("withdraw", withdraw_start)],
        states={
            WALLET: [withdraw_wallet],
            AMOUNT: [withdraw_amount],
        },
        fallbacks=[],
    )

    # -------- COMMANDS --------
    app.add_handler(register_handler)
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(withdraw_handler)
    app.add_handler(CommandHandler("trade", trade))

    # -------- AUTO TRADES --------
    app.job_queue.run_repeating(
        send_trade,
        interval=60,  # every 60 seconds
        first=15,
    )

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
