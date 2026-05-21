import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from bot.logging_config import setup_logging
from bot.validators import validate_order_inputs
from bot.client import get_client
from bot.orders import place_market_order, place_limit_order

console = Console()

def print_success(message: str, response: dict = None):
    text = Text(message, style="bold green")
    if response:
        text.append("\n\nOrder Details:\n", style="white")
        keys_to_display = {
            'orderId': 'Order ID',
            'symbol': 'Symbol',
            'side': 'Side',
            'type': 'Type',
            'origQty': 'Quantity',
            'status': 'Status',
            'price': 'Price'
        }
        for key, label in keys_to_display.items():
            if key in response:
                val = response[key]
                if key == 'price' and float(val) == 0:
                    continue
                text.append(f"{label}: ", style="bold cyan")
                text.append(f"{val}\n", style="white")
            
    console.print(Panel(text, title="Success", border_style="green"))

def print_error(message: str):
    console.print(Panel(Text(message, style="bold red"), title="Error", border_style="red"))

def main():
    parser = argparse.ArgumentParser(description='Binance Futures Testnet Trading Bot CLI')
    parser.add_argument('--symbol', required=True, help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT'], help='Order type (MARKET or LIMIT)')
    parser.add_argument('--quantity', required=True, type=float, help='Quantity to trade')
    parser.add_argument('--price', type=float, help='Price (required for LIMIT orders)')
    
    args = parser.parse_args()
    
    setup_logging()
    
    try:
        # Validate inputs
        symbol, side, order_type, quantity, price = validate_order_inputs(
            args.symbol, args.side, args.type, args.quantity, args.price
        )
        
        console.print(f"[bold blue]Initializing client...[/bold blue]")
        client = get_client()
        
        if order_type == 'MARKET':
            response = place_market_order(client, symbol, side, quantity)
            print_success(f"Successfully placed MARKET order for {quantity} {symbol}", response)
        elif order_type == 'LIMIT':
            response = place_limit_order(client, symbol, side, quantity, price)
            print_success(f"Successfully placed LIMIT order for {quantity} {symbol} at {price}", response)
            
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
