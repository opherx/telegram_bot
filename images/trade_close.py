from PIL import Image, ImageDraw
from images.generator import *
from utils.formatters import format_pool

W, H = 1200, 600


def generate_trade_close(data, filename="trade_close.png"):
    img = Image.new("RGB", (W, H), BG_COLOR)
    d = ImageDraw.Draw(img)

    win = data["win"]
    accent = GREEN if win else RED
    pnl = float(data["pnl"])

    d.text((60, 60), data["pair"], font=font(52), fill=GOLD)
    d.text((60, 130), f"{'+' if win else ''}{pnl:,.2f} USDT", font=font(36), fill=accent)

    rounded(d, (520, 60, 1120, 460), 28, CARD_COLOR)
    d.text((560, 90), "TRADE CLOSED", font=font(32), fill=GOLD)

    rows = [
        ("Pool Before", format_pool(data["pool_before"])),
        ("Pool After", format_pool(data["pool_after"])),
        ("Participants", str(data["participants"])),
    ]

    y = 160
    for k, v in rows:
        d.text((560, y), k, font=font(20), fill=GRAY)
        d.text((860, y), v, font=font(22), fill=WHITE)
        y += 50

    paste_logo_and_brand(img, d)
    paste_qr(img, data["qr"])

    img.save(filename)
    return filename
