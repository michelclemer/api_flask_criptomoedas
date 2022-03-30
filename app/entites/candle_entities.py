import time
import requests
from datetime import datetime, timedelta
import threading
import random
from ..databases.database_config import DatabaseConnection

class ModeloCandles:

    def __init__(self):
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

        nova_lista = {
            "abertura": lista["last"],
            "fechamento": lista["close"],
            "maximo": lista["highestBid"],
            "minimo": lista["lowestAsk"],
            "hash": lista["hash"],
        }
        return nova_lista

    def fechamento_candle(self, lista:dict ):
        if 'hash' in lista.keys():
            nova_lista = {
                "open": lista["last"],
                "close": lista["close"],
                "high": lista["highestBid"],
                "low": lista["lowestAsk"],
                "hash": lista["hash"],
                "moeda": "BTC",
                "periodicidade": 1
            }
            self.__db.insert_candle(nova_lista)
class Candle(ModeloCandles):
    def __init__(self):

        super().__init__()
        self.__lista_pair = {
            "last": "",
            "lowestAsk": "",
            "highestBid": "",
        }
        self.__bnb_btc_lista_um_minuto = {}
        self.__bnb_btc_lista_cinco_minutos = {}
        self.__bnb_btc_lista_dez_minutos = {}
        self.__data_atual = datetime.now()
        self.__controle_um_minuto = self.__data_atual + timedelta(minutes=1)
        self.__controle_cinco_minutos = self.__data_atual + timedelta(minutes=5)
        self.__controle_dez_minutos = self.__data_atual + timedelta(minutes=10)
        self.__iniciar_candles()
        self.__iniciar_monitor()

    def __buscar_dados(self) -> dict:
        req = requests.session()
        response = req.get("https://poloniex.com/public?command=returnTicker")

        return response.json()

    def __monitor_tempo(self) -> None:
        print("Contole extreno = ", self.__controle_um_minuto)

        while True:

            dt = datetime.now().time().minute

            minuto = self.__controle_um_minuto.minute
            print(minuto, dt)
            if dt == minuto:
                print("tempo 1 minuto = ", minuto)
                self.fechamento_candle(self.__bnb_btc_lista_um_minuto)
                self.__bnb_btc_lista_um_minuto = {}
                self.__data_atual = datetime.now()
                proximo = self.__data_atual + timedelta(minutes=1, seconds=2)
                print("Procimo = ", proximo)
                self.__controle_um_minuto = proximo
                minuto = self.__controle_um_minuto.minute
                print("Dentro if ", minuto)
            print("fora if ", minuto)

            if dt == self.__controle_cinco_minutos.minute:
                self.__controle_cinco_minutos += timedelta(minutes=5)
                self.__bnb_btc_lista_cinco_minutos = {}
                self.__btc_cinco_minutos()

            if dt == self.__controle_dez_minutos.minute:
                self.__controle_dez_minutos += timedelta(minutes=10)
                self.__bnb_btc_lista_dez_minutos = {}
                self.__btc_dez_minutos()

            time.sleep(1)


    def __btc_base(self) -> dict:
        btc = self.__buscar_dados()["BTC_ETH"]
        lista = [i for i in self.__lista_pair.keys()]
        dicionario = {}
        for key in lista:
            dicionario[key] = btc[key]
        return dicionario

    def __btc_um_minuto(self):

        um = self.__btc_base()

        if not self.__bnb_btc_lista_um_minuto:
            self.__bnb_btc_lista_um_minuto = um
            return self.__bnb_btc_lista_um_minuto

        elif self.__bnb_btc_lista_um_minuto:
            lista = self.atualizar_candle(self.__bnb_btc_lista_um_minuto, um)

            self.__bnb_btc_lista_um_minuto = lista
            return lista


    def __btc_cinco_minutos(self):
        cinco = self.__btc_base()

        if not self.__bnb_btc_lista_cinco_minutos:
            self.__bnb_btc_lista_cinco_minutos = cinco
            return self.__bnb_btc_lista_cinco_minutos

        elif self.__bnb_btc_lista_cinco_minutos:
            lista = self.atualizar_candle(self.__bnb_btc_lista_cinco_minutos, cinco)

            return lista

    def __btc_dez_minutos(self):

        dez = self.__btc_base()

        if not self.__bnb_btc_lista_dez_minutos:
            self.__bnb_btc_lista_dez_minutos = dez
            return self.__bnb_btc_lista_dez_minutos

        elif self.__bnb_btc_lista_dez_minutos:
            lista = self.atualizar_candle(self.__bnb_btc_lista_dez_minutos, dez)

            return lista

    def __iniciar_monitor(self):
        t1 = threading.Thread(target=self.__monitor_tempo)
        t1.start()


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
