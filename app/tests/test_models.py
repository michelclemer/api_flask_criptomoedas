import requests

from app.databases.database_config import DatabaseConnection


def test_new_candle():
    db = DatabaseConnection()

    data =  {'last': '0.07218870', 'lowestAsk': '0.07223856', 'highestBid': '0.07218441',
             'close': '0.07218689', 'hash': 251867576934480480337255644773980652194,
             'moeda': "btc", 'periodicidade': 1}

    assert db.insert_candle(data)

def test_return_json_btc():
    req = requests.get("http://localhost:5000/candles/btc")
    assert len(req.json()) > 0

def test_return_json_doge():
    req = requests.get("http://localhost:5000/candles/doge")
    assert len(req.json()) > 0
