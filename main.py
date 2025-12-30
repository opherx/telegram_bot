import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from database import init_db
from users import register_start, register_username, register_password, USERNAME, PASSWORD
from payments import deposit, withdraw_start, withdraw_wallet, withdraw_amount, WALLET, AMOUNT
from trades import generate_trade

TOKEN = os.getenv("RAILWAY_BOT_TOKEN")

def main():
    if not TOKEN:
        print("❌ RAILWAY_BOT_TOKEN not set")
        return

    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    register_conv = ConversationHandler(
        entry_points=[CommandHandler("register", register_start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_username)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_password)],
        },
        fallbacks=[]
    )

    withdraw_conv = ConversationHandler(
        entry_points=[CommandHandler("withdraw", withdraw_start)],
        states={
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_wallet)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount)],
        },
        fallbacks=[]
    )

    app.add_handler(register_conv)
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(withdraw_conv)

    app.run_polling()

if __name__ == "__main__":
    main()
