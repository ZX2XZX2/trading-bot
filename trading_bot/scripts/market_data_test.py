import argparse
from trading_bot.connection import safe_connect, disconnect
from trading_bot.contracts import get_stock
from trading_bot.market_data import request_market_data

def main():
    parser = argparse.ArgumentParser(description="Fetch market data for multiple stock symbols.")
    parser.add_argument(
        "--symbols",
        type=str,
        nargs="+",
        required=True,
        help="List of stock symbols to fetch (e.g., --symbols AAPL MSFT TSLA)"
    )
    args = parser.parse_args()

    ib = safe_connect()

    for symbol in args.symbols:
        symbol = symbol.upper()
        stock = get_stock(symbol)
        ticker = request_market_data(ib, stock)
        print(f"{symbol}: Bid={ticker.bid}, Ask={ticker.ask}, Last={ticker.last}")

    disconnect(ib)

if __name__ == "__main__":
    main()
