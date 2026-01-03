from handlers.ui import show_main_menu
from handlers.deposit import show_deposit_assets, deposit_select_asset
from handlers.referral import referral_menu
from handlers.performance import performance_menu
from handlers.trades import user_trades
from handlers.admin import admin_withdraw_approve

async def callback_router(update, context):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data.startswith("menu:"):
        page = data.split(":")[1]
        if page == "main":
            await show_main_menu(q)
        elif page == "deposit":
            await show_deposit_assets(q)
        elif page == "withdraw":
            await q.edit_message_text("Use /withdraw <amount>")
        elif page == "performance":
            await performance_menu(q)
        elif page == "trades":
            await user_trades(q)
        elif page == "referral":
            await referral_menu(q)

    elif data.startswith("deposit_asset:"):
        await deposit_select_asset(update, context)

    elif data.startswith("admin_withdraw:"):
        await admin_withdraw_approve(update, context)
