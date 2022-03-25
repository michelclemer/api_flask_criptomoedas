import time

import requests
from datetime import datetime, timedelta
import threading


class Candle:
    def __init__(self):
        self.__req = requests.session()
        self.__lista_pair = {
            "last": "",
            "lowestAsk": "",
            "highestBid": "",
        }
        self.__bnb_btc_lista_um_minuto = {}
        self.__bnb_btc_lista_cinco_minutos = {}
        self.__bnb_btc_lista_dez_minutos = {}
        self.__data_atual = datetime.now()
        self.__iniciar_monitor()

    def __buscar_dados(self) -> dict:
        response = self.__req.get("https://poloniex.com/public?command=returnTicker")
        return response.json()

    def __monitor_tempo(self) -> None:

        um_minuto = self.__data_atual + timedelta(minutes=1)
        cinco_minutos = self.__data_atual + timedelta(minutes=5)
        dez_minutos = self.__data_atual + timedelta(minutes=10)
        while True:
            dt = datetime.now().time().minute
            if dt == um_minuto.minute:
                um_minuto += timedelta(minutes=1)
                self.__btc_um_minutos()
            if dt == cinco_minutos.minute:
                cinco_minutos += timedelta(minutes=5)
                self.__btc_cinco_minutos()
            if dt == dez_minutos.minute:
                dez_minutos += timedelta(minutes=10)
                self.__btc_dez_minutos()
            time.sleep(0.5)

    def __btc_base(self) -> dict:
        btc = self.__buscar_dados()["BNB_BTC"]
        lista = [i for i in self.__lista_pair.keys()]
        dicionario = {}
        for key in lista:
            dicionario[key] = btc[key]
        return dicionario

    def __btc_um_minutos(self):
        um = self.__btc_base()
        self.__bnb_btc_lista_um_minuto = um

    def __btc_cinco_minutos(self):
        cinco = self.__btc_base()
        self.__bnb_btc_lista_cinco_minutos = cinco

    def __btc_dez_minutos(self):
        dez = self.__btc_base()
        self.__bnb_btc_lista_dez_minutos = dez

    def __iniciar_monitor(self):
        t1 = threading.Thread(target=self.__monitor_tempo)
        t1.start()

    def retorna_btc(self) -> dict:
        resultado = {
            "1": self.__bnb_btc_lista_um_minuto,
            "5": self.__bnb_btc_lista_cinco_minutos,
            "10": self.__bnb_btc_lista_dez_minutos,
        }
        return resultado
