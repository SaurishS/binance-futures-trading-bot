import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        logging.error("BINANCE_API_KEY or BINANCE_API_SECRET not found in environment variables.")
        raise ValueError("Missing API keys. Please check your .env file.")
    
    try:
        # Initialize client without testnet=True to avoid the Spot testnet DNS ping error
        # which sometimes happens when testnet.binance.vision is unreachable
        client = Client(api_key, api_secret, testnet=False)
        
        # Manually set the Futures URL to the testnet URL
        client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        
        # Ping to test connection to futures testnet
        client.futures_ping()
        logging.info("Successfully connected to Binance Futures Testnet.")
        return client
    except BinanceAPIException as e:
        logging.error(f"Binance API Exception: {e}")
        raise
    except BinanceRequestException as e:
        logging.error(f"Binance Request Exception: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error initializing client: {e}")
        raise
