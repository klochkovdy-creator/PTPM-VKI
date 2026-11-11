"""
Модуль для взаимодействия с пользователем.
Содержит абстрактный интерфейс IUserInterface и его реализацию ConsoleUserInterface для работы через консоль.
"""

from abc import ABC, abstractmethod
from typing import Tuple


class IUserInterface(ABC):
    """Интерфейс для взаимодействия с пользователем."""
    
    @abstractmethod
    def get_input(self) -> Tuple[float, float, float]:
        """
        Получает входные данные от пользователя.
        
        Returns:
            Кортеж из трёх длин сторон треугольника
        """
        pass


class ConsoleUserInterface(IUserInterface):
    """Класс для взаимодействия с пользователем через консоль."""
    
    def get_input(self) -> Tuple[float, float, float]:
        """
        Получает длины сторон треугольника от пользователя через консоль.
        
        Returns:
            Кортеж из трёх длин сторон
        """
        # Запрашиваем у пользователя длину первой стороны и преобразуем в float
        side1 = float(input("Введите длину первой стороны: "))
        # Запрашиваем длину второй стороны
        side2 = float(input("Введите длину второй стороны: "))
        # Запрашиваем длину третьей стороны
        side3 = float(input("Введите длину третьей стороны: "))
        # Возвращаем все три стороны в виде кортежа
        return side1, side2, side3
