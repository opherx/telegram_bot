import os
import random
import sqlite3
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue
)

# Environment variables
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 8443))
URL = os.getenv("RAILWAY_STATIC_URL")  # your Railway project URL

# Database setup
conn = sqlite3.connect("demo.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    balance REAL
)
""")
conn.commit()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to DEMO Trading Bot!\n\n"
        "Use /register <username> <password> to create an account."
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = context.args[0]
        password = context.args[1]
    except IndexError:
        await update.message.reply_text("Usage: /register <username> <password>")
        return

    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, username, password, balance) VALUES (?, ?, ?, ?)",
        (update.effective_user.id, username, password, 100)  # demo balance $100
    )
    conn.commit()
    await update.message.reply_text(f"✅ Registered as {username}. Demo balance: $100")

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT username, balance FROM users WHERE user_id=?", (update.effective_user.id,))
    row = cursor.fetchone()
    if not row:
        await update.message.reply_text("❌ Please register first using /register")
        return

    username, balance = row
    await update.message.reply_text(
        f"📊 Dashboard for {username}\n"
        f"Balance: ${balance:.2f}\n"
    )

# Auto trade function
async def auto_trade(context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT user_id, balance FROM users")
    rows = cursor.fetchall()
    for user_id, balance in rows:
        pnl = random.uniform(-5, 10)
        new_balance = balance + pnl
        cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
        conn.commit()
        # Send trade result to user
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📊 Auto Trade Result: ${pnl:.2f}\nBalance: ${new_balance:.2f}\n⚠️ DEMO MODE"
            )
        except:
            continue  # skip if user blocked bot

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("dashboard", dashboard))

    # Auto trade every 5 minutes
    app.job_queue.run_repeating(auto_trade, interval=300, first=10)

    # Run webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{URL}/webhook/{TOKEN}"
    )

if __name__ == "__main__":
    main()
