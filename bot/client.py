import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("trading_bot.client")

class BinanceFuturesClient:
    def __init__(self, testnet=True, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.testnet = testnet
        
        if not self.api_key or not self.api_secret:
            # Allow initialization without keys for UI setup, but log warning
            logger.warning("API credentials not found. Please set them via UI or .env.")
            self.client = None
            return

        logger.info(f"Initializing Binance Client (Testnet={testnet})")
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=testnet)

            # Ping to verify connection
            self.client.ping()
            logger.info("Successfully connected to Binance.")
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception during init: {e}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance Request Exception during init: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during init: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Places an order on Binance Futures.
        """
        if not self.client:
             raise ValueError("Client not initialized. Please set API keys.")

        logger.info(f"Placing order: Symbol={symbol}, Side={side}, Type={order_type}, Qty={quantity}, Price={price}")
        
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }

            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders.")
                params['price'] = price
                params['timeInForce'] = 'GTC'  # Good Till Cancelled

            # Execute order
            response = self.client.futures_create_order(**params)
            
            logger.info(f"Order placed successfully: {response}")
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: Code={e.code}, Message={e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            raise
