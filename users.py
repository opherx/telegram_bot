from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import get_db

USERNAME, PASSWORD = range(2)

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Enter a username:")
    return USERNAME

async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("🔐 Enter a password:")
    return PASSWORD

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    user_id = update.effective_user.id
    username = context.user_data["username"]

    db = get_db()
    c = db.cursor()

    c.execute(
        "INSERT OR REPLACE INTO users (telegram_id, username, password, balance) VALUES (?, ?, ?, ?)",
        (user_id, username, password, 0)
    )

    db.commit()
    db.close()

    await update.message.reply_text(
        f"✅ Registration successful!\n\nUsername: {username}\nBalance: $0"
    )
    return ConversationHandler.END
