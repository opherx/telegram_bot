from PIL import Image, ImageDraw, ImageFont
import os
import qrcode

FONT_PATH = "assets/fonts/DejaVuSans-Bold.ttf"
LOGO_PATH = "assets/logo.png"


def load_font(size):
    try:
        if os.path.exists(FONT_PATH):
            return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        pass
    return ImageFont.load_default()


def paste_logo(img):
    """Safely paste logo bottom-left"""
    if not os.path.exists(LOGO_PATH):
        return

    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo = logo.resize((110, 110))
        img.paste(logo, (40, img.height - 150), logo)
    except Exception as e:
        print("Logo error:", e)


def paste_qr(img, data: str):
    """Generate and paste QR bottom-right"""
    try:
        qr = qrcode.make(data)
        qr = qr.resize((130, 130))
        img.paste(qr, (img.width - 170, img.height - 170))
    except Exception as e:
        print("QR error:", e)


def base_card(title: str, qr_data: str | None = None):
    img = Image.new("RGB", (1100, 550), "#0b0f14")
    draw = ImageDraw.Draw(img)

    draw.text((40, 30), title, font=load_font(42), fill="#22c55e")

    paste_logo(img)

    if qr_data:
        paste_qr(img, qr_data)

    return img, draw
