
from flask import Blueprint, jsonify
from .btc_entities import BtcEntities
from .doge_entities import DogeEntities

model_candle = Blueprint("candles", __name__, url_prefix="/candles")

moeda_btc = BtcEntities()
moeda_doge = DogeEntities()

@model_candle.route("/btc", methods=["GET"])
def btc():
    return jsonify(moeda_btc.retornar_moeda())


@model_candle.route("/doge", methods=["GET"])
def bts():
    return jsonify(moeda_doge.retornar_moeda())
