
import math


def parse_number(value):
    value = value.strip().replace(",", ".")

    if not value:
        raise ValueError("Vui lòng nhập số.")

    try:
        number = float(value)
    except ValueError:
        raise ValueError("Vui lòng nhập số hợp lệ.")

    if not math.isfinite(number):
        raise ValueError("Vui lòng nhập số hợp lệ.")

    return number


def format_number(number):
    return f"{number:.12g}"


def calculate(a, op, b):
    if op == "+":
        return a + b

    if op == "-":
        return a - b

    if op == "*":
        return a * b

    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Không thể chia cho 0.")
        return a / b

    raise ValueError("Phép toán không hợp lệ.")
