from app.databases.database_config import DatabaseConnection

def test_create_new_table():

    db = DatabaseConnection()

    assert db.create_table() is not None

def test_new_candle():
    db = DatabaseConnection()

    data =  {'last': '0.07218870', 'lowestAsk': '0.07223856', 'highestBid': '0.07218441',
             'close': '0.07218689', 'hash': 251867576934480480337255644773980652194,
             'moeda': "btc", 'periodicidade': 1}

    assert db.insert_candle(data)
