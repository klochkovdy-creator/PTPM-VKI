from abc import ABC, abstractmethod
from typing import Tuple


class IUserInterface(ABC):
    
    @abstractmethod
    def get_input(self) -> Tuple[float, float, float]:
        pass


class ConsoleUserInterface(IUserInterface):
    
    def get_input(self) -> Tuple[float, float, float]:
        side1 = float(input("Введите длину первой стороны: "))
        side2 = float(input("Введите длину второй стороны: "))
        side3 = float(input("Введите длину третьей стороны: "))
        return side1, side2, side3
