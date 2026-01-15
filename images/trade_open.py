from PIL import Image, ImageDraw
from images.generator import *
from utils.formatters import format_pool

W, H = 1200, 600


def generate_trade_open(data, filename="trade_open.png"):
    img = Image.new("RGB", (W, H), BG_COLOR)
    d = ImageDraw.Draw(img)

    direction = data["direction"]
    dir_color = GREEN if direction == "LONG" else RED

    d.text((60, 60), data["pair"], font=font(52), fill=GOLD)
    d.text((60, 130), f"${data['entry']:,.2f}", font=font(36), fill=WHITE)

    rounded(d, (60, 210, 180, 250), 18, dir_color)
    d.text((75, 218), direction, font=font(20), fill="white")

    rounded(d, (190, 210, 260, 250), 18, GOLD)
    d.text((205, 218), f"{data['leverage']}x", font=font(20), fill="black")

    rounded(d, (520, 60, 1120, 460), 28, CARD_COLOR)
    d.text((560, 90), "NEW POSITION", font=font(32), fill=GOLD)

    rows = [
        ("Pool Size", format_pool(data["pool"])),
        ("Participants", str(data["participants"])),
    ]

    y = 160
    for k, v in rows:
        d.text((560, y), k, font=font(20), fill=GRAY)
        d.text((860, y), v, font=font(22), fill=WHITE)
        y += 50

    paste_logo_and_brand(img, d)
    paste_qr(img, data.get("qr", ""))

    img.save(filename)
    return filename
