from database import cur

async def user_trades(query):
    rows = cur.execute("""
        SELECT t.pair, ut.profit, t.created_at
        FROM user_trades ut
        JOIN trades t ON ut.trade_id = t.id
        WHERE ut.user_id=?
        ORDER BY t.id DESC LIMIT 10
    """, (query.from_user.id,)).fetchall()

    if not rows:
        await query.edit_message_text("No trades yet.")
        return

    text = "📈 Your Last Trades\n\n"
    for r in rows:
        text += f"{r['pair']} | +{r['profit']:.2f} | {r['created_at']}\n"

    await query.edit_message_text(text)
