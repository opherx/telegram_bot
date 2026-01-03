from handlers.ui import show_main_menu
from database import cur, conn

async def start(update, context):
    user = update.effective_user
    ref = None

    if context.args and context.args[0].startswith("ref_"):
        try:
            ref = int(context.args[0].split("_")[1])
            if ref == user.id:
                ref = None
        except:
            ref = None

    cur.execute("""
        INSERT OR IGNORE INTO users (telegram_id, username, referrer_id)
        VALUES (?, ?, ?)
    """, (user.id, user.username, ref))
    conn.commit()

    msg = await update.message.reply_text("Loading dashboard...")
    await show_main_menu(type("Q", (), {
        "from_user": user,
        "edit_message_text": msg.edit_text
    }))

