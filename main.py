import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# Environment token
TOKEN = os.environ.get("RAILWAY_BOT_TOKEN")

# In-memory storage (replace with DB for production)
users = {}
balances = {}

# Registration steps
USERNAME, PASSWORD = range(2)
WITHDRAW_WALLET, WITHDRAW_AMOUNT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Use /register to create an account, /deposit to get funds, "
        "/withdraw to withdraw, and /trade to see trades."
    )

# ---- REGISTER ----
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your desired username:")
    return USERNAME

async def reg_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Enter your desired password:")
    return PASSWORD

async def reg_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data['username']
    password = update.message.text
    users[update.effective_user.id] = {'username': username, 'password': password}
    balances[update.effective_user.id] = 0
    await update.message.reply_text(f"Registered successfully! Welcome, {username}.")
    return ConversationHandler.END

# ---- DEPOSIT ----
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users:
        await update.message.reply_text("You must register first with /register")
        return
    balances[uid] += 100
    await update.message.reply_text("Deposit successful! $100 credited to your account.")

# ---- WITHDRAW ----
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users:
        await update.message.reply_text("You must register first with /register")
        return ConversationHandler.END
    await update.message.reply_text("Enter your USDT wallet address:")
    return WITHDRAW_WALLET

async def withdraw_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['wallet'] = update.message.text
    await update.message.reply_text("Enter amount to withdraw:")
    return WITHDRAW_AMOUNT

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    amount = float(update.message.text)
    if amount > balances.get(uid, 0):
        await update.message.reply_text("Insufficient balance.")
    else:
        balances[uid] -= amount
        wallet = context.user_data['wallet']
        await update.message.reply_text(f"Withdrawal of ${amount} to {wallet} successful!")
    return ConversationHandler.END

# ---- TRADE SIMULATION ----
async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example simulated trade
    await update.message.reply_text("Trade signal: BUY BTC/USDT at 30000, TP: 30500, SL: 29500")

async def trade_simulation(context: ContextTypes.DEFAULT_TYPE):
    for uid in users:
        await context.bot.send_message(chat_id=uid, text="Trade update: BUY ETH/USDT at 1800, TP: 1850, SL: 1750")

# ---- MAIN ----
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Registration handler
    reg_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_username)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_password)],
        },
        fallbacks=[]
    )

    withdraw_handler = ConversationHandler(
        entry_points=[CommandHandler('withdraw', withdraw)],
        states={
            WITHDRAW_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_wallet)],
            WITHDRAW_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(reg_handler)
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(withdraw_handler)
    app.add_handler(CommandHandler("trade", trade))

    # Run simulated trades every 60 seconds
    if app.job_queue:
        app.job_queue.run_repeating(trade_simulation, interval=60, first=10)

    app.run_polling()

if __name__ == "__main__":
    if not TOKEN:
        print("Error: Set RAILWAY_BOT_TOKEN environment variable!")
    else:
        main()
