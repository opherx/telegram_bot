import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
)
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
from jobs.trade_engine import send_trade

TOKEN = os.environ.get("RAILWAY_BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # your Telegram channel ID

# START command
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to TradeMaster Bot!*\n\n"
        "💎 Ready to start your demo trading journey?\n\n"
        "Here’s what you can do:\n"
        "📝 /register - Create your account\n"
        "💰 /deposit - Auto credit $100 (demo)\n"
        "📤 /withdraw - Withdraw your balance\n"
        "📈 /trade - See latest trade signals\n"
        "ℹ️ /balance - Check your balance\n\n"
        "⚡ *Tip:* Trades are simulated every 1 minute, stay tuned for signals! 🚀"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

def main():
    if not TOKEN:
        raise RuntimeError("RAILWAY_BOT_TOKEN not set")

    app = ApplicationBuilder().token(TOKEN).build()

    # store channel id globally
    app.bot_data["CHANNEL_ID"] = CHANNEL_ID
    app.bot_data["USERS"] = []  # to store registered user IDs

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
    app.add_handler(CommandHandler("start", start))
    app.add_handler(register_handler)
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(withdraw_handler)
    app.add_handler(CommandHandler("trade", trade))

    # -------- AUTO TRADES --------
    app.job_queue.run_repeating(
        send_trade,
        interval=60,   # every 60 seconds
        first=15,
    )

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
