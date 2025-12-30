import os
import random
import sqlite3
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue,
)

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 8443))  # Railway provides this automatically

# SQLite DB (can be replaced with PostgreSQL for production)
conn = sqlite3.connect("demo.db", check_same_thread=False)
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    balance REAL
)
""")
conn.commit()


# -------------------------
# User commands
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Demo Trading Bot\n"
        "Use /register <username> <password> to start."
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
        (update.effective_user.id, username, password, 100.0)
    )
    conn.commit()
    await update.message.reply_text(
        f"✅ Registered as {username}\n💰 Demo balance: $100"
    )

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute(
        "SELECT username, balance FROM users WHERE user_id=?",
        (update.effective_user.id,)
    )
    row = cursor.fetchone()
    if not row:
        await update.message.reply_text("❌ Please register first.")
        return

    username, balance = row
    await update.message.reply_text(
        f"📊 Dashboard\nUser: {username}\nBalance: ${balance:.2f}"
    )

# -------------------------
# Auto-trade logic
# -------------------------

def generate_trade_image(entry, exit_price, pnl):
    # Simple demo screenshot image
    img = Image.new("RGB", (500, 300), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((20, 20), f"Entry: ${entry:.2f}", font=font, fill="white")
    draw.text((20, 60), f"Exit: ${exit_price:.2f}", font=font, fill="white")
    draw.text((20, 100), f"P/L: ${pnl:.2f}", font=font, fill="white")
    bio = BytesIO()
    bio.name = "trade.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio

async def auto_trade(context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT user_id, balance FROM users")
    users = cursor.fetchall()
    for user_id, balance in users:
        pnl = random.uniform(-5, 10)
        new_balance = balance + pnl
        cursor.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (new_balance, user_id)
        )
        conn.commit()

        entry = balance
        exit_price = new_balance
        img = generate_trade_image(entry, exit_price, pnl)

        try:
            await context.bot.send_photo(
                chat_id=user_id,
                photo=InputFile(img),
                caption=f"📊 Auto-trade result\nP/L: ${pnl:.2f}\nBalance: ${new_balance:.2f}"
            )
        except Exception as e:
            print(f"Failed to send trade to {user_id}: {e}")


# -------------------------
# Main app with webhook
# -------------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("dashboard", dashboard))

    # Job queue for auto-trading every 5 minutes
    app.job_queue.run_repeating(auto_trade, interval=300, first=10)

    # Webhook
    RAILWAY_URL = os.environ.get("RAILWAY_STATIC_URL")  # your Railway project URL
    if not RAILWAY_URL:
        print("Error: Set RAILWAY_STATIC_URL in Railway environment variables.")
        return

    webhook_url = f"{RAILWAY_URL}/{TOKEN}"
    print(f"Webhook URL: {webhook_url}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url_path=TOKEN,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    main()
