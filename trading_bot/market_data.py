from ib_insync import IB, Ticker

def request_market_data(ib: IB, contract) -> Ticker:
    ib.reqMarketDataType(3)  # 1=live, 3=delayed if necessary
    ticker = ib.reqMktData(contract)
    ib.sleep(2)
    return ticker