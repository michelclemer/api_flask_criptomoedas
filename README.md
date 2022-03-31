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


# Iniciando sem o docker:

``python run.py``

# Iniciando com docker:

``docker-compose up --build``

# Endpoints:

* Moeda BTC_ETH

``http://localhost:5000/candles/btc``

* Moeda BTC_DOGE

``http://localhost:5000/candles/doge``



## Respostas api:

![image](https://user-images.githubusercontent.com/42013634/161131433-a978bc6a-7500-47b0-9500-c6dc6f97050a.png)


Resultado JSON:

* 1 : Candle de 1 minuto.
  
    ###### A cada 1 minuto o valor do candle fecha 
* 5 : Candles de 5 minutos.
    
    ###### A cada 5 minutos o valor do candle fecha 
* 10 : Candle de 10 minutos.

    ###### A cada 10 minutos o valor do candle fecha

* abertura : Preço de execução para a negociação mais recente para este par.

* fechamento : Preço final após finalizar o candle.

* maximo : Preço de venda atual mais alto para este ativo.

* minimo : Menor preço de compra atual para este ativo.

