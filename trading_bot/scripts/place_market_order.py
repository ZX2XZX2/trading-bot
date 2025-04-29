#!/usr/bin/env python3

import argparse
from trading_bot.connection import safe_connect, disconnect
from trading_bot.orders import submit_market_order
from trading_bot.utils import get_logger

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description="Submit a market order through IB paper account.")
    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Stock symbol to trade (e.g., AAPL)"
    )
    parser.add_argument(
        "--quantity",
        type=int,
        default=1,
        help="Number of shares (default: 1)"
    )
    parser.add_argument(
        "--action",
        type=str,
        choices=["BUY", "SELL"],
        default="BUY",
        help="Action to perform: BUY or SELL (default: BUY)"
    )
    args = parser.parse_args()

    ib = safe_connect()

    logger.info(f"Placing {args.action} order for {args.quantity} shares of {args.symbol.upper()}...")
    submit_market_order(ib, args.symbol.upper(), quantity=args.quantity, action=args.action)

    disconnect(ib)

if __name__ == "__main__":
    main()
