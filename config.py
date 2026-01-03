import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

MIN_DEPOSIT = 20.0
REFERRAL_RATE = 0.06
MIN_POOL_FOR_TRADING = 100_000
DEFAULT_POOL_BALANCE = 150_000

FAKE_WALLETS = {
    "BTC": "bc1qdemobtcaddress",
    "ETH": "0xdemoethaddress",
    "BNB": "bnb1demobnbaddress",
    "SOL": "SoLDeMoAddress"
}
