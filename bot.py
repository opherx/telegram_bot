from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from config import BOT_TOKEN, CHANNEL_ID
from database import init_db
from handlers.user import start
from handlers.router import callback_router
from handlers.deposit import deposit_amount
from handlers.withdraw import withdraw_request
from handlers.auth import set_pin
from services.trading import run_trade


def main():
    # Initialize database
    init_db()

    # Build application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.bot_data["CHANNEL_ID"] = CHANNEL_ID

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("withdraw", withdraw_request))
    app.add_handler(CommandHandler("setpin", set_pin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount))
    app.add_handler(CallbackQueryHandler(callback_router))

    # Background trading job
    app.job_queue.run_repeating(run_trade, interval=300, first=30)

    # Start polling (PTB manages the event loop internally)
    app.run_polling()


if __name__ == "__main__":
    main()
