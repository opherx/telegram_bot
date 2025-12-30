import random
from database import update_balance
from telegram.ext import ContextTypes

PAIRS = ["EUR/USD", "GBP/USD", "BTC/USDT", "ETH/USDT"]

async def send_trade(context: ContextTypes.DEFAULT_TYPE):
    pair = random.choice(PAIRS)
    result = random.choice(["WIN
