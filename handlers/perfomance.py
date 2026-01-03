from images.performance import generate_performance_card

async def performance_menu(query):
    img = generate_performance_card()
    await query.message.reply_photo(photo=img, caption="📊 Platform Performance")
