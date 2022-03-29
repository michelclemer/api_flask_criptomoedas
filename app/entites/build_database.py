from api_flask_criptomoedas.app.models.models import *


class BuildDatabase:
    def __init__(self):
        self.session = session

    def adicionar_candle(
        self, moeda: str, periodicidade: int, open: str, low: str, high: str, close: str
    ) -> None:
        """
        Adiciona um candle finalizado ao banco de dados
        :param moeda: Nome da moeda
        :param periodicidade: tempo em minutos
        :param open: valor de abertura
        :param low: valor mais alto
        :param high: valor mais baixo
        :param close:  valor de fechamento
        :return: None
        """
        candle = Candle(
            moeda=moeda,
            periodicidade=periodicidade,
            open=open,
            low=low,
            high=high,
            close=close,
        )
        self.session.add(candle)
        self.session.commit()
