from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import cur, get_pool_balance

async def show_main_menu(query):
    user = cur.execute(
        "SELECT balance FROM users WHERE telegram_id=?",
        (query.from_user.id,)
    ).fetchone()

    balance = user["balance"] if user else 0
    pool = get_pool_balance()

    text = (
        "🤖 AI Trading Platform (DEMO)\n\n"
        f"💰 Your Balance: {balance:.2f} USDT\n"
        f"🏦 Pool Balance: {pool:,.2f} USDT\n"
        "📊 Status: ACTIVE"
    )

    keyboard = [
        [InlineKeyboardButton("💰 Deposit", callback_data="menu:deposit"),
         InlineKeyboardButton("🏧 Withdraw", callback_data="menu:withdraw")],
        [InlineKeyboardButton("📊 Performance", callback_data="menu:performance"),
         InlineKeyboardButton("📈 Trades", callback_data="menu:trades")],
        [InlineKeyboardButton("👥 Referral", callback_data="menu:referral")]
    ]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
