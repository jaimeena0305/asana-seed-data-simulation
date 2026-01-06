import uuid
import random
import datetime
import sqlite3
from src.config import DB_PATH, SCHEMA_PATH

def init_db():
    """Initializes the SQLite database with the schema."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    return conn

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def generate_uuid():
    return str(uuid.uuid4())

def random_date(start_date, end_date, work_days_only=True):
    """Generates a random datetime between two dates."""
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    res = start_date + datetime.timedelta(seconds=random_second)
    
    # Simple heuristic: if it's weekend and we want workdays, shift to Monday
    if work_days_only and res.weekday() >= 5: # 5=Sat, 6=Sun
        res += datetime.timedelta(days=(7 - res.weekday()))
    
    return res

def weighted_choice(choices, weights):
    """Selects an item based on weights."""
    return random.choices(choices, weights=weights, k=1)[0]

import os