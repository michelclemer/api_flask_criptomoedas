import random
import threading
import time
from datetime import datetime, timedelta
import logging

from ..interfaces.moedas import Moeda
from ..databases.database_config import DatabaseConnection
from ..models.conn import RequestData


class ModeloCandles:
    """
        Contém os métodos para manipular os candles
    """

    def __init__(self):

        self.__db = DatabaseConnection()

    """ Atualiza as listas """

    def atualizar_candle(self, lista: dict, nova_lista: dict) -> dict:

        """
        Atualizar
        :param lista: lista que deve ser atualizar (antiga)
        :param nova_lista:  lista contendo os novos dados (atual)
        :return: lista atualizada com o valor de fechamento
        """

        lista["highestBid"] = nova_lista["highestBid"]
        lista["lowestAsk"] = nova_lista["lowestAsk"]
        lista["close"] = nova_lista["last"]

        if "hash" not in lista.keys():
            lista["hash"] = random.getrandbits(128)
        return lista

    """ Formata os dados para serem retornados na página"""

    def formatar_resultado(self, lista: dict) -> dict:

        """
        Formata
        :param lista: Lista que será formata, traduzindo os dados para pt-br 
        :return:  Lista com chaves traduzidas
        """

        if 'hash' in lista.keys():
            nova_lista = {
                "abertura": lista["last"],
                "fechamento": lista["close"],
                "maximo": lista["highestBid"],
                "minimo": lista["lowestAsk"],
                "hash": lista["hash"],
            }
            return nova_lista
        return lista

    """ Realiza o fechamento daquela moeda em especifico, inserindo ao banco de dados"""

    def fechamento_candle(self, lista: dict, periodicidade: int) -> None:

        """
        Fechamento
        :param lista:  Lista que será inserida ao banco de dados
        :param periodicidade: quantos minutos é o candle
        :return:  None
        """

        if 'hash' in lista.keys():
            nova_lista = {
                "open": lista["last"],
                "close": lista["close"],
                "high": lista["highestBid"],
                "low": lista["lowestAsk"],
                "hash": lista["hash"],
                "moeda": 'doge_ETH',
                "periodicidade": periodicidade
            }
            self.__db.insert_candle(nova_lista)


