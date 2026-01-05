from PIL import Image, ImageDraw
from images.generator import (
    font,
    rounded,
    paste_logo,
    paste_qr,
    BG_COLOR,
    CARD_COLOR,
    GOLD,
    GRAY,
    WHITE,
    GREEN,
    RED,
)

W, H = 1200, 600


def _to_float(value, default=0.0):
    """
    Safely convert value to float.
    Accepts int, float, or numeric string.
    """
    try:
        return float(value)
    except Exception:
        return default


def generate_trade_close(data, filename="trade_close.png"):
    """
    data keys expected:
      pair, entry, exit, pnl, win,
      pool_before, pool_after,
      leverage, participants, trade_no, qr
    """

    img = Image.new("RGB", (W, H), BG_COLOR)
    d = ImageDraw.Draw(img)

    # ---------- NORMALIZE DATA (NO CRASH ZONE) ----------
    is_win = bool(data.get("win", False))

    entry = _to_float(data.get("entry"))
    exit_price = _to_float(data.get("exit"))
    pnl_value = _to_float(data.get("pnl"))
    pool_before = _to_float(data.get("pool_before"))
    pool_after = _to_float(data.get("pool_after"))

    pair = data.get("pair", "N/A")
    leverage = data.get("leverage", "-")
    participants = data.get("participants", "-")
    trade_no = data.get("trade_no", "-")
    qr_data = data.get("qr", "")

    accent = GREEN if is_win else RED
    title = "POSITION CLOSED - PROFIT" if is_win else "POSITION CLOSED - LOSS"

    # ---------- LEFT PANEL ----------
    d.text((60, 60), pair, font=font(52), fill=GOLD)
    d.text((60, 130), f"${exit_price:,.2f}", font=font(36), fill=WHITE)
    d.text((60, 180), title, font=font(20), fill=accent)

    # PNL pill
    rounded(d, (60, 220, 260, 260), 18, accent)
    sign = "+" if is_win else ""
    pnl_text = f"{sign}{pnl_value:,.2f} USDT"
    d.text((80, 228), pnl_text, font=font(20), fill="white")

    # ---------- RIGHT CARD ----------
    card_x = 520
    rounded(d, (card_x, 60, 1120, 460), 28, CARD_COLOR)

    d.text((card_x + 40, 90), "TRADE SUMMARY", font=font(32), fill=GOLD)

    rows = [
        ("Entry Price", f"${entry:,.2f}"),
        ("Exit Price", f"${exit_price:,.2f}"),
        ("Pool Before", f"{pool_before:,.2f} USDT"),
        ("Pool After", f"{pool_after:,.2f} USDT"),
        ("Leverage", f"{leverage}x"),
        ("Participants", str(participants)),
        ("Trade #", str(trade_no)),
    ]

    y = 150
    for label, value in rows:
        d.text((card_x + 40, y), label, font=font(20), fill=GRAY)
        d.text((card_x + 360, y), value, font=font(22), fill=WHITE)
        y += 45

    # ---------- BRAND BAR ----------
    rounded(d, (0, 500, W, H), 0, "#d1d5db")
    paste_logo(img)
    paste_qr(img, qr_data)

    img.save(filename)
    return filename
