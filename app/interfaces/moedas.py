from abc import ABC,abstractmethod


class Moeda(ABC):

    """
        Classe que será implementada caso precise criar mais de uma moeda
    """

    @abstractmethod
    def monitor_tempo(self):
        pass

    @abstractmethod
    def moeda_um_minuto(self):
        pass

    @abstractmethod
    def moeda_cinco_minutos(self):
        pass

    @abstractmethod
    def moeda_dez_minutos(self):
        pass

    @abstractmethod
    def inicar_monitor(self):
        pass

    @abstractmethod
    def inicar_moedas(self):
        pass

    @abstractmethod
    def retornar_moeda(self):
        pass