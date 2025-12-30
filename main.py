import os
import random
import psycopg2
import bcrypt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue,
)

# --- Environment Variables ---
TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Database Connection ---
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    balance REAL DEFAULT 100.0
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    trade_id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    pnl REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# --- Helper Functions ---
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

def generate_trade_image(username: str, pnl: float, balance: float) -> BytesIO:
    # Create simple trade screenshot
    img = Image.new("RGB", (400, 200), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    
    draw.text((10, 20), f"User: {username}", fill="white", font=font)
    draw.text((10, 60), f"Trade PnL: ${pnl:.2f}", fill="white", font=font)
    draw.text((10, 100), f"Balance: ${balance:.2f}", fill="white", font=font)
    
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Demo Trading Bot\n\n"
        "Use /register <username> <password> to create an account\n"
        "Use /login <username> <password> to login"
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /register <username> <password>")
        return
    
    username, password = context.args
    password_hash = hash_password(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (user_id, username, password_hash) VALUES (%s, %s, %s)",
            (update.effective_user.id, username, password_hash)
        )
        conn.commit()
        await update.message.reply_text("✅ Registration successful! Your demo balance is $100")
    except psycopg2.errors.UniqueViolation:
        await update.message.reply_text("❌ Username already exists.")
        conn.rollback()

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /login <username> <password>")
        return

    username, password = context.args
    cursor.execute(
        "SELECT password_hash FROM users WHERE username=%s AND user_id=%s",
        (username, update.effective_user.id)
    )
    row = cursor.fetchone()
    if not row or not verify_password(password, row[0].tobytes() if hasattr(row[0], "tobytes") else row[0]):
        await update.message.reply_text("❌ Invalid username or password")
        return
    await update.message.reply_text("✅ Logged in successfully!")

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT balance FROM users WHERE user_id=%s", (update.effective_user.id,))
    row = cursor.fetchone()
    if not row:
        await update.message.reply_text("❌ You need to register first")
        return
    balance = row[0]

    cursor.execute(
        "SELECT pnl, timestamp FROM trades WHERE user_id=%s ORDER BY timestamp DESC LIMIT 5",
        (update.effective_user.id,)
    )
    trades = cursor.fetchall()
    
    text = f"💰 Balance: ${balance:.2f}\n\n📈 Last 5 trades:\n"
    for pnl, ts in trades:
        text += f"{ts}: ${pnl:.2f}\n"
    await update.message.reply_text(text)

# --- Automated Trades ---
async def auto_trade(context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT user_id, username, balance FROM users")
    users = cursor.fetchall()
    for user_id, username, balance in users:
        pnl = random.uniform(-5, 10)
        new_balance = balance + pnl

        cursor.execute(
            "UPDATE users SET balance=%s WHERE user_id=%s",
            (new_balance, user_id)
        )
        cursor.execute(
            "INSERT INTO trades (user_id, pnl) VALUES (%s, %s)",
            (user_id, pnl)
        )
        conn.commit()

        # Send trade screenshot
        image = generate_trade_image(username, pnl, new_balance)
        await context.bot.send_photo(chat_id=user_id, photo=InputFile(image))

# --- Main ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("dashboard", dashboard))

    # JobQueue for auto trades
    app.job_queue.run_repeating(auto_trade, interval=300, first=10)  # every 5 minutes

    app.run_polling()

if __name__ == "__main__":
    main()
