from database import cur

async def referral_menu(query):
    uid = query.from_user.id
    invited = cur.execute(
        "SELECT COUNT(*) FROM users WHERE referrer_id=?", (uid,)
    ).fetchone()[0]

    earnings = cur.execute(
        "SELECT referral_earnings FROM users WHERE telegram_id=?", (uid,)
    ).fetchone()[0]

    link = f"https://t.me/{query.message.chat.username}?start=ref_{uid}"

    await query.edit_message_text(
        f"👥 Referral Program\n\n"
        f"🔗 {link}\n\n"
        f"Invited: {invited}\n"
        f"Earnings: {earnings:.2f} USDT"
    )
