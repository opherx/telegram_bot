# ================================
# GOTHIX AI — DEMO TRADING BOT
# python-telegram-bot v20+
# ================================

import asyncio
import random
import sqlite3
from datetime import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from PIL import Image, ImageDraw, ImageFont

# ================= CONFIG =================

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


MIN_DEPOSIT = 20.0
TRADE_INTERVAL = 300  # seconds

PAIRS = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]
DIRECTIONS = ["LONG", "SHORT"]
LEVERAGES = [5, 10, 12, 15]

# ================= DATABASE =================

db = sqlite3.connect("gothix.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    balance REAL,
    deposited REAL,
    withdrawn REAL,
    profit REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY,
    total_trades INTEGER,
    wins INTEGER,
    losses INTEGER,
    capital REAL,
    profit REAL
)
""")

cur.execute("""
INSERT OR IGNORE INTO stats VALUES (1,0,0,0,0,0)
""")

db.commit()

# ================= UTILITIES =================

def get_user(uid):
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    return cur.fetchone()

def create_user(uid, username, password):
    cur.execute("""
    INSERT INTO users VALUES (?,?,?,?,?,?,?)
    """, (uid, username, password, 0, 0, 0, 0))
    db.commit()

def update_user(uid, field, value):
    cur.execute(f"UPDATE users SET {field}={field}+? WHERE user_id=?", (value, uid))
    db.commit()

def get_stats():
    cur.execute("SELECT * FROM stats WHERE id=1")
    return cur.fetchone()

# ================= IMAGE GENERATION =================

def generate_card(title, lines, filename):
    img = Image.new("RGB", (900, 500), "#111111")
    draw = ImageDraw.Draw(img)
    font_big = ImageFont.load_default()
    font = ImageFont.load_default()

    draw.text((30, 20), title, fill="#00ff99", font=font_big)

    y = 100
    for line in lines:
        draw.text((30, y), line, fill="#ffffff", font=font)
        y += 40

    img.save(filename)

# ================= START / REGISTER =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not get_user(uid):
        context.user_data["reg"] = "username"
        await update.message.reply_text("👋 Welcome!\n\nCreate username:")
    else:
        await dashboard(update, context)

async def register(update: Update, context):
    step = context.user_data.get("reg")
    if step == "username":
        context.user_data["username"] = update.message.text
        context.user_data["reg"] = "password"
        await update.message.reply_text("Set password:")
    elif step == "password":
        create_user(
            update.effective_user.id,
            context.user_data["username"],
            update.message.text
        )
        context.user_data.clear()
        await update.message.reply_text("✅ Registration complete")
        await dashboard(update, context)

# ================= DASHBOARD =================

async def dashboard(update, context):
    user = get_user(update.effective_user.id)
    text = (
        f"📊 *Dashboard*\n\n"
        f"💰 Balance: {user[3]:.2f} USDT\n"
        f"📥 Deposited: {user[4]:.2f}\n"
        f"📤 Withdrawn: {user[5]:.2f}\n"
        f"📈 Profit: {user[6]:.2f}"
    )
    kb = [
        [InlineKeyboardButton("➕ Deposit", callback_data="deposit")],
        [InlineKeyboardButton("➖ Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("📊 Performance", callback_data="stats")]
    ]
    await update.message.reply_text(
        text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

# ================= DEPOSIT FLOW =================

async def deposit(update: Update, context):
    coins = ["BTC", "ETH", "BNB", "SOL"]
    kb = [[InlineKeyboardButton(c, callback_data=f"coin_{c}")] for c in coins]
    await update.callback_query.message.reply_text(
        "Select coin:", reply_markup=InlineKeyboardMarkup(kb)
    )

async def select_coin(update: Update, context):
    context.user_data["coin"] = update.callback_query.data.split("_")[1]
    await update.callback_query.message.reply_text("Enter amount (USDT):")
    context.user_data["await_amount"] = True

async def deposit_amount(update: Update, context):
    if not context.user_data.get("await_amount"):
        return

    amount = float(update.message.text)
    if amount < MIN_DEPOSIT:
        await update.message.reply_text("❌ Minimum deposit is $20")
        return

    context.user_data["amount"] = amount
    context.user_data["await_amount"] = False

    kb = [
        [
            InlineKeyboardButton("✅ Verify Payment", callback_data="verify"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel")
        ]
    ]

    await update.message.reply_text(
        f"Send {amount} {context.user_data['coin']} to demo wallet.\n\n"
        "Click Verify when done.",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def verify(update: Update, context):
    u = update.effective_user
    kb = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{u.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{u.id}")
        ]
    ]
    await context.bot.send_message(
        ADMIN_ID,
        f"💰 Deposit Request\nUser: {u.username}\nAmount: {context.user_data['amount']} USDT\nCoin: {context.user_data['coin']}",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    await update.callback_query.message.reply_text("⏳ Sent for admin review")

async def admin_deposit(update: Update, context):
    action, uid = update.callback_query.data.split("_")
    uid = int(uid)

    amount = context.user_data.get("amount", 0)

    if action == "confirm":
        update_user(uid, "balance", amount)
        update_user(uid, "deposited", amount)

        generate_card(
            "Deposit Confirmed",
            [f"User ID: {uid}", f"Amount: {amount} USDT", f"Time: {datetime.now()}"],
            f"deposit_{uid}.png"
        )

        await context.bot.send_message(uid, "✅ Deposit confirmed")
        await context.bot.send_message(
            CHANNEL_ID,
            f"💰 Deposit Confirmed\nUser: {uid}\nAmount: {amount} USDT"
        )
    else:
        await context.bot.send_message(uid, "❌ Deposit rejected")

# ================= WITHDRAWAL =================

async def withdraw(update: Update, context):
    await update.callback_query.message.reply_text("Enter withdrawal amount:")
    context.user_data["withdraw"] = True

async def process_withdraw(update: Update, context):
    if not context.user_data.get("withdraw"):
        return

    amount = float(update.message.text)
    user = get_user(update.effective_user.id)

    if amount > user[3]:
        await update.message.reply_text("❌ Insufficient balance")
        return

    context.user_data["withdraw"] = False

    kb = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"wok_{update.effective_user.id}_{amount}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"wno_{update.effective_user.id}")
        ]
    ]

    await context.bot.send_message(
        ADMIN_ID,
        f"📤 Withdrawal Request\nUser: {update.effective_user.username}\nAmount: {amount}",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def admin_withdraw(update: Update, context):
    data = update.callback_query.data.split("_")
    if data[0] == "wok":
        uid = int(data[1])
        amount = float(data[2])
        update_user(uid, "balance", -amount)
        update_user(uid, "withdrawn", amount)
        await context.bot.send_message(uid, "✅ Withdrawal approved")
        await context.bot.send_message(CHANNEL_ID, f"📤 Withdrawal: {amount} USDT")

# ================= TRADING ENGINE =================

async def trading_engine(context):
    cur.execute("SELECT user_id, balance FROM users")
    users = cur.fetchall()
    pool = sum(u[1] for u in users)

    if pool <= 0:
        return

    pair = random.choice(PAIRS)
    direction = random.choice(DIRECTIONS)
    leverage = random.choice(LEVERAGES)
    participants = len(users)

    win = random.random() > 0.25
    pnl = pool * (0.02 if win else -0.01)

    for uid, bal in users:
        share = bal / pool
        delta = pnl * share
        update_user(uid, "balance", delta)
        update_user(uid, "profit", delta)

    cur.execute("""
    UPDATE stats SET
        total_trades = total_trades + 1,
        wins = wins + ?,
        losses = losses + ?,
        capital = capital + ?,
        profit = profit + ?
    """, (1 if win else 0, 0 if win else 1, pool, pnl))

    db.commit()

    await context.bot.send_message(
        CHANNEL_ID,
        f"🔔 POOL TRADE CLOSED\nPair: {pair}\nPnL: {pnl:.2f} USDT"
    )

# ================= MAIN =================

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.PRIVATE, register))
    app.add_handler(CallbackQueryHandler(deposit, pattern="deposit"))
    app.add_handler(CallbackQueryHandler(select_coin, pattern="coin_"))
    app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
    app.add_handler(CallbackQueryHandler(admin_deposit, pattern="confirm_|reject_"))
    app.add_handler(CallbackQueryHandler(withdraw, pattern="withdraw"))
    app.add_handler(MessageHandler(filters.TEXT & filters.PRIVATE, deposit_amount))
    app.add_handler(MessageHandler(filters.TEXT & filters.PRIVATE, process_withdraw))
    app.add_handler(CallbackQueryHandler(admin_withdraw, pattern="wok_|wno_"))

    app.job_queue.run_repeating(trading_engine, interval=TRADE_INTERVAL, first=10)

    print("✅ Gothix AI Demo Bot Running")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
