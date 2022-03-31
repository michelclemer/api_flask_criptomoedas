import requests


class RequestData:

    """
        Encarregada de todas as requisições para API Poloniex
    """

    def __init__(self):
        self.__lista_pair = {
            "last": "",
            "lowestAsk": "",
            "highestBid": "",
        }

    """ Realiza a busca contendo o json com todos as moedas"""
    def buscar_moeda(self) -> dict:
        """
        Buscar
        :return: dict
        """


        headers = {"accept": "application/json",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

        response = requests.get("https://poloniex.com/public?command=returnTicker", headers=headers)

        return response.json()

    """ Retorna a moeda espefica """
    def moeda_base(self, moeda: str) -> dict:
        """
        Moeda especifica
        :param moeda: Nome da criptomoeda
        :return: dict
        """

        btc = self.buscar_moeda()[moeda]
        lista = [i for i in self.__lista_pair.keys()]
        dicionario = {}
        for key in lista:
            dicionario[key] = btc[key]
        return dicionario