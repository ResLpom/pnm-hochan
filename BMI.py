
import math


def validate_value(value, minimum, maximum):
    value = value.strip().replace(",", ".")

    if not value:
        return None, "Vui lòng nhập giá trị"

    try:
        number = float(value)
    except ValueError:
        return None, "Giá trị phải là số"

    if not math.isfinite(number):
        return None, "Giá trị phải là số"

    if not minimum <= number <= maximum:
        return None, f"Giá trị phải từ {minimum} đến {maximum}"

    return number, ""


def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        category, color = "Thiếu cân", "warning"
    elif bmi < 23:
        category, color = "Bình thường", "success"
    elif bmi < 25:
        category, color = "Thừa cân", "warning"
    else:
        category, color = "Béo phì", "danger"

    ideal_min = round(18.5 * height_m ** 2, 1)
    ideal_max = round(22.9 * height_m ** 2, 1)

    return bmi, category, color, ideal_min, ideal_max
