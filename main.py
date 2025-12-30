import sqlite3
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)

# --- SQLite setup ---
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    username TEXT,
    password TEXT,
    balance REAL DEFAULT 0
)
"""
)
conn.commit()

# --- Conversation states ---
REGISTER_USERNAME, REGISTER_PASSWORD = range(2)
WITHDRAW_WALLET, WITHDRAW_AMOUNT = range(2)

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Use /register to create an account."
    )

# --- Register ---
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your desired username:")
    return REGISTER_USERNAME

async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("Enter your password:")
    return REGISTER_PASSWORD

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    username = context.user_data["username"]
    telegram_id = update.message.from_user.id

    try:
        cursor.execute(
            "INSERT INTO users (telegram_id, username, password, balance) VALUES (?, ?, ?, ?)",
            (telegram_id, username, password, 0),
        )
        conn.commit()
        await update.message.reply_text(
            f"✅ Registration complete!\nUsername: {username}\nBalance: $0"
        )
    except sqlite3.IntegrityError:
        await update.message.reply_text("⚠️ You are already registered!")
    return ConversationHandler.END

# --- Deposit ---
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE telegram_id=?", (telegram_id,))
    user = cursor.fetchone()
    if not user:
        await update.message.reply_text("⚠️ You must /register first.")
        return
    cursor.execute(
        "UPDATE users SET balance = balance + 100 WHERE telegram_id=?", (telegram_id,)
    )
    conn.commit()
    await update.message.reply_text("💰 Deposited $100. Enjoy!")

# --- Withdraw ---
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE telegram_id=?", (telegram_id,))
    user = cursor.fetchone()
    if not user:
        await update.message.reply_text("⚠️ You must /register first.")
        return ConversationHandler.END
    await update.message.reply_text("Enter your USDT wallet address:")
    return WITHDRAW_WALLET

async def withdraw_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet"] = update.message.text
    await update.message.reply_text("Enter amount to withdraw:")
    return WITHDRAW_AMOUNT

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = float(update.message.text)
    telegram_id = update.message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE telegram_id=?", (telegram_id,))
    balance = cursor.fetchone()[0]

    if amount > balance:
        await update.message.reply_text("⚠️ Insufficient balance.")
        return ConversationHandler.END

    cursor.execute(
        "UPDATE users SET balance = balance - ? WHERE telegram_id=?",
        (amount, telegram_id),
    )
    conn.commit()
    await update.message.reply_text(
        f"✅ Withdrawal of {amount} USDT successful to wallet {context.user_data['wallet']}."
    )
    return ConversationHandler.END

# --- Trade simulation ---
async def trade_simulation(context: ContextTypes.DEFAULT_TYPE):
    channel_id = context.bot_data.get("CHANNEL_ID")
    if channel_id:
        await context.bot.send_message(
            chat_id=channel_id,
            text="📈 New trade signal: BUY EUR/USD at 1.1234",
        )

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Trade signals will be sent to the channel.")

# --- Main ---
def main():
    TOKEN = "YOUR_BOT_TOKEN"
    CHANNEL_ID = -1001234567890  # replace with your channel ID

    app = ApplicationBuilder().token(TOKEN).build()
    app.bot_data["CHANNEL_ID"] = CHANNEL_ID

    # Conversation handler for registration
    reg_conv = ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={
            REGISTER_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_username)],
            REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_password)],
        },
        fallbacks=[],
    )

    # Conversation handler for withdraw
    withdraw_conv = ConversationHandler(
        entry_points=[CommandHandler("withdraw", withdraw)],
        states={
            WITHDRAW_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_wallet)],
            WITHDRAW_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(reg_conv)
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(withdraw_conv)
    app.add_handler(CommandHandler("trade", trade))

    # Schedule trade simulation every 60 seconds
    app.job_queue.run_repeating(trade_simulation, interval=60, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
