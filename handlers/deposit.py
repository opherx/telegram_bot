from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from config import FAKE_WALLETS, MIN_DEPOSIT, ADMIN_ID
from database import cur, conn, update_pool

# STEP 1: show asset list
async def show_deposit_assets(query):
    keyboard = [
        [InlineKeyboardButton(asset, callback_data=f"deposit_asset:{asset}")]
        for asset in FAKE_WALLETS
    ]
    keyboard.append([InlineKeyboardButton("⬅ Back", callback_data="menu:main")])

    await query.edit_message_text(
        "💰 Select deposit asset:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# STEP 2: asset selected
async def deposit_select_asset(update, context):
    query = update.callback_query
    asset = query.data.split(":")[1]
    context.user_data["deposit_asset"] = asset

    await query.edit_message_text(
        f"🪙 Asset selected: {asset}\n\n"
        f"Enter deposit amount (minimum {MIN_DEPOSIT} USDT):"
    )


# STEP 3: amount entered
async def deposit_amount(update, context):
    try:
        amount = float(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number.")
        return

    if amount < MIN_DEPOSIT:
        await update.message.reply_text(
            f"❌ Minimum deposit is {MIN_DEPOSIT} USDT."
        )
        return

    asset = context.user_data.get("deposit_asset")
    if not asset:
        await update.message.reply_text("❌ Please start deposit from the menu.")
        return

    wallet = FAKE_WALLETS[asset]

    cur.execute("""
        INSERT INTO pending_deposits (user_id, asset, amount, status, created_at)
        VALUES (?, ?, ?, 'PENDING', ?)
    """, (
        update.effective_user.id,
        asset,
        amount,
        datetime.utcnow().isoformat()
    ))
    conn.commit()

    deposit_id = cur.lastrowid
    context.user_data["deposit_id"] = deposit_id

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Verify Payment", callback_data="deposit_verify"),
            InlineKeyboardButton("❌ Cancel", callback_data="menu:main")
        ]
    ])

    await update.message.reply_text(
        f"💰 **Deposit Instructions**\n\n"
        f"🪙 Asset: {asset}\n"
        f"💵 Amount: {amount:.2f} USDT\n\n"
        f"📥 Send funds to:\n`{wallet}`\n\n"
        f"⚠️ Send only {asset} on the correct network.\n\n"
        f"After payment, click **Verify Payment**.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# STEP 4: user clicks VERIFY → notify admin
async def deposit_verify(update, context):
    query = update.callback_query
    user = query.from_user
    deposit_id = context.user_data.get("deposit_id")

    if not deposit_id:
        await query.answer("Deposit not found.", show_alert=True)
        return

    row = cur.execute("""
        SELECT asset, amount FROM pending_deposits
        WHERE id=? AND status='PENDING'
    """, (deposit_id,)).fetchone()

    if not row:
        await query.answer("Deposit already processed.", show_alert=True)
        return

    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirm Deposit",
                                 callback_data=f"admin_deposit_confirm:{deposit_id}"),
            InlineKeyboardButton("❌ Not Received",
                                 callback_data=f"admin_deposit_reject:{deposit_id}")
        ]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "💰 **New Deposit Request**\n\n"
            f"👤 User: @{user.username or user.id}\n"
            f"🪙 Asset: {row['asset']}\n"
            f"💵 Amount: {row['amount']} USDT\n"
            f"🕒 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        ),
        reply_markup=admin_keyboard,
        parse_mode="Markdown"
    )

    await query.edit_message_text(
        "⏳ Payment verification sent.\n\n"
        "Please wait for admin confirmation."
    )
