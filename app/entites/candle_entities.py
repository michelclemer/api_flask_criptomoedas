
import time
import requests
from datetime import datetime, timedelta
import threading
import random
from ..databases.database_config import DatabaseConnection

class ModeloCandles:

    def __init__(self, moeda):
        self.moeda = moeda
        self.__db = DatabaseConnection()

    def atualizar_candle(self, lista: dict, nova_lista: dict) -> dict:

        lista["highestBid"] = nova_lista["highestBid"]
        lista["lowestAsk"] = nova_lista["lowestAsk"]
        lista["close"] = nova_lista["last"]

        if "hash" not in lista.keys():
            lista["hash"] = random.getrandbits(128)
        return lista

    def formatar_resultado(self, lista):
        print("formatar = ", lista)

        if 'hash' in lista.keys():
            nova_lista = {
                "abertura": lista["last"],
                "fechamento": lista["close"],
                "maximo": lista["highestBid"],
                "minimo": lista["lowestAsk"],
                "hash": lista["hash"],
            }
            return nova_lista

    def fechamento_candle(self, lista:dict, periodicidade: int):
        if 'hash' in lista.keys():
            nova_lista = {
                "open": lista["last"],
                "close": lista["close"],
                "high": lista["highestBid"],
                "low": lista["lowestAsk"],
                "hash": lista["hash"],
                "moeda": self.moeda,
                "periodicidade": periodicidade
            }
            self.__db.insert_candle(nova_lista)

class Candle(ModeloCandles):
    def __init__(self, moeda):

        super().__init__(moeda)
        self.__lista_pair = {
            "last": "",
            "lowestAsk": "",
            "highestBid": "",
        }
        self.__btc_btc_lista_um_minuto = {}
        self.__btc_btc_lista_cinco_minutos = {}
        self.__btc_btc_lista_dez_minutos = {}
        self.__data_atual = datetime.now()
        self.__controle_um_minuto = self.__data_atual + timedelta(minutes=1)
        self.__controle_cinco_minutos = self.__data_atual + timedelta(minutes=5)
        self.__controle_dez_minutos = self.__data_atual + timedelta(minutes=10)
        self.__iniciar_candles()


    def __buscar_dados(self) -> dict:
        req = requests.session()
        response = req.get("https://poloniex.com/public?command=returnTicker")

        return response.json()

    def __monitor_tempo(self):
        print("Contole extreno = ", self.__controle_um_minuto)

        while True:

            dt = datetime.now().time().minute
            print("x ", self.__controle_um_minuto.minute, dt)
            if dt == self.__controle_um_minuto.minute:
                self.fechamento_candle(self.__btc_btc_lista_um_minuto, 1)
                print("1 Minuto ",self.__btc_btc_lista_um_minuto)
                self.__btc_btc_lista_um_minuto = {}
                self.__controle_um_minuto = datetime.now() + timedelta(minutes=1)
                self.__btc_um_minuto()

            if dt == self.__controle_cinco_minutos.minute:
                self.fechamento_candle(self.__btc_btc_lista_cinco_minutos, 5)
                print("5 Minutos ", self.__btc_btc_lista_cinco_minutos)
                self.__btc_btc_lista_cinco_minutos = {}
                self.__controle_cinco_minutos = datetime.now() + timedelta(minutes=5)
                self.__btc_cinco_minutos()

            if dt == self.__controle_dez_minutos.minute:
                self.fechamento_candle(self.__btc_btc_lista_dez_minutos, 10)
                print("10 Minutos ", self.__controle_dez_minutos)
                self.__btc_btc_lista_dez_minutos = {}
                self.__controle_dez_minutos = datetime.now() + timedelta(minutes=10)
                self.__btc_dez_minutos()

            time.sleep(2)
            self.__iniciar_candles()
    def __btc_base(self) -> dict:
        btc = self.__buscar_dados()["BTC_ETH"]
        lista = [i for i in self.__lista_pair.keys()]
        dicionario = {}
        for key in lista:
            dicionario[key] = btc[key]
        return dicionario

    def __btc_um_minuto(self):

        um = self.__btc_base()

        if not self.__btc_btc_lista_um_minuto:
            self.__btc_btc_lista_um_minuto = um
            return self.__btc_btc_lista_um_minuto

        elif self.__btc_btc_lista_um_minuto:
            lista = self.atualizar_candle(self.__btc_btc_lista_um_minuto, um)

            self.__btc_btc_lista_um_minuto = lista
            return lista


    def __btc_cinco_minutos(self):
        cinco = self.__btc_base()

        if not self.__btc_btc_lista_cinco_minutos:
            self.__btc_btc_lista_cinco_minutos = cinco
            return self.__btc_btc_lista_cinco_minutos

        elif self.__btc_btc_lista_cinco_minutos:
            lista = self.atualizar_candle(self.__btc_btc_lista_cinco_minutos, cinco)

            return lista

    def __btc_dez_minutos(self):

        dez = self.__btc_base()

        if not self.__btc_btc_lista_dez_minutos:
            self.__btc_btc_lista_dez_minutos = dez
            return self.__btc_btc_lista_dez_minutos

        elif self.__btc_btc_lista_dez_minutos:
            lista = self.atualizar_candle(self.__btc_btc_lista_dez_minutos, dez)

            return lista

    def iniciar_monitor(self):
        threading.Thread(target=self.__monitor_tempo).start()


    def __iniciar_candles(self):

        self.__btc_um_minuto()
        self.__btc_cinco_minutos()
        self.__btc_dez_minutos()


    def retorna_btc(self) -> dict:

        resultado = {
            "1": self.formatar_resultado(self.__btc_um_minuto()),
            "5": self.formatar_resultado(self.__btc_cinco_minutos()),
            "10": self.formatar_resultado(self.__btc_dez_minutos()),
        }

        return resultado

