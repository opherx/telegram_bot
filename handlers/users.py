# handlers/users.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import add_user  # your DB function

USERNAME, PASSWORD = range(2)

# ---- REGISTER ----

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start registration: ask for username."""
    await update.message.reply_text(
        "📝 *Registration*\n\n"
        "Please enter your desired username:",
        parse_mode="Markdown"
    )
    return USERNAME

async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store username and ask for password."""
    context.user_data['username'] = update.message.text
    await update.message.reply_text(
        "🔑 Great! Now enter your desired password:"
    )
    return PASSWORD

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store password, save user, and complete registration."""
    username = context.user_data['username']
    password = update.message.text
    tg_id = update.effective_user.id

    # Save user to DB
    add_user(tg_id, username, password)

    # Store user ID in bot_data safely
    if "USERS" not in context.bot_data:
        context.bot_data["USERS"] = []
    if tg_id not in context.bot_data["USERS"]:
        context.bot_data["USERS"].append(tg_id)

    # Confirmation message with emoji
    await update.message.reply_text(
        f"✅ Registration complete! Welcome, *{username}* 🎉\n\n"
        "💎 You can now:\n"
        "💰 /deposit - Add demo funds\n"
        "📤 /withdraw - Withdraw your balance\n"
        "📈 /trade - See trade signals\n"
        "ℹ️ /balance - Check your balance",
        parse_mode="Markdown"
    )

    return ConversationHandler.END
