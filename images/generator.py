from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

FONT = "assets/fonts/DejaVuSans-Bold.ttf"

def generate_card(title, lines, filename):
    img = Image.new("RGB", (900, 450), "#020617")
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype(FONT, 36)
    text_font = ImageFont.truetype(FONT, 24)

    draw.text((40, 30), title, font=title_font, fill="#22c55e")

    y = 100
    for line in lines:
        draw.text((40, y), line, font=text_font, fill="#e5e7eb")
        y += 36

    draw.text((40, 390),
              datetime.utcnow().strftime("UTC %Y-%m-%d %H:%M"),
              font=text_font, fill="#94a3b8")

    img.save(filename)
    return filename
