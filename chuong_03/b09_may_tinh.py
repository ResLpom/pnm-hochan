from math import isfinite
from flask import Flask, abort, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=error.description), 400


@app.get("/calc")
def calc():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    op = request.args.get("op", "add")
    if a is None or b is None or not isfinite(a) or not isfinite(b):
        abort(400, description="a và b phải là số hợp lệ.")

    if op == "add":
        result, symbol = a + b, "+"
    elif op == "sub":
        result, symbol = a - b, "-"
    elif op == "mul":
        result, symbol = a * b, "*"
    elif op == "div":
        if b == 0:
            abort(400, description="Không thể chia cho 0.")
        result, symbol = a / b, "/"
    else:
        abort(400, description="Phép toán không hợp lệ.")
    if not isfinite(result):
        abort(400, description="Kết quả vượt giới hạn số.")

    return jsonify(a=a, b=b, op=op,
                   expression=f"{a:g} {symbol} {b:g}", result=result)
