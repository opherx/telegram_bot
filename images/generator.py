from PIL import Image, ImageDraw, ImageFont
import os, qrcode

FONT_PATH = "assets/fonts/DejaVuSans-Bold.ttf"
LOGO_PATH = "assets/logo.png"

BG_COLOR = "#0f1115"
CARD_COLOR = "#151a22"
GOLD = "#f5c26b"
GRAY = "#9ca3af"
WHITE = "#e5e7eb"
GREEN = "#22c55e"
RED = "#ef4444"


def font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def rounded(draw, xy, radius, fill):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def paste_logo_and_brand(img, draw):
    footer_y = img.height - 100
    rounded(draw, (0, footer_y, img.width, img.height), 0, "#d1d5db")

    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA").resize((70, 70))
        img.paste(logo, (40, footer_y + 15), logo)

    draw.text(
        (130, footer_y + 35),
        "CASHIFY AI BOT",
        font=font(28),
        fill="#111827"
    )


def paste_qr(img, data: str):
    qr = qrcode.make(data).resize((80, 80))
    img.paste(qr, (img.width - 120, img.height - 90))
