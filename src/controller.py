"""
Модуль контроллера бизнес-логики.
Содержит класс TriangleController, который координирует работу всех компонентов системы:
получение данных от пользователя, работу с БД, вычисления и отправку результатов.
"""

from src.triangle import Triangle
from src.database import TriangleDatabase
from src.user_interface import IUserInterface
from src.external_service import IExternalService


class TriangleController:
    """Контроллер для управления бизнес-логикой работы с треугольниками."""
    
    def __init__(self, user_interface: IUserInterface, 
                 external_service: IExternalService,
                 database: TriangleDatabase):
        """
        Инициализация контроллера.
        
        Args:
            user_interface: интерфейс для взаимодействия с пользователем
            external_service: сервис для отправки данных
            database: база данных треугольников
        """
        self.user_interface = user_interface
        self.external_service = external_service
        self.database = database
        self.triangle = Triangle()
    
    def process(self) -> str:
        """
        Выполняет сквозной сценарий обработки треугольника:
        1. Запрашивает данные у пользователя
        2. Проверяет наличие записи в БД
        3. Если нет - вычисляет и сохраняет
        4. Отправляет результат стороннему сервису
        
        Returns:
            Результат обработки (тип треугольника)
        """
        # Шаг 1: Получаем от пользователя длины трёх сторон треугольника
        side1, side2, side3 = self.user_interface.get_input()
        
        # Шаг 2: Ищем в базе данных запись с такими сторонами
        db_result = self.database.get(side1, side2, side3)
        
        # Проверяем, найдена ли запись в БД
        if db_result:
            # Если запись найдена - извлекаем из неё данные
            triangle_type, error_message = db_result
            # Если есть ошибка - возвращаем её, иначе - тип треугольника
            result = error_message if error_message else triangle_type
        else:
            # Если записи нет - вычисляем тип треугольника
            triangle_type = self.triangle.classify(side1, side2, side3)
            
            # Проверяем, является ли результат ошибкой (невалидный треугольник)
            if triangle_type == "Not a triangle":
                error_message = triangle_type
                result = error_message
            else:
                # Если треугольник валидный - ошибки нет
                error_message = None
                result = triangle_type
            
            # Сохраняем вычисленный результат в базу данных
            self.database.add(side1, side2, side3, triangle_type, error_message)
        
        # Шаг 3: Формируем строку с результатом для отправки
        data_to_send = f"Треугольник ({side1}, {side2}, {side3}): {result}"
        # Отправляем результат стороннему сервису (имитация)
        self.external_service.send_data(data_to_send)
        
        # Шаг 4: Возвращаем результат обработки
        return result
