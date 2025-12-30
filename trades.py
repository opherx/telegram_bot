import random
from database import get_user, update_balance

def simulate_trade(user_id):
    user = get_user(user_id)
    if not user:
        return None
    pnl = random.uniform(-5, 10)
    new_balance = user[3] + pnl  # balance column
    update_balance(user_id, new_balance)
    return pnl, new_balance
