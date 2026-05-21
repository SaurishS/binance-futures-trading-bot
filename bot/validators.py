def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Invalid symbol. Please provide a valid trading pair (e.g., 'BTCUSDT').")
    return symbol.upper()

def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid order side: '{side}'. Accepted values are 'BUY' or 'SELL'.")
    return side

def validate_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValueError(f"Invalid order type: '{order_type}'. Accepted values are 'MARKET' or 'LIMIT'.")
    return order_type

def validate_quantity(quantity: float) -> float:
    try:
        qty = float(quantity)
    except ValueError:
        raise ValueError("Invalid quantity. The quantity must be a valid number.")
    if qty <= 0:
        raise ValueError("Invalid quantity. The quantity must be strictly greater than 0.")
    return qty

def validate_price(order_type: str, price: float = None) -> float:
    if order_type.upper() == 'LIMIT':
        if price is None:
            raise ValueError("Missing price. A target price is strictly required for LIMIT orders.")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Invalid price. The price must be strictly greater than 0.")
            return p
        except ValueError:
            raise ValueError("Invalid price. The price must be a valid number.")
    return None

def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(order_type, price)
    return symbol, side, order_type, quantity, price
