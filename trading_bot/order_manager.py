from ib_insync import IB, Trade, MarketOrder, LimitOrder, StopOrder
from trading_bot.contracts import get_stock
from trading_bot.utils import get_logger

logger = get_logger()

class OrderManager:
    def __init__(self, ib: IB):
        self.ib = ib
        self.refresh_open_trades()

    def refresh_open_trades(self):
        """Refresh list of open trades."""
        self.ib.reqOpenOrders()
        self.ib.sleep(1)
        self.open_trades = self.ib.openTrades()
        logger.info(f"Refreshed open trades. {len(self.open_trades)} open trades found.")

    def list_open_orders(self):
        """List all open orders."""
        self.refresh_open_trades()
        for trade in self.open_trades:
            logger.info(
                f"Order ID: {trade.order.orderId}, Symbol: {trade.contract.symbol}, "
                f"Type: {trade.order.orderType}, Action: {trade.order.action}, "
                f"Qty: {trade.order.totalQuantity}, Status: {trade.orderStatus.status}"
            )

    def find_trade_by_order_id(self, order_id: int) -> Trade | None:
        """Find a Trade by its order ID."""
        for trade in self.open_trades:
            if trade.order.orderId == order_id:
                return trade
        logger.error(f"Order ID {order_id} not found.")
        return None

    def cancel_order(self, order_id: int):
        """Cancel an order by its ID."""
        trade = self.find_trade_by_order_id(order_id)
        if trade:
            self.ib.cancelOrder(trade.order)
            logger.info(f"Requested cancellation of Order ID {order_id}.")

    def move_limit_order(self, order_id: int, new_limit_price: float):
        """Modify the limit price of a LIMIT order."""
        trade = self.find_trade_by_order_id(order_id)
        if trade:
            if trade.order.orderType != "LMT":
                logger.error(f"Order ID {order_id} is not a LIMIT order.")
                return
            trade.order.lmtPrice = new_limit_price
            self.ib.placeOrder(trade.contract, trade.order)
            logger.info(f"Modified LIMIT order ID {order_id} to new limit price {new_limit_price}.")

    def move_stop_order(self, order_id: int, new_stop_price: float):
        """Modify the stop price of a STOP order."""
        trade = self.find_trade_by_order_id(order_id)
        if trade:
            if trade.order.orderType != "STP":
                logger.error(f"Order ID {order_id} is not a STOP order.")
                return
            trade.order.auxPrice = new_stop_price
            self.ib.placeOrder(trade.contract, trade.order)
            logger.info(f"Modified STOP order ID {order_id} to new stop price {new_stop_price}.")

    # ----------------------------------------
    # Create new orders
    # ----------------------------------------

    def submit_market_order(self, symbol: str, quantity: int = 1, action: str = "BUY"):
        contract = get_stock(symbol)
        order = MarketOrder(action, quantity)

        trade = self.ib.placeOrder(contract, order)
        logger.info(f"Submitted {action} MARKET order for {quantity} shares of {symbol}")

        self.ib.sleep(2)
        logger.info(f"Order Status: {trade.orderStatus.status}")

        return trade

    def submit_limit_order(self, symbol: str, quantity: int, limit_price: float, action: str = "BUY"):
        contract = get_stock(symbol)
        order = LimitOrder(action, quantity, limit_price)

        trade = self.ib.placeOrder(contract, order)
        logger.info(f"Submitted {action} LIMIT order for {quantity} shares of {symbol} at {limit_price}")

        self.ib.sleep(2)
        logger.info(f"Order Status: {trade.orderStatus.status}")

        return trade

    def submit_stop_order(self, symbol: str, quantity: int, stop_price: float, action: str = "SELL"):
        contract = get_stock(symbol)
        order = StopOrder(action, quantity, stop_price)

        trade = self.ib.placeOrder(contract, order)
        logger.info(f"Submitted {action} STOP order for {quantity} shares of {symbol} at stop price {stop_price}")

        self.ib.sleep(2)
        logger.info(f"Order Status: {trade.orderStatus.status}")

        return trade
