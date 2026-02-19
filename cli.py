import click
import sys
import os

# Ensure the current directory is in the python path to import bot modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.logging_config import setup_logging
from bot.orders import OrderManager
from bot.validators import validate_positive_float, validate_symbol, validate_side, validate_order_type

# Initialize logging
logger = setup_logging()

@click.command()
@click.option('--symbol', prompt='Symbol (e.g., BTCUSDT)', callback=validate_symbol, help='Trading pair symbol.')
@click.option('--side', prompt='Side (BUY/SELL)', callback=validate_side, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Order side.')
@click.option('--type', 'order_type', prompt='Type (MARKET/LIMIT/STOP_MARKET)', callback=validate_order_type, type=click.Choice(['MARKET', 'LIMIT', 'STOP_MARKET'], case_sensitive=False), help='Order type.')
@click.option('--quantity', prompt='Quantity', callback=validate_positive_float, type=float, help='Order quantity.')
@click.option('--price', callback=validate_positive_float, type=float, required=False, help='Order price (required for LIMIT orders).')
@click.option('--stop-price', 'stop_price', callback=validate_positive_float, type=float, required=False, help='Stop price (required for STOP_MARKET orders).')
def main(symbol, side, order_type, quantity, price, stop_price):
    """
    Simple CLI for placing orders on Binance Futures Testnet.
    """
    logger.info(f"CLI Command received: {symbol} {side} {order_type} {quantity} {price} {stop_price}")

    if order_type == 'LIMIT' and price is None:
        price = click.prompt("Price", type=float, value_proc=lambda x: validate_positive_float(None, None, float(x)))
    
    if order_type == 'STOP_MARKET' and stop_price is None:
        stop_price = click.prompt("Stop Price", type=float, value_proc=lambda x: validate_positive_float(None, None, float(x)))

    manager = OrderManager()
    manager.execute_order(symbol, side, order_type, quantity, price, stop_price)

if __name__ == '__main__':
    main()
