from telegram import Update
from telegram.ext import ContextTypes
from jobs.trade_engine import send_trade

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual trigger to send a trade to the channel."""
    channel_id = context.bot_data.get("CHANNEL_ID")
    if not channel_id:
        await update.message.reply_text("Channel not set.")
        return
    await send_trade(context)
    await update.message.reply_text("Trade signal sent!")

