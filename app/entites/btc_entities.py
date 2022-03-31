import random
import threading
import time
from datetime import datetime, timedelta

from ..interfaces.moedas import Moeda
from ..databases.database_config import DatabaseConnection
from ..models.conn import RequestData

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
                "moeda": 'BTC_ETH',
                "periodicidade": periodicidade
            }
            self.__db.insert_candle(nova_lista)

class BtcEntities(Moeda):

    def __init__(self):

        self.modelo_moeda = ModeloCandles()
        self.conn_data = RequestData()
        self.__btc_btc_lista_um_minuto = {}
        self.__btc_btc_lista_cinco_minutos = {}
        self.__btc_btc_lista_dez_minutos = {}
        self.__data_atual = datetime.now()
        self.__controle_um_minuto = self.__data_atual + timedelta(minutes=1)
        self.__controle_cinco_minutos = self.__data_atual + timedelta(minutes=5)
        self.__controle_dez_minutos = self.__data_atual + timedelta(minutes=10)
        self.inicar_moedas()

    def monitor_tempo(self):
        print("Contole extreno = ", self.__controle_um_minuto)

        while True:

            dt = datetime.now().time().minute
            print("x ", self.__controle_um_minuto.minute, dt)
            if dt == self.__controle_um_minuto.minute:
                self.modelo_moeda.fechamento_candle(self.__btc_btc_lista_um_minuto, 1)
                print("1 Minuto ", self.__btc_btc_lista_um_minuto)
                self.__btc_btc_lista_um_minuto = {}
                self.__controle_um_minuto = datetime.now() + timedelta(minutes=1)
                self.moeda_um_minuto()

            if dt == self.__controle_cinco_minutos.minute:
                self.modelo_moeda.fechamento_candle(self.__btc_btc_lista_cinco_minutos, 5)
                print("5 Minutos ", self.__btc_btc_lista_cinco_minutos)
                self.__btc_btc_lista_cinco_minutos = {}
                self.__controle_cinco_minutos = datetime.now() + timedelta(minutes=5)
                self.moeda_cinco_minutos()

            if dt == self.__controle_dez_minutos.minute:
                self.modelo_moeda.fechamento_candle(self.__btc_btc_lista_dez_minutos, 10)
                print("10 Minutos ", self.__controle_dez_minutos)
                self.__btc_btc_lista_dez_minutos = {}
                self.__controle_dez_minutos = datetime.now() + timedelta(minutes=10)
                self.moeda_dez_minutos()

            time.sleep(2)
            self.inicar_moedas()

    def moeda_um_minuto(self):
        um = self.conn_data.moeda_base('BTC_ETH')

        if not self.__btc_btc_lista_um_minuto:
            self.__btc_btc_lista_um_minuto = um
            return self.__btc_btc_lista_um_minuto

        elif self.__btc_btc_lista_um_minuto:
            lista = self.modelo_moeda.atualizar_candle(self.__btc_btc_lista_um_minuto, um)

            self.__btc_btc_lista_um_minuto = lista
            return lista

    def moeda_cinco_minutos(self):
        cinco = self.conn_data.moeda_base('BTC_ETH')

        if not self.__btc_btc_lista_cinco_minutos:
            self.__btc_btc_lista_cinco_minutos = cinco
            return self.__btc_btc_lista_cinco_minutos

        elif self.__btc_btc_lista_cinco_minutos:
            lista = self.modelo_moeda.atualizar_candle(self.__btc_btc_lista_cinco_minutos, cinco)

            return lista

    def moeda_dez_minutos(self):
        dez = self.conn_data.moeda_base('BTC_ETH')

        if not self.__btc_btc_lista_dez_minutos:
            self.__btc_btc_lista_dez_minutos = dez
            return self.__btc_btc_lista_dez_minutos

        elif self.__btc_btc_lista_dez_minutos:
            lista = self.modelo_moeda.atualizar_candle(self.__btc_btc_lista_dez_minutos, dez)

            return lista

    def inicar_monitor(self):
        threading.Thread(target=self.monitor_tempo).start()

    def inicar_moedas(self):
        self.moeda_um_minuto()
        self.moeda_cinco_minutos()
        self.moeda_dez_minutos()

    def retornar_moeda(self):
        resultado = {
            "1": self.modelo_moeda.formatar_resultado(self.moeda_um_minuto()),
            "5": self.modelo_moeda.formatar_resultado(self.moeda_cinco_minutos()),
            "10": self.modelo_moeda.formatar_resultado(self.moeda_dez_minutos()),
        }

        return resultado