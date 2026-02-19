import json
from .client import BinanceFuturesClient
import logging

logger = logging.getLogger("trading_bot.orders")

class OrderManager:
    def __init__(self):
        self.client = BinanceFuturesClient(testnet=True)

    def execute_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            # Pass stop_price to client if it's there
            print(f"Executing order: {symbol} {side} {order_type} Qty={quantity} Price={price} Stop={stop_price}")
            response = self.client.place_order(symbol, side, order_type, quantity, price=price, stop_price=stop_price)
            if response:
                self._print_order_summary(response)
            return response
        except Exception as e:
            logger.error(f"Order execution failed: {e}")
            print(f"❌ Order failed: {e}")
            return None

    def _print_order_summary(self, response):
        """
        Prints a user-friendly summary of the order response.
        """
        print("\n✅ Order Placed Successfully!")
        print("-" * 30)
        print(f"Order ID:      {response.get('orderId')}")
        print(f"Symbol:        {response.get('symbol')}")
        print(f"Side:          {response.get('side')}")
        print(f"Type:          {response.get('type')}")
        print(f"Status:        {response.get('status')}")
        print(f"Orig Qty:      {response.get('origQty')}")
        print(f"Executed Qty:  {response.get('executedQty')}")
        print(f"Avg Price:     {response.get('avgPrice')}")
        print("-" * 30)
