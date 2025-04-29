#!/usr/bin/env python3

import argparse
from trading_bot.connection import safe_connect, disconnect
from trading_bot.orders import move_stop_order
from trading_bot.utils import get_logger

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description="Modify the stop price for an existing STOP order.")
    parser.add_argument(
        "--order-id",
        type=int,
        required=True,
        help="Order ID of the existing stop order"
    )
    parser.add_argument(
        "--new-stop-price",
        type=float,
        required=True,
        help="New stop price"
    )
    args = parser.parse_args()

    ib = safe_connect()

    move_stop_order(ib, args.order_id, args.new_stop_price)

    disconnect(ib)

if __name__ == "__main__":
    main()
