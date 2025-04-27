from ib_insync import Stock

def get_stock(symbol: str):
    return Stock(symbol, 'SMART', 'USD')
