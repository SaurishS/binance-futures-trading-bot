# Binance Futures Testnet Trading Bot

A robust, production-ready Command Line Interface (CLI) application for placing algorithmic orders on the Binance Futures Testnet. Built with Python, this tool demonstrates clean architecture, input validation, and comprehensive error handling.

## Features
- **Market & Limit Orders**: Place `BUY` and `SELL` orders seamlessly.
- **Input Validation**: Ensures safe operations (e.g., verifying price is provided for limit orders, quantity > 0).
- **Error Handling**: Gracefully handles network issues, API exceptions, and invalid user inputs.
- **Comprehensive Logging**: Silent console output for user experience, with full detailed logs preserved in `logs/trading_bot.log`.
- **Rich CLI**: Beautifully formatted terminal outputs using the `rich` library.

## Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance API client initialization
│   ├── logging_config.py # Centralized logging configuration
│   ├── orders.py         # Core order execution logic
│   └── validators.py     # Strict input validation logic
├── logs/                 # Auto-generated directory for log files
├── .env.example          # Template for environment variables
├── cli.py                # Main CLI entry point
├── README.md             
└── requirements.txt      # Project dependencies
```

## Setup Instructions

1. **Clone the Repository**
   Ensure you are in the `trading_bot` directory.

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Copy the provided `.env.example` file to create your local `.env` configuration:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and replace the placeholder values with your actual API credentials. You can generate these at the [Binance Futures Testnet](https://testnet.binancefuture.com/).

## Usage

Interact with the bot using the CLI provided in `cli.py`. The application will output only essential details to the console while logging the full API response internally.

### Example Commands

**1. Place a MARKET Order**
Market orders execute immediately at the best available price.
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**2. Place a LIMIT Order**
Limit orders require a target `--price`.
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

### Command Arguments Reference
- `--symbol`: Trading pair symbol (e.g., BTCUSDT)
- `--side`: Order direction (`BUY` or `SELL`)
- `--type`: Order type (`MARKET` or `LIMIT`)
- `--quantity`: Asset quantity to trade (must be > 0)
- `--price`: Target price (strictly required for `LIMIT` orders)

## Logging & Validation
- **Logging**: All API requests, responses, and errors are securely logged to `logs/trading_bot.log`. The terminal only displays essential information to keep the user experience clean. The repository includes a sample `trading_bot.log` file demonstrating successful MARKET and LIMIT order executions, rigorous validation handling, and graceful Binance API exception management.
- **Validation**: Inputs are rigorously checked prior to making any API requests to prevent unnecessary network calls and handle edge cases locally.
