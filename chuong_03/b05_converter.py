from flask import Flask, jsonify
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class ListConverter(BaseConverter):
    regex = r"-?\d+(?:,-?\d+)*"

    def to_python(self, value):
        return [int(n) for n in value.split(",")]

    def to_url(self, values):
        return ",".join(str(int(n)) for n in values)


app.url_map.converters["list"] = ListConverter


@app.get("/sum/<list:numbers>")
def sum_numbers(numbers):
    return jsonify(numbers=numbers, sum=sum(numbers))