class DogeEntities(Moeda):
    """
        Responsável pela gerenciamento da moeda DOGE
    """

    def __init__(self):

        logging.basicConfig(filename='logs.log', level=logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        self.modelo_moeda = ModeloCandles()
        self.conn_data = RequestData()
        self.__doge_doge_lista_um_minuto = {}
        self.__doge_doge_lista_cinco_minutos = {}
        self.__doge_doge_lista_dez_minutos = {}
        self.__data_atual = datetime.now()
        self.__controle_um_minuto = self.__data_atual + timedelta(minutes=1)
        self.__controle_cinco_minutos = self.__data_atual + timedelta(minutes=5)
        self.__controle_dez_minutos = self.__data_atual + timedelta(minutes=10)
        self.inicar_moedas()

    """ Realiza o monitoramento dos candles a cada 2 segundo """

    def monitor_tempo(self) -> None:
        """
        Monitor
        :return: None 
        """

        logging.info('Monitor DOG iniciado')

        while True:

            dt = datetime.now().time().minute
            logging.debug("Data Esperada: %s", self.__controle_um_minuto.minute)
            logging.debug("Data Atual: %s", dt)
            if dt == self.__controle_um_minuto.minute:
                self.modelo_moeda.fechamento_candle(self.__doge_doge_lista_um_minuto, 1)
                logging.info("[+] 1 minuto Dados - DOGE inseridos: %s", self.__doge_doge_lista_um_minuto)
                self.__doge_doge_lista_um_minuto = {}
                self.__controle_um_minuto = datetime.now() + timedelta(minutes=1)
                logging.debug("[*] 1 minuto esperado atualizado: %s", self.__controle_um_minuto.minute)
                self.moeda_um_minuto()

            if dt == self.__controle_cinco_minutos.minute:
                self.modelo_moeda.fechamento_candle(self.__doge_doge_lista_cinco_minutos, 5)
                logging.info("[+] 5 minutos Dados - DOGE inseridos: %s", self.__doge_doge_lista_cinco_minutos)
                self.__doge_doge_lista_cinco_minutos = {}
                self.__controle_cinco_minutos = datetime.now() + timedelta(minutes=5)
                logging.debug("[*] 5 minutos esperado atualizado: %s", self.__controle_cinco_minutos.minute)
                self.moeda_cinco_minutos()

            if dt == self.__controle_dez_minutos.minute:
                self.modelo_moeda.fechamento_candle(self.__doge_doge_lista_dez_minutos, 10)
                logging.info("[+] 10 minutos Dados - DOGE inseridos: %s", self.__doge_doge_lista_cinco_minutos)
                self.__doge_doge_lista_dez_minutos = {}
                self.__controle_dez_minutos = datetime.now() + timedelta(minutes=10)
                logging.debug("[*] 10 minutos esperado atualizado: %s", self.__controle_cinco_minutos.minute)
                self.moeda_dez_minutos()

            time.sleep(2)
            self.inicar_moedas()

    """ Faz uma nova requisição para atualiar o valor para o canbdle de 1 minuto """

    def moeda_um_minuto(self) -> dict:

        """
        Atualiza candle 1 minuto
        :return: dict
        """
        um = self.conn_data.moeda_base('BTC_DOGE')

        if not self.__doge_doge_lista_um_minuto:
            self.__doge_doge_lista_um_minuto = um
            return self.__doge_doge_lista_um_minuto

        elif self.__doge_doge_lista_um_minuto:
            lista = self.modelo_moeda.atualizar_candle(self.__doge_doge_lista_um_minuto, um)

            self.__doge_doge_lista_um_minuto = lista
            return lista
        return {}

    """ Faz uma nova requisição para atualiar o valor para o canbdle de 5 minuto """

    def moeda_cinco_minutos(self) -> dict:

        """
        Atualiza candle 1 minuto
        :return: dict
        """
        cinco = self.conn_data.moeda_base('BTC_DOGE')

        if not self.__doge_doge_lista_cinco_minutos:
            self.__doge_doge_lista_cinco_minutos = cinco
            return self.__doge_doge_lista_cinco_minutos

        elif self.__doge_doge_lista_cinco_minutos:
            lista = self.modelo_moeda.atualizar_candle(self.__doge_doge_lista_cinco_minutos, cinco)

            return lista
        return {}

    """ Faz uma nova requisição para atualiar o valor para o canbdle de 10 minuto """

    def moeda_dez_minutos(self):
        dez = self.conn_data.moeda_base('BTC_DOGE')

        if not self.__doge_doge_lista_dez_minutos:
            self.__doge_doge_lista_dez_minutos = dez
            return self.__doge_doge_lista_dez_minutos

        elif self.__doge_doge_lista_dez_minutos:
            lista = self.modelo_moeda.atualizar_candle(self.__doge_doge_lista_dez_minutos, dez)

            return lista

    """ Inicia o monitor de tempo para os candles """

    def inicar_monitor(self) -> None:
        """
        Inica uma Thread para o monitor como arg 
        :return: None
        """

        threading.Thread(target=self.monitor_tempo).start()

    """ Inicia a coleta dos candles de 1, 5 e 10 minutos """

    def inicar_moedas(self) -> None:
        """
        Inicia coleta
        :return:  None
        """
        self.moeda_um_minuto()
        self.moeda_cinco_minutos()
        self.moeda_dez_minutos()

    """ retorna um dicionario com todos os 3 candles """

    def retornar_moeda(self) -> dict:
        """
        Retorna dados da moeda
        :return: dict
        """

        resultado = {
            "1": self.modelo_moeda.formatar_resultado(self.moeda_um_minuto()),
            "5": self.modelo_moeda.formatar_resultado(self.moeda_cinco_minutos()),
            "10": self.modelo_moeda.formatar_resultado(self.moeda_dez_minutos()),
        }

        return resultado