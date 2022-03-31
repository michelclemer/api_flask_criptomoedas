import time

from flask import Blueprint, request, jsonify
from .btc_entities import BtcEntities
from .bts_entities import BtsEntities



model_candle = Blueprint("candles", __name__, url_prefix="/candles")
moeda_btc = BtcEntities()
moeda_bts = BtsEntities()

@model_candle.route("/btc", methods=["GET"])
def btc():
    return jsonify(moeda_btc.retornar_moeda())


@model_candle.route("/bts", methods=["GET"])
def bts():
    return jsonify(moeda_bts.retornar_moeda())
