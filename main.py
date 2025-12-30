import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ====== DATABASE SETUP ======
conn = sqlite3.connect("bot_users.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    balance REAL DEFAULT 0
)
""")
conn.commit()

# ====== BOT TOKEN ======
import os
TOKEN = os.environ.get("RAILWAY_BOT_TOKEN")
if not TOKEN:
    print("RAILWAY_BOT_TOKEN not set in environment")
    exit(1)

# ====== COMMAND HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Use /register <username> <password> to create an account."
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = context.args[0]
        password = context.args[1]
    except IndexError:
        await update.message.reply_text("Usage: /register <username> <password>")
        return

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        await update.message.reply_text(f"Registered {username} successfully!")
    except sqlite3.IntegrityError:
        await update.message.reply_text("Username already exists!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.args[0] if context.args else None
    if not username:
        await update.message.reply_text("Usage: /balance <username>")
        return

    c.execute("SELECT balance FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        await update.message.reply_text(f"{username}'s balance: ${result[0]:.2f}")
    else:
        await update.message.reply_text("User not found!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/register <username> <password> - Register an account\n"
        "/balance <username> - Check your balance\n"
        "/help - Show this message"
    )

# ====== MAIN FUNCTION ======
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
