#!/usr/bin/env python3

from trading_bot.connection import safe_connect, disconnect
from trading_bot.orders import list_open_orders
from trading_bot.utils import get_logger

logger = get_logger()

def main():
    ib = safe_connect()

    list_open_orders(ib)

    disconnect(ib)

if __name__ == "__main__":
    main()
