from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters
from database import add_user

USERNAME, PASSWORD = range(2)

async def start_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Enter a username:")
    return USERNAME

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("🔐 Enter a password:")
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(
        update.effective_user.id,
        context.user_data["username"],
        update.message.text
    )
    await update.message.reply_text("✅ Registration successful!")
    return ConversationHandler.END


register_handler = ConversationHandler(
    entry_points=[CommandHandler("register", start_register)],
    states={
        USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
    },
    fallbacks=[]
)

