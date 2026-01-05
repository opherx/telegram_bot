from PIL import Image, ImageDraw
from images.generator import (
    font, rounded, paste_logo, paste_qr,
    BG_COLOR, CARD_COLOR, GOLD, GRAY, WHITE, RED
)

W, H = 1200, 600


def generate_trade_open(data, filename="trade_open.png"):
    img = Image.new("RGB", (W, H), BG_COLOR)
    d = ImageDraw.Draw(img)

    # LEFT PANEL
    d.text((60, 60), data["pair"], font=font(52), fill=GOLD)
    d.text((60, 130), f"${data['entry']:,.2f}", font=font(36), fill=WHITE)
    d.text((60, 180), "POSITION OPENING", font=font(20), fill=GRAY)

    rounded(d, (60, 220, 150, 260), 18, RED)
    d.text((78, 228), data["direction"], font=font(20), fill="white")

    rounded(d, (160, 220, 230, 260), 18, GOLD)
    d.text((175, 228), f"{data['leverage']}x", font=font(20), fill="black")

    # RIGHT CARD
    card_x = 520
    rounded(d, (card_x, 60, 1120, 460), 28, CARD_COLOR)

    d.text((card_x + 40, 90), "NEW POSITION", font=font(32), fill=GOLD)
    d.text((card_x + 40, 140), "POSITION DETAILS", font=font(18), fill=GRAY)

    rows = [
        ("Entry Price", f"${data['entry']:,.2f}"),
        ("Position Size", f"{data['pool']:,.2f} USDT"),
        ("Leverage", f"{data['leverage']}x"),
        ("Participants", str(data['participants']))
    ]

    y = 190
    for k, v in rows:
        d.text((card_x + 40, y), k, font=font(20), fill=GRAY)
        d.text((card_x + 360, y), v, font=font(22), fill=WHITE)
        y += 55

    d.text(
        (card_x + 40, 410),
        "Position will be closed automatically",
        font=font(16),
        fill=GRAY
    )

    # BRAND BAR
    rounded(d, (0, 500, W, H), 0, "#d1d5db")
    paste_logo(img)
    paste_qr(img, data.get("qr", ""))

    img.save(filename)
    return filename
