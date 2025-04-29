from ib_insync import IB, MarketOrder, LimitOrder, StopOrder
from trading_bot.contracts import get_stock
from trading_bot.utils import get_logger

logger = get_logger()

def submit_market_order(ib: IB, symbol: str, quantity: int = 1, action: str = "BUY"):
    contract = get_stock(symbol)
    order = MarketOrder(action, quantity)

    trade = ib.placeOrder(contract, order)

    logger.info(f"Submitted {action} MARKET order for {quantity} shares of {symbol}")
    ib.sleep(2)
    logger.info(f"Order Status: {trade.orderStatus.status}")

    return trade

def submit_limit_order(ib: IB, symbol: str, quantity: int, limit_price: float, action: str = "BUY"):
    contract = get_stock(symbol)
    order = LimitOrder(action, quantity, limit_price)

    trade = ib.placeOrder(contract, order)

    logger.info(f"Submitted {action} LIMIT order for {quantity} shares of {symbol} at {limit_price}")
    ib.sleep(2)
    logger.info(f"Order Status: {trade.orderStatus.status}")

    return trade

def submit_stop_order(ib: IB, symbol: str, quantity: int, stop_price: float, action: str = "SELL"):
    contract = get_stock(symbol)
    order = StopOrder(action, quantity, stop_price)

    trade = ib.placeOrder(contract, order)

    logger.info(f"Submitted {action} STOP order for {quantity} shares of {symbol} at stop price {stop_price}")
    ib.sleep(2)
    logger.info(f"Order Status: {trade.orderStatus.status}")

    return trade

def cancel_order(ib: IB, order_id: int):
    ib.reqOpenOrders()
    ib.sleep(1)  # Allow time to sync

    for trade in ib.openTrades():
        if trade.order.orderId == order_id:
            ib.cancelOrder(trade.order)
            logger.info(f"Requested cancel for Order ID {order_id}")
            return

    logger.error(f"Order ID {order_id} not found among open trades.")


def list_open_orders(ib: IB):
    ib.reqOpenOrders()
    ib.sleep(1)  # allow time
    orders = ib.openTrades()

    logger.info(f"Found {len(orders)} open trades:")
    for trade in orders:
        logger.info(
            f"Order ID: {trade.order.orderId}, Symbol: {trade.contract.symbol}, Action: {trade.order.action}, Quantity: {trade.order.totalQuantity}, Status: {trade.orderStatus.status}"
        )
    return orders

def move_stop_order(ib: IB, order_id: int, new_stop_price: float):
    orders = ib.openTrades()
    for trade in orders:
        if trade.order.orderId == order_id:
            logger.info(f"Modifying STOP order ID {order_id} to new stop price {new_stop_price}")
            trade.order.auxPrice = new_stop_price
            ib.placeOrder(trade.contract, trade.order)
            return
    logger.error(f"Order ID {order_id} not found among open trades.")
