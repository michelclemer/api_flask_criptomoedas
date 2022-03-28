from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
    jsonify,
)

from app import *

from app.module_one.candles_model import Candle


model_candle = Blueprint("candles", __name__, url_prefix="/candles")
candle_ob = Candle()


@model_candle.route("/btc", methods=["GET"])
def candle():
    return jsonify(candle_ob.retorna_btc())


@model_candle.route("/", methods=["GET"])
def show_pair():
    id = request.args.get("id", None)
    if id is None:
        return jsonify({"message": {}})
    print(request.args)
    return id
