from PIL import Image, ImageDraw, ImageFont
import os
import qrcode

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


def paste_logo(img):
    if not os.path.exists(LOGO_PATH):
        return
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA").resize((90, 90))
        img.paste(logo, (40, img.height - 130), logo)
    except Exception as e:
        print("Logo error:", e)


def paste_qr(img, data: str):
    try:
        qr = qrcode.make(data).resize((90, 90))
        img.paste(qr, (img.width - 130, img.height - 130))
    except Exception as e:
        print("QR error:", e)


def rounded(draw, xy, radius, fill):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)
