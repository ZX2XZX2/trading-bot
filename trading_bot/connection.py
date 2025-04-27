from ib_insync import IB
from trading_bot import config

def connect():
    ib = IB()
    ib.connect(config.HOST, config.PORT, clientId=config.CLIENT_ID)
    return ib

def disconnect(ib: IB):
    ib.disconnect()
