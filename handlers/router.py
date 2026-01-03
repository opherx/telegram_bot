from handlers.ui import show_main_menu
from handlers.deposit import (
    show_deposit_assets,
    deposit_select_asset,
    deposit_verify
)
from handlers.referral import referral_menu
from handlers.performance import performance_menu
from handlers.trades import user_trades
from handlers.admin import (
    admin_deposit_confirm,
    admin_deposit_reject,
    admin_withdraw_approve
)

async def callback_router(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    # MENU ROUTES
    if data.startswith("menu:"):
        page = data.split(":")[1]

        if page == "main":
            await show_main_menu(query)
        elif page == "deposit":
            await show_deposit_assets(query)
        elif page == "withdraw":
            await query.edit_message_text("Use /withdraw <amount>")
        elif page == "performance":
            await performance_menu(query)
        elif page == "trades":
            await user_trades(query)
        elif page == "referral":
            await referral_menu(query)

    # DEPOSIT (USER)
    elif data.startswith("deposit_asset:"):
        await deposit_select_asset(update, context)

    elif data == "deposit_verify":
        await deposit_verify(update, context)

    # DEPOSIT (ADMIN)
    elif data.startswith("admin_deposit_confirm:"):
        await admin_deposit_confirm(update, context)

    elif data.startswith("admin_deposit_reject:"):
        await admin_deposit_reject(update, context)

    # WITHDRAW (ADMIN)
    elif data.startswith("admin_withdraw:"):
        await admin_withdraw_approve(update, context)
