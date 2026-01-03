from database import cur, conn

async def set_pin(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /setpin <4-digit-pin>")
        return

    pin = context.args[0]
    if not pin.isdigit() or len(pin) != 4:
        await update.message.reply_text("PIN must be 4 digits.")
        return

    cur.execute(
        "UPDATE users SET pin=? WHERE telegram_id=?",
        (pin, update.effective_user.id)
    )
    conn.commit()
    await update.message.reply_text("✅ PIN set.")
