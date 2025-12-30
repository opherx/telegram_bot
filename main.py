import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
from database import add_user, get_user
from trades import simulate_trade
from screenshot import generate_trade_screenshot
import random

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 8443))
RAILWAY_URL = os.environ.get("RAILWAY_STATIC_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Demo Trading Bot\nUse /register username password to start.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /register <username> <password>")
        return
    username, password = context.args
    add_user(update.effective_user.id, username, password)
    await update.message.reply_text(f"✅ Registered {username}. Balance: $100")

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not user:
        await update.message.reply_text("❌ You need to register first.")
        return
    await update.message.reply_text(f"📊 Dashboard\nUsername: {user[1]}\nBalance: ${user[3]:.2f}")

async def auto_trade_job(context: ContextTypes.DEFAULT_TYPE):
    for user_id in [row[0] for row in context.bot_data.get("users", [])]:
        pnl, balance = simulate_trade(user_id)
        screenshot_file = generate_trade_screenshot(pnl, balance)
        try:
            await context.bot.send_photo(chat_id=user_id, photo=open(screenshot_file, "rb"))
        except:
            pass

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("dashboard", dashboard))

    # Add job queue
    app.job_queue.run_repeating(auto_trade_job, interval=300, first=10)

    # Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url_path=TOKEN,
        webhook_url=f"{RAILWAY_URL}/{TOKEN}"
    )

main()
