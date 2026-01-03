from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from config import FAKE_WALLETS, MIN_DEPOSIT, ADMIN_ID
from database import cur, conn

# STEP 1 — SHOW ASSETS
async def show_deposit_assets(query):
    keyboard = [
        [InlineKeyboardButton(asset, callback_data=f"deposit_asset:{asset}")]
        for asset in FAKE_WALLETS
    ]
    keyboard.append([InlineKeyboardButton("⬅ Back", callback_data="menu:main")])

    await query.edit_message_text(
        "Select deposit asset:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# STEP 2 — ASSET SELECTED
async def deposit_select_asset(update, context):
    query = update.callback_query
    asset = query.data.split(":")[1]
    context.user_data["deposit_asset"] = asset

    await query.edit_message_text(
        f"Asset selected: {asset}\n\nEnter deposit amount (min {MIN_DEPOSIT} USDT):"
    )

# STEP 3 — AMOUNT ENTERED
async def deposit_amount(update, context):
    try:
        amount = float(update.message.text)
    except ValueError:
        await update.message.reply_text("Enter a valid number.")
        return

    if amount < MIN_DEPOSIT:
        await update.message.reply_text(f"Minimum deposit is {MIN_DEPOSIT} USDT.")
        return

    asset = context.user_data.get("deposit_asset")
    if not asset:
        await update.message.reply_text("Please start deposit from menu.")
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
            InlineKeyboardButton("Verify Payment", callback_data="deposit_verify"),
            InlineKeyboardButton("Cancel", callback_data="menu:main")
        ]
    ])

    await update.message.reply_text(
        f"Send {amount:.2f} USDT\n"
        f"Asset: {asset}\n"
        f"Wallet:\n{wallet}\n\n"
        "After payment, click Verify Payment.",
        reply_markup=keyboard
    )

# STEP 4 — USER VERIFIES → ADMIN DM
async def deposit_verify(update, context):
    query = update.callback_query
    deposit_id = context.user_data.get("deposit_id")

    if not deposit_id:
        await query.answer("Deposit not found", show_alert=True)
        return

    row = cur.execute("""
        SELECT asset, amount FROM pending_deposits
        WHERE id=? AND status='PENDING'
    """, (deposit_id,)).fetchone()

    if not row:
        await query.answer("Already processed", show_alert=True)
        return

    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Confirm Deposit",
                callback_data=f"admin_deposit_confirm:{deposit_id}"
            ),
            InlineKeyboardButton(
                "Reject",
                callback_data=f"admin_deposit_reject:{deposit_id}"
            )
        ]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "New Deposit Request\n\n"
            f"User ID: {query.from_user.id}\n"
            f"Asset: {row['asset']}\n"
            f"Amount: {row['amount']} USDT\n"
            f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        ),
        reply_markup=admin_keyboard
    )

    await query.edit_message_text(
        "Payment submitted. Awaiting admin confirmation."
    )
