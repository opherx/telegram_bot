from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import cur, conn, update_pool
from config import ADMIN_ID

async def withdraw_request(update, context):
    try:
        amount = float(context.args[0])
    except:
        await update.message.reply_text("Usage: /withdraw <amount>")
        return

    bal = cur.execute(
        "SELECT balance FROM users WHERE telegram_id=?",
        (update.effective_user.id,)
    ).fetchone()["balance"]

    if amount <= 0 or amount > bal:
        await update.message.reply_text("❌ Invalid amount.")
        return

    cur.execute("""
        INSERT INTO pending_withdrawals (user_id, wallet, amount, status, created_at)
        VALUES (?, 'demo_wallet', ?, 'PENDING', ?)
    """, (update.effective_user.id, amount, datetime.utcnow().isoformat()))
    conn.commit()

    wid = cur.lastrowid
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Approve", callback_data=f"admin_withdraw:{wid}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"admin_withdraw_reject:{wid}")]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Withdrawal request\nUser: {update.effective_user.id}\nAmount: {amount}",
        reply_markup=kb
    )
    await update.message.reply_text("⏳ Withdrawal request submitted.")
