import math


class Triangle:
    
    @staticmethod
    def classify(a, b, c):
        if not all(isinstance(side, (int, float)) for side in [a, b, c]):
            return "Not a triangle"
        
        if any(side <= 0 for side in [a, b, c]):
            return "Not a triangle"
        
        if not (math.isclose(a + b, c) or a + b > c):
            return "Not a triangle"
        if not (math.isclose(a + c, b) or a + c > b):
            return "Not a triangle"
        if not (math.isclose(b + c, a) or b + c > a):
            return "Not a triangle"
        
        if math.isclose(a, b) and math.isclose(b, c):
            return "Equilateral"
        elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
            return "Isosceles"
        else:
            return "Scalene"
