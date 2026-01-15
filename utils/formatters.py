def format_pool(value: float) -> str:
    try:
        value = float(value)
    except Exception:
        return "0 USDT"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M USDT"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K USDT"
    return f"{value:,.2f} USDT"
