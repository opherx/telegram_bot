from images.generator import base_card, load_font

def generate_trade_open(data, filename="trade_open.png"):
    img, draw = base_card(
        title="NEW POSITION",
        qr_data=f"Trade #{data['trade_no']} | {data['pair']}"
    )

    draw.text((40, 90), data["pair"], font=load_font(46), fill="#facc15")
    draw.text((40, 150), f"${data['entry']:,.2f}", font=load_font(28), fill="#e5e7eb")

    y = 230
    lines = [
        f"Direction: {data['direction']}",
        f"Pool: {data['pool']:,.2f} USDT",
        f"Leverage: {data['leverage']}x",
        f"Participants: {data['participants']}",
        f"Trade #: {data['trade_no']}",
        f"Opened: {data['time']}"
    ]

    for line in lines:
        draw.text((40, y), line, font=load_font(22), fill="#cbd5f5")
        y += 34

    img.save(filename)
    return filename
