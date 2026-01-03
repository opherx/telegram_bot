from database import cur, conn, update_pool
from config import ADMIN_ID

async def admin_withdraw_approve(update, context):
    q = update.callback_query
    if q.from_user.id != ADMIN_ID:
        return

    wid = int(q.data.split(":")[1])
    row = cur.execute(
        "SELECT user_id, amount FROM pending_withdrawals WHERE id=? AND status='PENDING'",
        (wid,)
    ).fetchone()

    if not row:
        return

    cur.execute("UPDATE pending_withdrawals SET status='APPROVED' WHERE id=?", (wid,))
    cur.execute("""
        UPDATE users
        SET balance=balance-?, total_withdrawn=total_withdrawn+?
        WHERE telegram_id=?
    """, (row["amount"], row["amount"], row["user_id"]))

    update_pool(-row["amount"])
    conn.commit()
    await q.edit_message_text("✅ Withdrawal approved.")
