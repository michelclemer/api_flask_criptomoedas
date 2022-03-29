from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .entites.candle_controller import *

app = Flask(__name__)

db = SQLAlchemy(app)

app.register_blueprint(model_candle)
