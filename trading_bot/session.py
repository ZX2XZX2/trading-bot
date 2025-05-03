from ib_insync import IB, Contract, Ticker
from trading_bot.connection import safe_connect, disconnect
from trading_bot.order_manager import OrderManager
from strategy_lab.strategies import discover_strategies
from trading_bot.utils import get_logger

logger = get_logger()

class TradingSession:
    def __init__(self):
        self.ib: IB = None
        self.order_manager: OrderManager = None
        self.subscribed_tickers: dict[str, Ticker] = {}

    def start(self):
        """Start the trading session: connect to IB and initialize manager."""
        logger.info("Starting trading session...")
        self.ib = safe_connect()
        self.order_manager = OrderManager(self.ib)
        logger.info("Trading session started.")

    def stop(self):
        """Stop the trading session: disconnect from IB."""
        if self.ib:
            disconnect(self.ib)
            logger.info("Trading session stopped.")
        else:
            logger.warning("Trading session was not active.")

    def subscribe_market_data(self, symbol: str) -> Ticker:
        """Subscribe to live (or delayed) market data for a stock symbol."""
        logger.info(f"Subscribing to market data for {symbol}...")
        contract = Contract(symbol=symbol, secType="STK", exchange="SMART", currency="USD")
        self.ib.reqMarketDataType(3)  # Request delayed if real-time unavailable
        ticker = self.ib.reqMktData(contract)
        self.subscribed_tickers[symbol] = ticker
        return ticker

    def get_last_price(self, symbol: str) -> float | None:
        """Get the last traded price for a subscribed symbol."""
        ticker = self.subscribed_tickers.get(symbol)
        if ticker:
            return ticker.last
        logger.warning(f"No ticker data for {symbol}.")
        return None

    def place_market_order(self, symbol: str, quantity: int = 1, action: str = "BUY"):
        """Convenience function to submit a simple market order."""
        return self.order_manager.submit_market_order(symbol, quantity, action)

    def run_strategy_by_name(self, strategy_name: str, **kwargs):
        strategies = discover_strategies()
        if strategy_name not in strategies:
            logger.error(f"Strategy '{strategy_name}' not found.")
            return

        logger.info(f"Launching strategy: {strategy_name}")
        strategy_class = strategies[strategy_name]
        strategy = strategy_class(self)
        strategy.run(**kwargs)
