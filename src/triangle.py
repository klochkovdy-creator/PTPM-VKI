import math


class Triangle:
    """Класс для определения типа треугольника по трём сторонам."""
    
    @staticmethod
    def classify(a, b, c):
        """
        Определяет тип треугольника по трём сторонам.
        
        Args:
            a, b, c: длины сторон треугольника
            
        Returns:
            str: тип треугольника или сообщение об ошибке
        """
        # Валидация входных данных
        if not all(isinstance(side, (int, float)) for side in [a, b, c]):
            return "Not a triangle"
        
        if any(side <= 0 for side in [a, b, c]):
            return "Not a triangle"
        
        # Проверка неравенства треугольника с учётом погрешности float
        if not (math.isclose(a + b, c) or a + b > c):
            return "Not a triangle"
        if not (math.isclose(a + c, b) or a + c > b):
            return "Not a triangle"
        if not (math.isclose(b + c, a) or b + c > a):
            return "Not a triangle"
        
        # Определение типа треугольника
        if math.isclose(a, b) and math.isclose(b, c):
            return "Equilateral"
        elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
            return "Isosceles"
        else:
            return "Scalene"
