"""
Модуль интеграционных тестов для системы классификации треугольников.
Тестирует взаимодействие всех компонентов системы: контроллера, БД, пользовательского интерфейса и внешнего сервиса.
Использует unittest.mock для создания заглушек (mock) вместо реальных объектов.
"""

import unittest
import os
import tempfile
from unittest.mock import Mock, patch
from src.controller import TriangleController
from src.database import TriangleDatabase
from src.user_interface import ConsoleUserInterface
from src.external_service import EmailService
from src.triangle import Triangle


class TestTriangleIntegration(unittest.TestCase):
    """Интеграционные тесты для системы работы с треугольниками."""
    
    def setUp(self):
        """Подготовка к каждому тесту."""
        # Создаём временный файл БД для изоляции тестов друг от друга
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        # Закрываем файл, чтобы SQLite мог его использовать
        self.temp_db.close()
        # Создаём объект БД с временным файлом
        self.db = TriangleDatabase(self.temp_db.name)
    
    def tearDown(self):
        """Очистка после каждого теста."""
        # Удаляем временный файл БД после завершения теста
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_full_workflow_with_calculation(self):
        """
        Интеграционный тест: полный сценарий с вычислением.
        Проверяет взаимодействие контроллера, БД, класса вычислений и внешнего сервиса.
        """
        # Создаём мок пользовательского интерфейса
        mock_ui = Mock(spec=ConsoleUserInterface)
        # Настраиваем, чтобы get_input возвращал стороны треугольника 3, 4, 5
        mock_ui.get_input.return_value = (3.0, 4.0, 5.0)
        
        # Создаём мок внешнего сервиса
        mock_service = Mock(spec=EmailService)
        # Настраиваем, чтобы send_data всегда возвращал True
        mock_service.send_data.return_value = True
        
        # Создаём контроллер с реальной БД и моками UI/сервиса
        controller = TriangleController(mock_ui, mock_service, self.db)
        
        # Выполняем полный процесс обработки
        result = controller.process()
        
        # Проверяем, что треугольник 3-4-5 определён как разносторонний
        self.assertEqual(result, "Scalene")
        
        # Проверяем, что данные были сохранены в БД
        db_result = self.db.get(3.0, 4.0, 5.0)
        self.assertIsNotNone(db_result)
        self.assertEqual(db_result[0], "Scalene")
        
        # Проверяем, что внешний сервис был вызван ровно один раз
        mock_service.send_data.assert_called_once()
        # Получаем аргумент, с которым был вызван send_data
        call_args = mock_service.send_data.call_args[0][0]
        # Проверяем, что в отправленной строке есть результат "Scalene"
        self.assertIn("Scalene", call_args)
    
    def test_full_workflow_from_database(self):
        """
        Интеграционный тест: получение результата из БД.
        Проверяет, что при повторном запросе данные берутся из БД, а не вычисляются заново.
        """
        # Предварительно сохраняем данные о равностороннем треугольнике в БД
        self.db.add(5.0, 5.0, 5.0, "Equilateral", None)
        
        # Создаём моки UI и внешнего сервиса
        mock_ui = Mock(spec=ConsoleUserInterface)
        # При запросе пользователь вводит те же стороны, что уже есть в БД
        mock_ui.get_input.return_value = (5.0, 5.0, 5.0)
        
        mock_service = Mock(spec=EmailService)
        mock_service.send_data.return_value = True
        
        # Создаём контроллер
        controller = TriangleController(mock_ui, mock_service, self.db)
        
        # Выполняем процесс
        result = controller.process()
        
        # Проверяем, что результат взят из БД (равносторонний треугольник)
        self.assertEqual(result, "Equilateral")
        
        # Проверяем, что внешний сервис был вызван с правильными данными
        mock_service.send_data.assert_called_once()
        call_args = mock_service.send_data.call_args[0][0]
        self.assertIn("Equilateral", call_args)
    
    def test_full_workflow_with_invalid_triangle(self):
        """
        Интеграционный тест: обработка невалидного треугольника.
        Проверяет корректную обработку ошибочных данных через всю систему.
        """
        # Создаём моки
        mock_ui = Mock(spec=ConsoleUserInterface)
        # Стороны 1, 2, 10 не образуют треугольник (нарушено неравенство треугольника)
        mock_ui.get_input.return_value = (1.0, 2.0, 10.0)
        
        mock_service = Mock(spec=EmailService)
        mock_service.send_data.return_value = True
        
        # Создаём контроллер
        controller = TriangleController(mock_ui, mock_service, self.db)
        
        # Выполняем процесс
        result = controller.process()
        
        # Проверяем, что результат - сообщение об ошибке
        self.assertEqual(result, "Not a triangle")
        
        # Проверяем, что ошибка сохранена в БД
        db_result = self.db.get(1.0, 2.0, 10.0)
        self.assertIsNotNone(db_result)
        # error_message находится во втором элементе кортежа
        self.assertEqual(db_result[1], "Not a triangle")
        
        # Проверяем, что внешний сервис был вызван с сообщением об ошибке
        mock_service.send_data.assert_called_once()
        call_args = mock_service.send_data.call_args[0][0]
        self.assertIn("Not a triangle", call_args)
    
    @patch('builtins.input', side_effect=['6', '8', '10'])
    def test_console_user_interface_integration(self, mock_input):
        """
        Интеграционный тест: имитация реального пользовательского ввода.
        Проверяет работу с реальным классом ConsoleUserInterface через mock.
        """
        # Создаём реальный объект ConsoleUserInterface (не мок!)
        ui = ConsoleUserInterface()
        
        # Получаем данные - благодаря @patch input будет возвращать '6', '8', '10'
        side1, side2, side3 = ui.get_input()
        
        # Проверяем корректность полученных данных (строки преобразовались в float)
        self.assertEqual(side1, 6.0)
        self.assertEqual(side2, 8.0)
        self.assertEqual(side3, 10.0)
        
        # Создаём мок внешнего сервиса
        mock_service = Mock(spec=EmailService)
        mock_service.send_data.return_value = True
        
        # Создаём контроллер с реальным UI (не моком)
        controller = TriangleController(ui, mock_service, self.db)
        
        # Выполняем процесс с новым вводом (равносторонний треугольник 3-3-3)
        with patch('builtins.input', side_effect=['3', '3', '3']):
            result = controller.process()
        
        # Проверяем, что треугольник 3-3-3 определён как равносторонний
        self.assertEqual(result, "Equilateral")
    
    def test_database_operations_integration(self):
        """
        Тест: проверка работы всех операций БД в связке.
        Не является полностью интеграционным (изолирован от контроллера),
        но проверяет интеграцию с SQLite.
        """
        # Добавляем запись о равностороннем треугольнике 7-7-7
        self.db.add(7.0, 7.0, 7.0, "Equilateral", None)
        
        # Получаем эту запись из БД
        result = self.db.get(7.0, 7.0, 7.0)
        # Проверяем, что запись найдена
        self.assertIsNotNone(result)
        # Проверяем тип треугольника
        self.assertEqual(result[0], "Equilateral")
        # Проверяем, что ошибки нет (None)
        self.assertIsNone(result[1])
        
        # Удаляем эту запись
        self.db.delete(7.0, 7.0, 7.0)
        
        # Проверяем, что запись действительно удалена
        result = self.db.get(7.0, 7.0, 7.0)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
