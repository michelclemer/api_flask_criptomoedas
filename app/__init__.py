from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from app.module_one.controllers import *
from app.module_one.databases.mysql_database import init_db

app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)

app.register_blueprint(model_candle)
