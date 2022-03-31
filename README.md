# Flask API para Poloniex

### Poloniex API ->  ``https://docs.poloniex.com/#returnticker``

Dados os preços de execução (cotações) de uma criptomoeda reportados em tempo real
através de uma API pública.

# Dependencies
Python - Programming Language

Flask - The framework used

Pip - Dependency Management

Virtual environments

MySQL - Data base

Docker

``$ sudo apt-get install python-virtualenv``

``$ python3 -m venv venv``

``$ . venv/bin/activate``

``$ pip install Flask``

## Instalando as dependencias usando:

``$ pip install -r requirements.txt``


# Iniciando:

``docker-compuse up --build``

# Endpoints:

* Moeda BTC_ETH

``http://localhost:5000/candles/btc``

* Moeda BTC_DOGE

``http://localhost:5000/candles/doge``



## Respostas api:

imagem aqui


Resultado JSON:

* 1 : Candle de 1 minuto.
  
    ######A cada 1 minuto o valor do candle fecha 
* 5 : Candles de 5 minutos.
    
    ######A cada 5 minuto o valor do candle fecha 
* 10 : Candle de 10 minutos.

    ######A cada 10 minuto o valor do candle fecha


