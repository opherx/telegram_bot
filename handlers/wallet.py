from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import get_user, update_balance

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_balance(update.effective_user.id, 100)
    await update.message.reply_text("💰 $100 credited successfully (Demo).")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not user:
        await update.message.reply_text("❌ Please register first.")
        return
    await update.message.reply_text(f"💳 Balance: ${user[3]}")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📤 Withdrawal request received.\n(Approved automatically for demo)"
    )

