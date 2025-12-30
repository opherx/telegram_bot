from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import add_user, get_user

USERNAME, PASSWORD = range(2)

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Enter your username:")
    return USERNAME

async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("🔐 Enter your password:")
    return PASSWORD

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data["username"]
    password = update.message.text
    tg_id = update.effective_user.id
    add_user(tg_id, username, password)

    # Add to bot's user list
    tg_id = update.effective_user.id

# Initialize USERS list if it doesn't exist
if "USERS" not in context.bot_data:
    context.bot_data["USERS"] = []

context.bot_data["USERS"].append(tg_id)


    await update.message.reply_text(f"✅ Registration complete! Welcome, {username} 🎉")
    return ConversationHandler.END
