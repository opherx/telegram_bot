# database.py

# This is a simple in-memory DB simulation.
# Replace with real DB code if you want persistent storage.
USERS = []

def get_db():
    """Returns the simulated database"""
    return USERS

def get_all_users():
    """Return all registered users"""
    return USERS

def get_user(tg_id):
    """Find a user by Telegram ID"""
    for user in USERS:
        if user["telegram_id"] == tg_id:
            return user
    return None

def add_user(tg_id, username):
    """Add a new user"""
    user = {
        "telegram_id": tg_id,
        "username": username,
        "balance": 0.0
    }
    USERS.append(user)
    return user

def update_balance(tg_id, amount):
    """Update user's balance by adding the amount"""
    user = get_user(tg_id)
    if user:
        user["balance"] += amount
        return True
    return False

def set_balance(tg_id, amount):
    """Set user's balance to a specific value"""
    user = get_user(tg_id)
    if user:
        user["balance"] = amount
        return True
    return False
