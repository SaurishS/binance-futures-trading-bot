import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, FloatPrompt
from bot.logging_config import setup_logging
from bot.validators import validate_order_inputs
from bot.client import get_client
from bot.orders import place_market_order, place_limit_order

console = Console()

def print_banner():
    banner = Text(" Binance Futures Trading Bot ", style="bold black on yellow", justify="center")
    console.print(Panel(banner, border_style="yellow"))

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

def interactive_mode():
    console.print("[cyan]Entering interactive mode...[/cyan]\n")
    symbol = Prompt.ask("Trading pair symbol (e.g., BTCUSDT)", default="BTCUSDT")
    side = Prompt.ask("Order side", choices=["BUY", "SELL"], default="BUY")
    order_type = Prompt.ask("Order type", choices=["MARKET", "LIMIT"], default="MARKET")
    quantity = FloatPrompt.ask("Quantity to trade")
    
    price = None
    if order_type == "LIMIT":
        price = FloatPrompt.ask("Target price")
        
    return symbol, side, order_type, quantity, price

def main():
    parser = argparse.ArgumentParser(
        description='A professional CLI for placing algorithmic orders on the Binance Futures Testnet.',
        epilog='Examples:\n  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001\n  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 3500.0\n  python cli.py (Runs in interactive mode without arguments)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser.add_argument('--type', choices=['MARKET', 'LIMIT'], help='Order type (MARKET or LIMIT)')
    parser.add_argument('--quantity', type=float, help='Quantity to trade (must be > 0)')
    parser.add_argument('--price', type=float, help='Target price (strictly required for LIMIT orders)')
    
    args = parser.parse_args()
    
    print_banner()
    setup_logging()
    
    # Trigger interactive mode if no arguments are provided
    if len(sys.argv) == 1:
        try:
            symbol, side, order_type, quantity, price = interactive_mode()
        except KeyboardInterrupt:
            console.print("\n[red]Operation cancelled by user.[/red]")
            sys.exit(0)
    else:
        # Check required fields for CLI mode
        if not args.symbol or not args.side or not args.type or not args.quantity:
            print_error("Missing required arguments. Please provide --symbol, --side, --type, and --quantity, or run without arguments for interactive mode.")
            sys.exit(1)
            
        symbol = args.symbol
        side = args.side
        order_type = args.type
        quantity = args.quantity
        price = args.price
    
    try:
        # Validate inputs before network call
        symbol, side, order_type, quantity, price = validate_order_inputs(
            symbol, side, order_type, quantity, price
        )
        
        console.print(f"[bold blue]Initializing Binance client...[/bold blue]")
        client = get_client()
        
        if order_type == 'MARKET':
            response = place_market_order(client, symbol, side, quantity)
            print_success(f"Successfully placed MARKET {side} order for {quantity} {symbol}", response)
        elif order_type == 'LIMIT':
            response = place_limit_order(client, symbol, side, quantity, price)
            print_success(f"Successfully placed LIMIT {side} order for {quantity} {symbol} at {price}", response)
            
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
