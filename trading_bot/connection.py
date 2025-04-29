from ib_insync import IB
from trading_bot import config
from trading_bot.utils import get_logger

logger = get_logger()

def connect() -> IB:
    ib = IB()
    ib.connect(config.HOST, config.PORT, clientId=config.CLIENT_ID)
    return ib

def safe_connect() -> IB:
    ib = connect()

    account_summary = ib.accountSummary()
    paper_accounts = [a.account for a in account_summary if a.tag == "AccountType" or a.tag == "AccountCode"]
    logger.info(f"Connected accounts: {paper_accounts}")

    # Check if the account starts with DU (paper account ID typically starts with DU)
    for acc in paper_accounts:
        if acc.startswith("DU"):
            logger.info(f"✅ Connected to paper trading account: {acc}")
            return ib

    logger.error("❌ Connected to a LIVE trading account! Aborting for safety.")
    disconnect(ib)
    raise RuntimeError("Not connected to a paper account (DU*). Connection closed for safety.")

def disconnect(ib: IB):
    ib.disconnect()
