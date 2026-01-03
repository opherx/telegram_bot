from database import cur, conn, update_pool
from config import ADMIN_ID

# CONFIRM DEPOSIT
async def admin_deposit_confirm(update, context):
    query = update.callback_query
    if query.from_user.id != ADMIN_ID:
        return

    deposit_id = int(query.data.split(":")[1])

    row = cur.execute("""
        SELECT user_id, amount
        FROM pending_deposits
        WHERE id=? AND status='PENDING'
    """, (deposit_id,)).fetchone()

    if not row:
        await query.edit_message_text("Already processed.")
        return

    cur.execute(
        "UPDATE pending_deposits SET status='APPROVED' WHERE id=?",
        (deposit_id,)
    )

    cur.execute("""
        UPDATE users
        SET balance=balance+?, total_deposited=total_deposited+?
        WHERE telegram_id=?
    """, (row["amount"], row["amount"], row["user_id"]))

    update_pool(row["amount"])
    conn.commit()

    await query.edit_message_text("Deposit approved.")

    await context.bot.send_message(
        chat_id=row["user_id"],
        text=f"Your deposit of {row['amount']} USDT was approved."
    )

# REJECT DEPOSIT
async def admin_deposit_reject(update, context):
    query = update.callback_query
    if query.from_user.id != ADMIN_ID:
        return

    deposit_id = int(query.data.split(":")[1])

    cur.execute(
        "UPDATE pending_deposits SET status='REJECTED' WHERE id=?",
        (deposit_id,)
    )
    conn.commit()

    await query.edit_message_text("Deposit rejected.")

# WITHDRAW APPROVAL (UNCHANGED)
async def admin_withdraw_approve(update, context):
    query = update.callback_query
    if query.from_user.id != ADMIN_ID:
        return

    withdraw_id = int(query.data.split(":")[1])

    row = cur.execute("""
        SELECT user_id, amount
        FROM pending_withdrawals
        WHERE id=? AND status='PENDING'
    """, (withdraw_id,)).fetchone()

    if not row:
        await query.edit_message_text("Already processed.")
        return

    cur.execute(
        "UPDATE pending_withdrawals SET status='APPROVED' WHERE id=?",
        (withdraw_id,)
    )

    cur.execute("""
        UPDATE users
        SET balance=balance-?, total_withdrawn=total_withdrawn+?
        WHERE telegram_id=?
    """, (row["amount"], row["amount"], row["user_id"]))

    update_pool(-row["amount"])
    conn.commit()

    await query.edit_message_text("Withdrawal approved.")

    await context.bot.send_message(
        chat_id=row["user_id"],
        text=f"Your withdrawal of {row['amount']} USDT was approved."
    )
