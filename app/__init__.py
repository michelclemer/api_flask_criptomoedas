
from flask import Flask
from .entites.candle_controller import *
from .databases.database_config import DatabaseConnection

creat_db = DatabaseConnection()
creat_db.create_table()

app = Flask(__name__)


@app.before_first_request
def monitor():
    moeda_btc.inicar_monitor()
    moeda_doge.inicar_monitor()


app.register_blueprint(model_candle)
