import sqlite3
import json
import os
from datetime import datetime

# Use a data directory for persistence if it exists (good for Docker)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
if os.path.exists(DATA_DIR):
    DB_FILE = os.path.join(DATA_DIR, 'trading_bot.db')
else:
    DB_FILE = 'trading_bot.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Create orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  symbol TEXT,
                  side TEXT,
                  type TEXT,
                  quantity REAL,
                  price REAL,
                  status TEXT,
                  order_id TEXT,
                  details TEXT)''')
    # Create settings table
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()

def log_order(order_data, response):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO orders (timestamp, symbol, side, type, quantity, price, status, order_id, details) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (datetime.now().isoformat(), 
               order_data['symbol'], 
               order_data['side'], 
               order_data['type'], 
               order_data['quantity'], 
               order_data.get('price'),
               response.get('status', 'UNKNOWN'),
               str(response.get('orderId', '')),
               json.dumps(response)))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_setting(key, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_setting(key):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
