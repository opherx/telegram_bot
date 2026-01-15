from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# =======================
# TEXT CONTENT
# =======================

ABOUT_TEXT = (
    "🤖 *CASHIFY AI BOT*\n\n"
    "CASHIFY AI BOT simulates a pooled algorithmic trading platform.\n\n"
    "All trades, balances, and profits are *virtual* and intended for "
    "demonstration and testing purposes only.\n\n"
    "No real funds are used."
)

HOW_IT_WORKS_TEXT = (
    "⚙️ *How It Works*\n\n"
    "• Users deposit demo funds into a shared pool\n"
    "• The system opens and closes simulated trades automatically\n"
    "• Each trade produces a profit or loss\n"
    "• Results are distributed proportionally\n"
    "• Trading runs during active market hours only\n\n"
    "This bot is a demo — not a real trading platform."
)

# =======================
# MAIN MENU (RESTORED)
# =======================

async def show_main_menu(target):
    """
    target can be:
    - update.message (from /start)
    - callback_query (from buttons)
    """

    keyboard = [
        [
            InlineKeyboardButton("💰 Balance", callback_data="menu:balance"),
            InlineKeyboardButton("📈 Trades", callback_data="menu:trades"),
        ],
        [
            InlineKeyboardButton("➕ Deposit", callback_data="menu:deposit"),
            InlineKeyboardButton("➖ Withdraw", callback_data="menu:withdraw"),
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="menu:about"),
            InlineKeyboardButton("⚙️ How It Works", callback_data="menu:how"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Called from /start
    if hasattr(target, "reply_text"):
        await target.reply_text(
            "Welcome to *CASHIFY AI BOT* 🚀\n\n"
            "Select an option below:",
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )
    else:
        # Called from callback
        await target.edit_message_text(
            "Main Menu:",
            reply_markup=reply_markup,
        )

# =======================
# ABOUT & HOW IT WORKS
# =======================

async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        ABOUT_TEXT,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="menu:main")]]
        ),
    )


async def show_how_it_works(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        HOW_IT_WORKS_TEXT,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="menu:main")]]
        ),
    )
