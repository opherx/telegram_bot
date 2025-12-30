from telegram import Update, ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from database import (
    create_user,
    get_user,
    update_balance,
    deduct_balance,
)
from jobs.trade_engine import send_trade

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "YOUR_CHANNEL_ID"

# ----- Registration flow -----
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your username:")
    return 1  # Step 1 for conversation

async def username_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("Now enter your password:")
    return 2  # Step 2 for conversation

async def password_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    username = context.user_data["username"]
    create_user(username, password, balance=100)  # Auto credit $100
    await update.message.reply_text(f"✅ Registered {username} with $100 balance!")
    return -1  # End of conversation

# ----- Deposit -----
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.message.from_user.id)
    if not user:
        await update.message.reply_text("❌ You need to /register first.")
        return
    update_balance(user["id"], user["balance"] + 100)
    await update.message.reply_text("💰 $100 deposited automatically!")

# ----- Withdraw -----
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter the USDT wallet address:")
    return 1

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet = update.message.text
    await update.message.reply_text("Enter the amount to withdraw:")
    context.user_data["wallet"] = wallet
    return 2

async def withdraw_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = float(update.message.text)
    user = get_user(update.message.from_user.id)
    if user["balance"] < amount:
        await update.message.reply_text("❌ Not enough balance!")
        return -1
    deduct_balance(user["id"], amount)
    await update.message.reply_text(f"✅ Withdrawal of {amount} USDT sent to {context.user_data['wallet']}")
    return -1

# ----- Main -----
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.bot_data["CHANNEL_ID"] = int(CHANNEL_ID)

    # Commands
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("withdraw", withdraw))

    # Job queue for trades every 5 minutes
    app.job_queue.run_repeating(send_trade, interval=300, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
