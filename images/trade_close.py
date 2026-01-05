from PIL import Image, ImageDraw
from images.generator import (
    font, rounded, paste_logo, paste_qr,
    BG_COLOR, CARD_COLOR, GOLD, GRAY, WHITE, GREEN, RED
)

W, H = 1200, 600


def generate_trade_close(data, filename="trade_close.png"):
    img = Image.new("RGB", (W, H), BG_COLOR)
    d = ImageDraw.Draw(img)

    # Decide colors/text based on result
    is_win = data["win"]
    title = "POSITION CLOSED - PROFIT" if is_win else "POSITION CLOSED - LOSS"
    accent = GREEN if is_win else RED

    # LEFT PANEL
    d.text((60, 60), data["pair"], font=font(52), fill=GOLD)
    d.text((60, 130), f"${data['exit']:,.2f}", font=font(36), fill=WHITE)
    d.text((60, 180), title, font=font(20), fill=accent)

    rounded(d, (60, 220, 200, 260), 18, accent)
    pnl_text = f"{'+' if is_win else ''}{data['pnl']:.2f} USDT"
    d.text((75, 228), pnl_text, font=font(20), fill="white")

    # RIGHT CARD
    card_x = 520
    rounded(d, (card_x, 60, 1120, 460), 28, CARD_COLOR)

    d.text((card_x + 40, 90), "TRADE SUMMARY", font=font(32), fill=GOLD)

    rows = [
        ("Entry Price", f"${data['entry']:,.2f}"),
        ("Exit Price", f"${data['exit']:,.2f}"),
        ("Pool Before", f"{data['pool_before']:,.2f} USDT"),
        ("Pool After", f"{data['pool_after']:,.2f} USDT"),
        ("Leverage", f"{data['leverage']}x"),
        ("Participants", str(data['participants'])),
        ("Trade #", str(data["trade_no"])),
    ]

    y = 150
    for k, v in rows:
        d.text((card_x + 40, y), k, font=font(20), fill=GRAY)
        d.text((card_x + 360, y), v, font=font(22), fill=WHITE)
        y += 45

    # BRAND BAR
    rounded(d, (0, 500, W, H), 0, "#d1d5db")
    paste_logo(img)
    paste_qr(img, data.get("qr", ""))

    img.save(filename)
    return filename
