from datetime import datetime, timedelta, timezone
from random import randint
from flask import Flask, abort, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False

WEEKDAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm",
            "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=error.description), 400


@app.get("/api/time")
def api_time():
    now = datetime.now(timezone(timedelta(hours=7)))
    return jsonify(iso=now.isoformat(timespec="seconds"),
                   date=now.strftime("%d/%m/%Y"),
                   time=now.strftime("%H:%M:%S"),
                   weekday=WEEKDAYS[now.weekday()])


@app.get("/api/random")
def api_random():
    try:
        minimum = int(request.args.get("min", "1"))
        maximum = int(request.args.get("max", "100"))
        count = int(request.args.get("count", "1"))
    except ValueError:
        abort(400, description="min, max và count phải là số nguyên.")
    if minimum > maximum:
        abort(400, description="min không được lớn hơn max.")
    if not 1 <= count <= 100:
        abort(400, description="count phải từ 1 đến 100.")
    return jsonify(min=minimum, max=maximum, count=count,
                   numbers=[randint(minimum, maximum) for _ in range(count)])
