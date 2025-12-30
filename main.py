from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import database

database.create_tables()

# Simple auto-trade function
async def auto_trade(context: ContextTypes.DEFAULT_TYPE):
    print("Auto-trade executed")
    # Add logic to fetch price and update trades table

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /register or /login to begin.")

# /register command
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = context.args[0]
        password = context.args[1]
    except IndexError:
        await update.message.reply_text("Usage: /register <username> <password>")
        return

    if database.add_user(username, password):
        await update.message.reply_text(f"User {username} registered successfully!")
    else:
        await update.message.reply_text(f"Username {username} already exists.")

# /login command
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = context.args[0]
        password = context.args[1]
    except IndexError:
        await update.message.reply_text("Usage: /login <username> <password>")
        return

    user = database.get_user(username, password)
    if user:
        await update.message.reply_text(f"Welcome back, {username}!\nDashboard: /dashboard")
    else:
        await update.message.reply_text("Invalid username or password.")

# /dashboard command
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here’s your user dashboard. Trades and stats will appear here.")

# Main function
def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("dashboard", dashboard))

    # Auto-trading every 5 minutes
    app.job_queue.run_repeating(auto_trade, interval=300, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
