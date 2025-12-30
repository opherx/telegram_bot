import os
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.register import register_handler
from handlers.wallet import deposit, balance, withdraw
from handlers.basic import start

TOKEN = os.getenv("RAILWAY_BOT_TOKEN")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(register_handler)
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("withdraw", withdraw))

    app.run_polling()

if __name__ == "__main__":
    main()
