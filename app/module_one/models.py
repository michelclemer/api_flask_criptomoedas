from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from app import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(DateTime(timezone=True), default=db.func.current_timestamp())


class Candle(Base):
    __tablename__ = "candles"

    moeda = db.Column(db.String(100))
    periodicidade = db.Column(db.Integer)
    open = db.Column(db.String(50))
    low = db.Column(db.String(50))
    high = db.Column(db.String(50))
    close = db.Column(db.String(50))
