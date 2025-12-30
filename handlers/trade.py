from telegram import Update
from telegram.ext import ContextTypes
from jobs.trade_engine import send_trade

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual trigger to send a trade signal"""
    await send_trade(context)
    await update.message.reply_text("📊 Trade signal sent to the channel! Check it out 🚀")
