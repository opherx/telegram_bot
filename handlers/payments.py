from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import get_db

WALLET, AMOUNT = range(2)

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = get_db()
    c = db.cursor()

    c.execute(
        "UPDATE users SET balance = balance + 100 WHERE telegram_id = ?",
        (update.effective_user.id,)
    )

    db.commit()
    db.close()

    await update.message.reply_text(
        "✅ Deposit Successful\n\nAmount: $100\nStatus: Confirmed"
    )

async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💳 Enter USDT wallet address:")
    return WALLET

async def withdraw_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet"] = update.message.text
    await update.message.reply_text("💰 Enter amount to withdraw:")
    return AMOUNT

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = float(update.message.text)
    user_id = update.effective_user.id

    db = get_db()
    c = db.cursor()

    c.execute("SELECT balance FROM users WHERE telegram_id = ?", (user_id,))
    balance = c.fetchone()[0]

    if amount > balance:
        await update.message.reply_text("❌ Insufficient balance.")
        return ConversationHandler.END

    c.execute(
        "UPDATE users SET balance = balance - ? WHERE telegram_id = ?",
        (amount, user_id)
    )

    db.commit()
    db.close()

    await update.message.reply_text(
        f"✅ Withdrawal Successful\n\nAmount: ${amount}\nStatus: Processing"
    )

    return ConversationHandler.END

