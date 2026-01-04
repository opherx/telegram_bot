from images.generator import base_card, load_font

def generate_trade_close(data, filename="trade_close.png"):
    title = "POSITION CLOSED - PROFIT" if data["win"] else "POSITION CLOSED - LOSS"

    img, draw = base_card(
        title=title,
        qr_data=f"Trade #{data['trade_no']} | PNL {data['pnl']}"
    )

    color = "#22c55e" if data["win"] else "#ef4444"

    draw.text((40, 90), data["pair"], font=load_font(42), fill="#facc15")
    draw.text((40, 150), f"P&L: {data['pnl']}", font=load_font(30), fill=color)

    y = 230
    lines = [
        f"Entry: {data['entry']:,.2f}",
        f"Exit: {data['exit']:,.2f}",
        f"Pool Before: {data['pool_before']:,.2f}",
        f"Pool After: {data['pool_after']:,.2f}",
        f"Trade #: {data['trade_no']}",
        f"Closed: {data['time']}"
    ]

    for line in lines:
        draw.text((40, y), line, font=load_font(22), fill="#cbd5f5")
        y += 34

    img.save(filename)
    return filename
