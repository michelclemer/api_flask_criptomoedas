import time

from poloniex import Poloniex

polo = Poloniex()
while True:
    ticker = polo.returnTicker()["BTC_ETH"]
    print(ticker)
    time.sleep(2)
