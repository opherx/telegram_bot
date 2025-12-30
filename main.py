import os
import random
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# DB setup
conn = sqlite3.connect("demo.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance REAL
)
""")
conn.commit()

# Basic commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 DEMO Trading Bot\nUse /deposit to start.")

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?)",
        (update.effective_user.id, 100)
    )
    conn.commit()
    await update.message.reply_text("💰 Demo balance credited: $100")

# Auto trade function
async def auto_trade(context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT user_id, balance FROM users")
    rows = cursor.fetchall()
    for user_id, balance in rows:
        pnl = random.uniform(-5, 10)
        new_balance = balance + pnl
        cursor.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (new_balance, user_id)
        )
        conn.commit()
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📊 Auto trade result: ${pnl:.2f}\nBalance: ${new_balance:.2f}"
            )
        except Exception:
            pass  # user may not have started bot

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deposit", deposit))

    # Auto trade job every 5 minutes (300s)
    if app.job_queue:
        app.job_queue.run_repeating(auto_trade, interval=300, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
