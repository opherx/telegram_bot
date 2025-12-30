from PIL import Image, ImageDraw, ImageFont
import random

def generate_trade_screenshot(pnl, balance, filename="trade.png"):
    img = Image.new("RGB", (600, 300), color=(24, 24, 24))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    d.text((20, 20), f"Trade Result: ${pnl:.2f}", fill=(0, 255, 0) if pnl>0 else (255,0,0), font=font)
    d.text((20, 50), f"Balance: ${balance:.2f}", fill=(255,255,255), font=font)

    img.save(filename)
    return filename
