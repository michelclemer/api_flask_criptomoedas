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


@model_candle.route("/", methods=["GET"])
def candle():
    return jsonify(candle_ob.returnTicket())
