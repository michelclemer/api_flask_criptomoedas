import requests


class Candle:
    def __init__(self):
        self.__req = requests.session()

    def __get_public_candles(self):
        response = self.__req.get("https://poloniex.com/public?command=returnTicker")
        return response.json()

    def returnTicket(self):
        return self.__get_public_candles()
