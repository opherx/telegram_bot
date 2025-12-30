from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import get_user, update_balance

WALLET, AMOUNT = range(2)

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto credit $100 to user balance (demo)."""
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Please register first using /register.")
        return
    update_balance(user_id, 100)
    await update.message.reply_text("✅ Deposit successful! $100 credited (Demo).")

# ---- Withdraw Flow ----
async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not get_user(user_id):
        await update.message.reply_text("❌ Please register first using /register.")
        return ConversationHandler.END
    await update.message.reply_text("💳 Enter your USDT wallet address:")
    return WALLET

async def withdraw_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet"] = update.message.text
    await update.message.reply_text("💰 Enter amount to withdraw:")
    return AMOUNT

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    amount = float(update.message.text)
    user = get_user(user_id)
    if amount > user[3]:  # index 3 = balance
        await update.message.reply_text("❌ Insufficient balance.")
        return ConversationHandler.END
    update_balance(user_id, -amount)
    wallet = context.user_data["wallet"]
    await update.message.reply_text(
        f"✅ Withdrawal successful!\nAmount: ${amount}\nWallet: {wallet}\nStatus: Processing"
    )
    return ConversationHandler.END
