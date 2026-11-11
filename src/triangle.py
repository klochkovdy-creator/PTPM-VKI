"""
Модуль для классификации треугольников.
Содержит класс Triangle с методом classify для определения типа треугольника по длинам трёх сторон.
"""

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
        # Проверяем, что все стороны являются числами (int или float)
        if not all(isinstance(side, (int, float)) for side in [a, b, c]):
            return "Not a triangle"
        
        # Проверяем, что все стороны положительные (больше нуля)
        if any(side <= 0 for side in [a, b, c]):
            return "Not a triangle"
        
        # Проверяем неравенство треугольника: сумма двух сторон должна быть больше третьей
        # Используем math.isclose для учёта погрешности вычислений с float
        if not (math.isclose(a + b, c) or a + b > c):
            return "Not a triangle"
        if not (math.isclose(a + c, b) or a + c > b):
            return "Not a triangle"
        if not (math.isclose(b + c, a) or b + c > a):
            return "Not a triangle"
        
        # Определяем тип треугольника по равенству сторон
        # Если все три стороны равны - равносторонний
        if math.isclose(a, b) and math.isclose(b, c):
            return "Equilateral"
        # Если хотя бы две стороны равны - равнобедренный
        elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
            return "Isosceles"
        # Если все стороны разные - разносторонний
        else:
            return "Scalene"
