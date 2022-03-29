from sqlalchemy import DateTime
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from ..databases.database_config import *


class Candle(Base):

    __tablename__ = "candles"

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(DateTime(timezone=True), default=db.func.current_timestamp())
    moeda = db.Column(db.String(100))
    periodicidade = db.Column(db.Integer)
    open = db.Column(db.String(50))
    low = db.Column(db.String(50))
    high = db.Column(db.String(50))
    close = db.Column(db.String(50))


class CandleSchema(SQLAlchemySchema):
    class Meta:
        model = Candle
        load_instance = True

    id = auto_field()
    date_time = auto_field()


Base.metadata.create_all(engine)
