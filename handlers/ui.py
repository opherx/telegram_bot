from telegram import InlineKeyboardButton, InlineKeyboardMarkup

ABOUT_TEXT = (
    "CASHIFY AI BOT simulates pooled algorithmic trading.\n\n"
    "All trades and balances are virtual and for demonstration only."
)

HOW_IT_WORKS = (
    "• Users pool demo funds\n"
    "• Trades open & close automatically\n"
    "• Profits are distributed proportionally\n"
    "• No real money is involved"
)


async def show_about(update, context):
    await update.callback_query.edit_message_text(ABOUT_TEXT)


async def show_how(update, context):
    await update.callback_query.edit_message_text(HOW_IT_WORKS)
