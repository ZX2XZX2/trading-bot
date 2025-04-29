#!/usr/bin/env python3

import argparse
from trading_bot.connection import safe_connect, disconnect
from trading_bot.orders import cancel_order
from trading_bot.utils import get_logger

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description="Cancel an existing order by order ID.")
    parser.add_argument(
        "--order-id",
        type=int,
        required=True,
        help="Order ID to cancel"
    )
    args = parser.parse_args()

    ib = safe_connect()

    cancel_order(ib, args.order_id)

    disconnect(ib)

if __name__ == "__main__":
    main()
