import math


def classify_triangle(a: float, b: float, c: float) -> str:
    if a <= 0 or b <= 0 or c <= 0:
        return "Not a triangle"

    # Неравенство треугольника с учётом погрешности float (0.1 + 0.2 != 0.3)
    for x, y, z in ((a, b, c), (a, c, b), (b, c, a)):
        if x + y <= z or math.isclose(x + y, z):
            return "Not a triangle"

    if math.isclose(a, b) and math.isclose(b, c):
        return "Equilateral"
    if math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
        return "Isosceles"
    return "Scalene"
