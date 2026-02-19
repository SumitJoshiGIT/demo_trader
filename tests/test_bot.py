import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.validators import validate_symbol, validate_side, validate_order_type, validate_positive_float
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
import click

class TestValidators(unittest.TestCase):
    def test_validate_symbol(self):
        self.assertEqual(validate_symbol(None, None, "btcusdt"), "BTCUSDT")
        with self.assertRaises(click.BadParameter):
            validate_symbol(None, None, "BTC-USDT")

    def test_validate_side(self):
        self.assertEqual(validate_side(None, None, "buy"), "BUY")
        self.assertEqual(validate_side(None, None, "SELL"), "SELL")
        with self.assertRaises(click.BadParameter):
            validate_side(None, None, "HOLD")

    def test_validate_order_type(self):
        self.assertEqual(validate_order_type(None, None, "market"), "MARKET")
        self.assertEqual(validate_order_type(None, None, "limit"), "LIMIT")
        with self.assertRaises(click.BadParameter):
            validate_order_type(None, None, "STOP_LOSS")

    def test_validate_positive_float(self):
        mock_param = MagicMock()
        mock_param.name = "quantity"
        self.assertEqual(validate_positive_float(None, mock_param, 10.5), 10.5)
        with self.assertRaises(click.BadParameter):
            validate_positive_float(None, mock_param, -5)
        with self.assertRaises(click.BadParameter):
            validate_positive_float(None, mock_param, 0)

class TestBinanceClient(unittest.TestCase):
    @patch('bot.client.Client')
    @patch.dict(os.environ, {'BINANCE_API_KEY': 'test_key', 'BINANCE_API_SECRET': 'test_secret'})
    def test_client_init(self, MockClient):
        client = BinanceFuturesClient(testnet=True)
        MockClient.assert_called_with('test_key', 'test_secret', testnet=True)
        self.assertIsNotNone(client.client)

    @patch('bot.client.Client')
    def test_place_order_market(self, MockClient):
        # Setup mock
        mock_instance = MockClient.return_value
        mock_instance.futures_create_order.return_value = {
            'orderId': 12345,
            'status': 'FILLED',
            'symbol': 'BTCUSDT'
        }

        client = BinanceFuturesClient(testnet=True, api_key="k", api_secret="s")
        response = client.place_order(symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=0.001)
        
        mock_instance.futures_create_order.assert_called_with(
            symbol='BTCUSDT',
            side='BUY',
            type='MARKET',
            quantity=0.001
        )
        self.assertEqual(response['orderId'], 12345)

    @patch('bot.client.Client')
    def test_place_order_limit(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.futures_create_order.return_value = {'orderId': 67890}

        client = BinanceFuturesClient(testnet=True, api_key="k", api_secret="s")
        response = client.place_order(symbol="ETHUSDT", side="SELL", order_type="LIMIT", quantity=1.5, price=2000)
        
        mock_instance.futures_create_order.assert_called_with(
            symbol='ETHUSDT',
            side='SELL',
            type='LIMIT',
            quantity=1.5,
            price=2000,
            timeInForce='GTC'
        )

    def test_place_limit_order_without_price_raises_error(self):
        client = BinanceFuturesClient(testnet=True, api_key="k", api_secret="s")
        # We don't need to mock the internal client call here as it should fail before matching
        # But to be safe in case it passes checking, let's mock it
        client.client = MagicMock()
        
        with self.assertRaises(ValueError):
            client.place_order(symbol="BTCUSDT", side="BUY", order_type="LIMIT", quantity=0.01)

class TestOrderManager(unittest.TestCase):
    @patch('bot.client.BinanceFuturesClient')
    def test_execute_order_success(self, MockClient):
        mock_client_instance = MockClient.return_value
        mock_client_instance.place_order.return_value = {
            'orderId': 111, 'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET',
            'status': 'NEW', 'origQty': '0.1', 'executedQty': '0.0', 'avgPrice': '0.0'
        }

        manager = OrderManager()
        # Inject the mock client
        manager.client = mock_client_instance

        response = manager.execute_order("BTCUSDT", "BUY", "MARKET", 0.1)
        
        self.assertEqual(response['orderId'], 111)
        mock_client_instance.place_order.assert_called_once()

    @patch('bot.client.BinanceFuturesClient')
    def test_execute_order_failure(self, MockClient):
         mock_client_instance = MockClient.return_value
         mock_client_instance.place_order.side_effect = Exception("API Error")

         manager = OrderManager()
         manager.client = mock_client_instance
         
         # Should catch exception and return None
         response = manager.execute_order("BTCUSDT", "BUY", "MARKET", 0.1)
         self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
