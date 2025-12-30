from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import get_user, update_balance

WALLET, AMOUNT = range(2)

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    update_balance(tg_id, 100)
    await update.message.reply_text(
        f"💵 Congrats {update.effective_user.first_name}! $100 demo credited 🎉"
    )

async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📤 Enter your USDT wallet address:")
    return WALLET

async def withdraw_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet"] = update.message.text
    await update.message.reply_text("💰 Enter amount to withdraw:")
    return AMOUNT

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    amount = float(update.message.text)
    user = get_user(tg_id)

    if amount > user[3]:
        await update.message.reply_text("❌ Insufficient balance.")
    else:
        wallet = context.user_data["wallet"]
        update_balance(tg_id, -amount)
        await update.message.reply_text(
            f"✅ Withdrawal of ${amount} to `{wallet}` is being processed 🕒",
            parse_mode="Markdown"
        )
    return ConversationHandler.END
