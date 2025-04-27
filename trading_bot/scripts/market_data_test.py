from trading_bot.connection import connect, disconnect
from trading_bot.contracts import get_stock
from trading_bot.market_data import request_market_data

ib = connect()

aapl = get_stock('AAPL')
ticker = request_market_data(ib, aapl)

print(f"AAPL Bid: {ticker.bid}, Ask: {ticker.ask}, Last: {ticker.last}")

disconnect(ib)
