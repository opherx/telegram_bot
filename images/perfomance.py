from PIL import Image, ImageDraw, ImageFont
from database import cur, get_pool_balance

FONT = "assets/fonts/DejaVuSans-Bold.ttf"

def generate_performance_card(filename="performance.png"):
    pool = cur.execute(
        "SELECT total_traded, total_profit, total_distributed, wins, losses FROM pool WHERE id=1"
    ).fetchone()

    users = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    pool_balance = get_pool_balance()

    total_traded, total_profit, total_dist, wins, losses = pool
    trades = wins + losses
    win_rate = (wins / trades * 100) if trades else 0

    img = Image.new("RGB", (900, 550), "#020617")
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT, 40)
    text_font = ImageFont.truetype(FONT, 26)

    draw.text((40, 30), "AI TRADING PERFORMANCE", font=title_font, fill="#22c55e")

    y = 110
    lines = [
        f"Investors: {users}",
        f"Total Trades: {trades}",
        f"Win Rate: {win_rate:.1f}%",
        "",
        f"Total Pool Traded: {total_traded:,.2f} USDT",
        f"Total Profit Generated: +{total_profit:,.2f} USDT",
        f"Profit Distributed: {total_dist:,.2f} USDT",
        "",
        f"Current Pool Balance: {pool_balance:,.2f} USDT"
    ]

    for line in lines:
        draw.text((40, y), line, font=text_font, fill="#e5e7eb")
        y += 40

    img.save(filename)
    return filename
