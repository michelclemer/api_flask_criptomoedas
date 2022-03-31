import requests

class RequestData:

    def __init__(self):
        self.__lista_pair = {
            "last": "",
            "lowestAsk": "",
            "highestBid": "",
        }

    def buscar_moeda(self) -> dict:
        req = requests.session()
        headers = {}
        headers["accept"] = "application/json"
        headers[
            "user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"

        response = req.get("https://poloniex.com/public?command=returnTicker", headers=headers)

        return response.json()

    def moeda_base(self, moeda: str) -> dict:
        btc = self.buscar_moeda()[moeda]
        lista = [i for i in self.__lista_pair.keys()]
        dicionario = {}
        for key in lista:
            dicionario[key] = btc[key]
        return dicionario