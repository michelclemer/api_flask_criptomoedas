from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.module_one.controllers import *

app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)

app.register_blueprint(model_candle)
