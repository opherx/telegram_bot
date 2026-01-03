from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = "assets/fonts/DejaVuSans-Bold.ttf"

def load_font(size):
    try:
        if os.path.exists(FONT_PATH):
            return ImageFont.truetype(FONT_PATH, size)
    except:
        pass
    return ImageFont.load_default()

def base_card(title):
    img = Image.new("RGB", (1100, 550), "#0b0f14")
    draw = ImageDraw.Draw(img)
    draw.text((40, 30), title, font=load_font(42), fill="#22c55e")
    return img, draw
