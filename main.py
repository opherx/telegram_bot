import os
import random
import sqlite3
import datetime
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)
from PIL import Image, ImageDraw, ImageFont

# ======================
# CONFIG
# ======================
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1001234567890  # 🔴 REPLACE WITH YOUR CHANNEL ID

if not TOKEN:
    raise ValueError("TOKEN not set")

# ======================
# DATABASE
# ======================
conn = sqlite3.connect("demo.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 100
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    pair TEXT,
    direction TEXT,
    entry REAL,
    exit REAL,
    pnl REAL,
    time TEXT
)
""")

conn.commit()

# ======================
# IMAGE GENERATOR (DEMO)
# ======================
def generate_trade_image(pair, direction, entry, exit_price, pnl):
    img = Image.new("RGB", (500, 300), (25, 25, 25))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    draw.text((20, 20), "DEMO TRADE RESULT", fill="white", font=font)
    draw.text((20, 60), f"PAIR: {pair}", fill="white", font=font)
    draw.text((20, 90), f"DIRECTION: {direction}", fill="white", font=font)
    draw.text((20, 120), f"ENTRY: {entry}", fill="white", font=font)
    draw.text((20, 150), f"EXIT: {exit_price}", fill="white", font=font)
    draw.text((20, 180), f"PNL: ${pnl}", fill="white", font=font)
    draw.text((20, 240), "SIMULATION ONLY", fill="red", font=font)

    img.save("trade_demo.png")

# ======================
# DASHBOARD
# ======================
def dashboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Balance", callback_data="balance")],
        [InlineKeyboardButton("📈 Trade History", callback_data="history")],
        [InlineKeyboardButton("🧪 Bot Status", callback_data="status")]
    ])

# ======================
# COMMANDS
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (user_id,))
    conn.commit()

    await update.message.reply_text(
        "🤖 DEMO Trading Bot\n\n"
        "⚠️ SIMULATION ONLY\n"
        "No real trading\n\n"
        "Join demo channel for trades.",
        reply_markup=dashboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "balance":
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        bal = cursor.fetchone()[0]
        await query.edit_message_text(f"📊 Balance: ${bal:.2f}\n⚠️ DEMO MODE")

    elif query.data == "history":
        cursor.execute(
            "SELECT pair, pnl FROM trades WHERE user_id=? ORDER BY id DESC LIMIT 5",
            (user_id,)
        )
        rows = cursor.fetchall()
        msg = "📈 Last trades:\n"
        for r in rows:
            msg += f"{r[0]} → ${r[1]:.2f}\n"
        await query.edit_message_text(msg or "No trades yet")

    elif query.data == "status":
        await query.edit_message_text("🧪 Bot running\nAuto demo trades enabled")

# ======================
# AUTO TRADE ENGINE
# ======================
async def auto_trade(context: ContextTypes.DEFAULT_TYPE):
    pairs = ["EUR/USD", "BTC/USD", "ETH/USD"]

    cursor.execute("SELECT user_id, balance FROM users")
    users = cursor.fetchall()

    if not users:
        return

    pair = random.choice(pairs)
    direction = random.choice(["BUY", "SELL"])
    entry = round(random.uniform(1.0, 2.0), 5)
    pnl = round(random.uniform(-5, 10), 2)
    exit_price = round(entry + pnl / 1000, 5)

    generate_trade_image(pair, direction, entry, exit_price, pnl)

    for user_id, balance in users:
        new_balance = balance + pnl

        cursor.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (new_balance, user_id)
        )

        cursor.execute(
            "INSERT INTO trades(user_id, pair, direction, entry, exit, pnl, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, pair, direction, entry, exit_price, pnl, datetime.datetime.now().isoformat())
        )
        conn.commit()

        await context.bot.send_message(
            chat_id=user_id,
            text=f"📉 DEMO Trade Closed\n{pair}\nPNL: ${pnl}\nBalance: ${new_balance:.2f}"
        )

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=open("trade_demo.png", "rb"),
        caption="📊 DEMO Trade Result\n⚠️ Simulation only"
    )

# ======================
# MAIN
# ======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.job_queue.run_repeating(auto_trade, interval=300, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
