# handlers/payments.py

from telegram import Update
from telegram.ext import ContextTypes
from database import get_user, update_balance

# Conversation states
WALLET, AMOUNT = range(2)

# -------- DEPOSIT --------
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.message.from_user.id
    user = get_user(tg_id)
    if not user:
        await update.message.reply_text("❌ You are not registered. Use /register first.")
        return
    # Simulate deposit of $100
    update_balance(tg_id, 100)
    await update.message.reply_text(f"💰 Deposit successful! Your balance: ${user['balance']:.2f}")

# -------- WITHDRAW --------
async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.message.from_user.id
    user = get_user(tg_id)
    if not user:
        await update.message.reply_text("❌ You are not registered. Use /register first.")
        return
    await update.message.reply_text("📤 Please enter your wallet address:")
    return WALLET

async def withdraw_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet"] = update.message.text
    await update.message.reply_text("📤 Enter the amount to withdraw:")
    return AMOUNT

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.message.from_user.id
    user = get_user(tg_id)
    amount_text = update.message.text

    try:
        amount = float(amount_text)
    except ValueError:
        await update.message.reply_text("❌ Invalid amount. Please enter a number:")
        return AMOUNT

    if amount > user["balance"]:
        await update.message.reply_text("❌ Insufficient balance.")
        return AMOUNT

    update_balance(tg_id, -amount)
    wallet = context.user_data.get("wallet", "N/A")
    await update.message.reply_text(
        f"✅ Withdrawal of ${amount:.2f} to wallet {wallet} successful!\n"
        f"💰 New balance: ${user['balance']:.2f}"
    )
    return -1  # End of conversation
