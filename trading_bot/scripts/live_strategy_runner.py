#!/usr/bin/env python3

import argparse
from trading_bot.session import TradingSession
from strategy_lab.strategies import discover_strategies

def list_available_strategies():
    strategies = discover_strategies()
    print("Available strategies:")
    for name in strategies:
        print(f"  - {name}")

def main():
    parser = argparse.ArgumentParser(
        description="Run a live trading strategy via the TradingSession plugin system."
    )
    parser.add_argument(
        "--strategy", type=str, help="Strategy name (e.g., trailing_stop, basic_buy)"
    )
    parser.add_argument(
        "--symbol", type=str, help="Stock symbol to trade (e.g., AAPL)"
    )
    parser.add_argument("--quantity", type=int, default=1)
    parser.add_argument("--trail", type=float, help="Trailing amount for stop-loss")
    parser.add_argument("--duration", type=int, default=300)
    parser.add_argument("--list", action="store_true", help="List all available strategies and exit")

    args = parser.parse_args()

    if args.list:
        list_available_strategies()
        return

    if not args.strategy or not args.symbol:
        parser.error("--strategy and --symbol are required unless --list is used.")

    session = TradingSession()
    session.run_strategy_by_name(
        strategy_name=args.strategy,
        symbol=args.symbol.upper(),
        quantity=args.quantity,
        trail=args.trail,
        duration=args.duration,
    )
    session.stop()

if __name__ == "__main__":
    main()
