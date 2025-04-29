from trading_bot.connection import connect, disconnect

ib = connect()
print(f"Connected: {ib.isConnected()}")
disconnect(ib)
