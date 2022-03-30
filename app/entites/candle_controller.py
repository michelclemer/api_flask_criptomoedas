import time

from flask import Blueprint, request, jsonify
from .candle_entities import Candle



model_candle = Blueprint("candles", __name__, url_prefix="/candles")
candle_ob = Candle('BTC')


@model_candle.route("/btc", methods=["GET"])
def candle():
    return jsonify(candle_ob.retorna_btc())


@model_candle.route("/", methods=["GET"])
def show_pair():
    id = request.args.get("id", None)
    if id is None:
        return jsonify({"message": {}})
    return id
