from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import cur, conn, update_pool
from config import ADMIN_ID
from datetime import datetime


# =========================
# DEPOSIT APPROVAL (ADMIN)
# =========================

async def admin_deposit_confirm(update, context):
    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer("Unauthorized", show_alert=True)
        return

    deposit_id = int(query.data.split(":")[1])

    row = cur.execute("""
        SELECT user_id, asset, amount
        FROM pending_deposits
        WHERE id=? AND status='PENDING'
    """, (deposit_id,)).fetchone()

    if not row:
        await query.answer("Deposit already processed.", show_alert=True)
        return

    # Update deposit status
    cur.execute(
        "UPDATE pending_deposits SET status='APPROVED' WHERE id=?",
        (deposit_id,)
    )

    # Update user balance
    cur.execute("""
        UPDATE users
        SET balance = balance + ?,
            total_deposited = total_deposited + ?
        WHERE telegram_id = ?
    """, (row["amount"], row["amount"], row["user_id"]))

    # Update pool balance
    update_pool(row["amount"])
    conn.commit()

    await query.edit_message_text("✅ Deposit confirmed successfully.")

    # Notify user
    await context.bot.send_message(
        chat_id=row["user_id"],
        text=(
            "✅ **Deposit Approved**\n\n"
            f"🪙 Asset: {row['asset']}\n"
            f"💵 Amount: {row['amount']} USDT\n"
            f"🕒 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        ),
        parse_mode="Markdown"
    )


async def admin_deposit_reject(update, context):
    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer("Unauthorized", show_alert=True)
        return

    deposit_id = int(query.data.split(":")[1])

    row = cur.execute("""
        SELECT user_id
        FROM pending_deposits
        WHERE id=? AND status='PENDING'
    """, (deposit_id,)).fetchone()

    if not row:
        await query.answer("Deposit already processed.", show_alert=True)
        return

    cur.execute(
        "UPDATE pending_deposits SET status='REJECTED' WHERE id=?",
        (deposit_id,)
    )
    conn.commit()

    await query.edit_message_text("❌ Deposit rejected.")

    await context.bot.send_message(
        chat_id=row["user_id"],
        text="❌ Your deposit was marked as *Not Received*. Please contact support.",
        parse_mode="Markdown"
    )


# =========================
# WITHDRAW APPROVAL (ADMIN)
# =========================

async def admin_withdraw_approve(update, context):
    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer("Unauthorized", show_alert=True)
        return

    withdraw_id = int(query.data.split(":")[1])

    row = cur.execute("""
        SELECT user_id, amount
        FROM pending_withdrawals
        WHERE id=? AND status='PENDING'
    """, (withdraw_id,)).fetchone()

    if not row:
        await query.answer("Already processed.", show_alert=True)
        return

    cur.execute(
        "UPDATE pending_withdrawals SET status='APPROVED' WHERE id=?",
        (withdraw_id,)
    )

    cur.execute("""
        UPDATE users
        SET balance = balance - ?,
            total_withdrawn = total_withdrawn + ?
        WHERE telegram_id = ?
    """, (row["amount"], row["amount"], row["user_id"]))

    update_pool(-row["amount"])
    conn.commit()

    await query.edit_message_text("✅ Withdrawal approved.")

    await context.bot.send_message(
        chat_id=row["user_id"],
        text=f"✅ Your withdrawal of {row['amount']} USDT has been approved."
    )
