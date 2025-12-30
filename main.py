import sqlite3
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ------------------------
# DATABASE SETUP
# ------------------------
DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE,
               password TEXT
           )"""
    )
    conn.commit()
    conn.close()

def add_user(username: str, password: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# ------------------------
# BOT HANDLERS
# ------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Use /register <username> <password> to register."
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /register <username> <password>")
        return
    username, password = context.args
    if add_user(username, password):
        await update.message.reply_text(f"User {username} registered successfully!")
    else:
        await update.message.reply_text(f"Username {username} is already taken.")

# ------------------------
# AUTO TRADING JOB
# ------------------------
async def auto_trade(context: ContextTypes.DEFAULT_TYPE):
    print("Running auto trade...")
    # Example: send a message to admin or group
    chat_id = context.bot_data.get("ADMIN_CHAT_ID")
    if chat_id:
        await context.bot.send_message(chat_id=chat_id, text="Auto trade executed.")

# ------------------------
# MAIN
# ------------------------
def main():
    init_db()  # Make sure DB is ready

    # Bot token from environment variable (Railway uses RAILWAY_BOT_TOKEN)
    import os
    TOKEN = os.environ.get("RAILWAY_BOT_TOKEN")
    if not TOKEN:
        print("RAILWAY_BOT_TOKEN not set in environment")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))

    # Optional: set admin chat ID (to send trade updates)
    admin_chat_id = os.environ.get("ADMIN_CHAT_ID")
    if admin_chat_id:
        app.bot_data["ADMIN_CHAT_ID"] = int(admin_chat_id)

    # Run auto trade every 5 minutes
    app.job_queue.run_repeating(auto_trade, interval=300, first=10)

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
