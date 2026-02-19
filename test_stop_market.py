import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret, testnet=True)

try:
    print("Testing STOP_MARKET order...")
    # Get current price to set a reasonable stop price
    ticker = client.futures_symbol_ticker(symbol="BTCUSDT")
    price = float(ticker['price'])
    stop_price = price * 1.01 # 1% above current price for a BUY STOP (Stop Loss / Take Profit) or entry?
    # If side is BUY, stop price above market = STOP BUY (trigger entry)
    # If side is SELL, stop price below market = STOP SELL (trigger entry)
    
    # Let's try a STOP LOSS for a Long position? No, STOP_MARKET can be used to open or close.
    # Let's try opening a LONG position with a STOP MARKET buy (Stop Entry)
    print(f"Current Price: {price}, Setting Stop Price: {stop_price}")
    
    order = client.futures_create_order(
        symbol='BTCUSDT',
        side='BUY',
        type='STOP_MARKET',
        quantity=0.002,
        stopPrice=stop_price
    )
    print("Order placed successfully:", order)

except BinanceAPIException as e:
    print(f"Binance API Error: Code={e.code}, Message={e.message}")
except Exception as e:
    print(f"Error: {e}")
