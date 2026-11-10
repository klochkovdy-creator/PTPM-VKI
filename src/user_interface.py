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
        side1 = float(input("Введите длину первой стороны: "))
        side2 = float(input("Введите длину второй стороны: "))
        side3 = float(input("Введите длину третьей стороны: "))
        return side1, side2, side3
