from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import FAKE_WALLETS, MIN_DEPOSIT
from database import cur, conn
from datetime import datetime

async def show_deposit_assets(query):
    kb = [[InlineKeyboardButton(a, callback_data=f"deposit_asset:{a}")]
          for a in FAKE_WALLETS]
    kb.append([InlineKeyboardButton("⬅ Back", callback_data="menu:main")])
    await query.edit_message_text("💰 Select deposit asset:", reply_markup=InlineKeyboardMarkup(kb))

async def deposit_select_asset(update, context):
    query = update.callback_query
    context.user_data["deposit_asset"] = query.data.split(":")[1]
    await query.edit_message_text(f"Enter deposit amount (min {MIN_DEPOSIT}):")

async def deposit_amount(update, context):
    try:
        amount = float(update.message.text)
    except:
        return

    if amount < MIN_DEPOSIT:
        await update.message.reply_text("❌ Below minimum.")
        return

    asset = context.user_data.get("deposit_asset")
    wallet = FAKE_WALLETS[asset]

    cur.execute("""
        INSERT INTO pending_deposits (user_id, asset, amount, status, created_at)
        VALUES (?, ?, ?, 'PENDING', ?)
    """, (update.effective_user.id, asset, amount, datetime.utcnow().isoformat()))
    conn.commit()

    await update.message.reply_text(
        f"Send {amount:.2f} USDT\nAsset: {asset}\nWallet:\n{wallet}"
    )
