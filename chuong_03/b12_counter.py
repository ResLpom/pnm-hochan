from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False
counter = 0


@app.get("/counter")
def get_counter():
    return jsonify(counter=counter)


@app.post("/counter")
def increase_counter():
    global counter
    try:
        step = int(request.args.get("step", "1"))
    except ValueError:
        return jsonify(error="step phải là số nguyên."), 400
    counter += step
    return jsonify(counter=counter, message=f"Đã tăng {step}")


@app.delete("/counter")
def reset_counter():
    global counter
    counter = 0
    return "", 204
