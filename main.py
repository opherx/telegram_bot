import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
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

# ---- START COMMAND ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 Register", callback_data="register")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("📤 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("📈 Trade", callback_data="trade")],
        [InlineKeyboardButton("ℹ️ Balance", callback_data="balance")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "👋 *Welcome to TradeMaster Bot!*\n\n"
        "💎 Ready to start your demo trading journey?\n\n"
        "⚡ Here’s what you can do:\n"
        "📝 Register /register\n"
        "💰 Deposit /deposit\n"
        "📤 Withdraw /withdraw\n"
        "📈 Trade /trade\n"
        "ℹ️ Balance /balance\n\n"
        "🚀 *Tip:* Trades are simulated every 1 minute. Stay tuned for signals!"
    )

    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)


def main():
    if not TOKEN:
        raise RuntimeError("RAILWAY_BOT_TOKEN not set")

    app = ApplicationBuilder().token(TOKEN).build()

    # Store channel id globally
    app.bot_data["CHANNEL_ID"] = CHANNEL_ID

    # -------- REGISTER --------
    register_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register_start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_username)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_password)],
        },
        fallbacks=[],
    )

    # -------- WITHDRAW --------
    withdraw_handler = ConversationHandler(
        entry_points=[CommandHandler("withdraw", withdraw_start)],
        states={
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_wallet)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount)],
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
        interval=60,  # every 60 seconds
        first=15,
    )

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
