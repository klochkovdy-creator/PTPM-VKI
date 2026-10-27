import math

def classify_triangle(a: float, b: float, c: float) -> str:
    if a <= 0 or b <= 0 or c <= 0:
        return "Не треугольник"

    for x, y, z in ((a, b, c), (a, c, b), (b, c, a)):
        if x + y <= z or math.isclose(x + y, z):
            return "Не треугольник"

    if math.isclose(a, b) and math.isclose(b, c):
        return "Равносторонний"
    
    if math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
        return "Равнобедренный"
        
    return "Разносторонний"