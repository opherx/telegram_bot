import os
import random
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

conn = sqlite3.connect("demo.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance REAL
)
""")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 DEMO Trading Bot\n\nSimulation only.\n\nUse /deposit to start."
    )

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?)",
        (update.effective_user.id, 100)
    )
    conn.commit()
    await update.message.reply_text("💰 Demo balance credited: $100")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (update.effective_user.id,)
    )
    row = cursor.fetchone()
    if not row:
        await update.message.reply_text("❌ Deposit first.")
        return

    pnl = random.uniform(-5, 10)
    new_balance = row[0] + pnl

    cursor.execute(
        "UPDATE users SET balance=? WHERE user_id=?",
        (new_balance, update.effective_user.id)
    )
    conn.commit()

    await update.message.reply_text(
        f"📊 Trade result: ${pnl:.2f}\n"
        f"Balance: ${new_balance:.2f}\n\n⚠️ DEMO MODE"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("trade", trade))
    app.run_polling()

main()
