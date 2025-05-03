#!/usr/bin/env python3

import argparse
from trading_bot.session import TradingSession

def main():
    parser = argparse.ArgumentParser(description="Run a registered trading strategy.")
    parser.add_argument("--strategy", type=str, required=True, help="Strategy name (e.g., trailing_stop)")
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--quantity", type=int, default=1)
    parser.add_argument("--trail", type=float)
    parser.add_argument("--duration", type=int, default=300)

    args = parser.parse_args()

    session = TradingSession()
    session.run_strategy_by_name(
        args.strategy,
        symbol=args.symbol.upper(),
        quantity=args.quantity,
        trail=args.trail,
        duration=args.duration
    )
    session.stop()

if __name__ == "__main__":
    main()
