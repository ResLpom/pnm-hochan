
from flask import Flask, render_template, request
from Calculator import calculate, format_number, parse_number
from Score import calculate_grade, validate_score
from BMI import calculate_bmi, validate_value

app = Flask(
    __name__,
    template_folder="chuong_03/templates",
    static_folder="chuong_03/static"
)


@app.route("/")
def menu():
    return render_template("menu.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    values = {k: request.form.get(k, "") for k in ("a", "op", "b")}

    if not values["op"]:
        values["op"] = "+"

    errors = {k: "" for k in values}
    result = None

    if request.method == "POST":
        numbers = {}

        for k in ("a", "b"):
            try:
                numbers[k] = parse_number(values[k])
            except ValueError as e:
                errors[k] = str(e)

        if values["op"] not in ("+", "-", "*", "/"):
            errors["op"] = "Phép toán không hợp lệ."

        if not any(errors.values()):
            try:
                answer = calculate(
                    numbers["a"], values["op"], numbers["b"]
                )
                result = (
                    f"{format_number(numbers['a'])} {values['op']} "
                    f"{format_number(numbers['b'])} = {format_number(answer)}"
                )
            except ZeroDivisionError as e:
                errors["b"] = str(e)

    return render_template(
        "calculator.html",
        values=values,
        errors=errors,
        result=result
    )


@app.route("/score", methods=["GET", "POST"])
def score():
    values = {
        k: request.form.get(k, "")
        for k in ("cc", "gk", "ck")
    }

    errors = {k: "" for k in values}
    total = grade = None
    is_liet = False

    if request.method == "POST":
        scores = {}

        for k, value in values.items():
            scores[k], errors[k] = validate_score(value)

        if not any(errors.values()):
            total, grade = calculate_grade(
                scores["cc"], scores["gk"], scores["ck"]
            )
            is_liet = scores["ck"] < 1

    return render_template(
        "Score.html",
        values=values,
        errors=errors,
        total=total,
        grade=grade,
        is_liet=is_liet
    )


@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    values = {
        k: request.form.get(k, "")
        for k in ("height", "weight")
    }

    errors = {k: "" for k in values}
    result = None

    if request.method == "POST":
        height, errors["height"] = validate_value(
            values["height"], 50, 250
        )

        weight, errors["weight"] = validate_value(
            values["weight"], 10, 300
        )

        if not any(errors.values()):
            result = calculate_bmi(height, weight)

    return render_template(
        "bmi.html",
        values=values,
        errors=errors,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True, port=8000)
