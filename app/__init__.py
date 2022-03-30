from flask import Flask

from .entites.candle_controller import *
from app.databases.database_config import DatabaseConnection

creat = DatabaseConnection()
creat.create_table()
app = Flask(__name__)



app.register_blueprint(model_candle)
