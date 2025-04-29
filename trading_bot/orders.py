from ib_insync import MarketOrder, IB
from trading_bot.contracts import get_stock
from trading_bot.utils import get_logger

logger = get_logger()

def submit_market_order(ib: IB, symbol: str, quantity: int = 1, action: str = "BUY"):
    contract = get_stock(symbol)
    order = MarketOrder(action, quantity)

    trade = ib.placeOrder(contract, order)

    logger.info(f"Submitted {action} order for {quantity} shares of {symbol}")
    ib.sleep(2)  # allow time to process
    logger.info(f"Order Status: {trade.orderStatus.status}")

    return trade
