from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import add_user, get_user

USERNAME, PASSWORD = range(2)

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start registration and ask for username."""
    await update.message.reply_text("👤 Enter a username:")
    return USERNAME

async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store username and ask for password."""
    context.user_data["username"] = update.message.text
    await update.message.reply_text("🔐 Enter a password:")
    return PASSWORD

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save user to database and finish registration."""
    username = context.user_data["username"]
    password = update.message.text
    user_id = update.effective_user.id

    # Use your existing database function to add the user
    add_user(user_id, username, password)

    await update.message.reply_text(
        f"✅ Registration successful!\n\nUsername: {username}\nBalance: $0"
    )
    return ConversationHandler.END
