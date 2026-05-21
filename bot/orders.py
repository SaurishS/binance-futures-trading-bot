import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

def place_market_order(client: Client, symbol: str, side: str, quantity: float):
    logging.info(f"Placing MARKET {side} order for {quantity} {symbol}")
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        logging.info(f"Market order placed successfully. Order ID: {response.get('orderId')}. Full response: {response}")
        return response
    except BinanceAPIException as e:
        logging.error(f"Binance API Exception while placing market order: {e}")
        raise
    except BinanceRequestException as e:
        logging.error(f"Network error while placing market order: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error placing market order: {e}")
        raise

def place_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float):
    logging.info(f"Placing LIMIT {side} order for {quantity} {symbol} at {price}")
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )
        logging.info(f"Limit order placed successfully. Order ID: {response.get('orderId')}. Full response: {response}")
        return response
    except BinanceAPIException as e:
        logging.error(f"Binance API Exception while placing limit order: {e}")
        raise
    except BinanceRequestException as e:
        logging.error(f"Network error while placing limit order: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error placing limit order: {e}")
        raise
