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
        # 1. Получаем входные данные от пользователя
        side1, side2, side3 = self.user_interface.get_input()
        
        # 2. Проверяем наличие записи в БД
        db_result = self.database.get(side1, side2, side3)
        
        if db_result:
            # Результат найден в БД
            triangle_type, error_message = db_result
            result = error_message if error_message else triangle_type
        else:
            # Вычисляем результат
            triangle_type = self.triangle.classify(side1, side2, side3)
            
            # Определяем, является ли результат ошибкой
            if triangle_type == "Not a triangle":
                error_message = triangle_type
                result = error_message
            else:
                error_message = None
                result = triangle_type
            
            # Сохраняем в БД
            self.database.add(side1, side2, side3, triangle_type, error_message)
        
        # 3. Отправляем результат стороннему сервису
        data_to_send = f"Треугольник ({side1}, {side2}, {side3}): {result}"
        self.external_service.send_data(data_to_send)
        
        # 4. Возвращаем результат
        return result
