"""
Модуль для работы с базой данных треугольников.
Содержит класс TriangleDatabase для выполнения операций CRUD (создание, чтение, удаление) с записями треугольников в SQLite.
"""

import sqlite3
from typing import Optional, Tuple


class TriangleDatabase:
    """Класс для работы с базой данных треугольников."""
    
    def __init__(self, db_path: str = "triangles.db"):
        """
        Инициализация базы данных.
        
        Args:
            db_path: путь к файлу базы данных
        """
        self.db_path = db_path
        self._create_table()
    
    def _get_connection(self):
        """Создаёт и возвращает соединение с БД."""
        # Создаём соединение с базой данных по указанному пути
        conn = sqlite3.connect(self.db_path)
        # Включаем режим WAL (Write-Ahead Logging) для лучшей производительности
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    
    def _create_table(self):
        """Создаёт таблицу треугольников, если она не существует."""
        # Получаем соединение с БД
        conn = self._get_connection()
        try:
            # Создаём таблицу с полями: три стороны, тип треугольника, сообщение об ошибке
            # PRIMARY KEY (side1, side2, side3) - комбинация трёх сторон уникальна
            conn.execute("""
                CREATE TABLE IF NOT EXISTS triangles (
                    side1 REAL,
                    side2 REAL,
                    side3 REAL,
                    triangle_type TEXT,
                    error_message TEXT,
                    PRIMARY KEY (side1, side2, side3)
                )
            """)
            # Сохраняем изменения в БД
            conn.commit()
        finally:
            # Обязательно закрываем соединение для освобождения ресурсов
            conn.close()
    
    def add(self, side1: float, side2: float, side3: float, 
            triangle_type: str, error_message: Optional[str] = None):
        """
        Добавляет запись в базу данных.
        
        Args:
            side1, side2, side3: длины сторон треугольника
            triangle_type: тип треугольника
            error_message: сообщение об ошибке (если есть)
        """
        # Получаем соединение с БД
        conn = self._get_connection()
        try:
            # INSERT OR REPLACE - если запись с такими сторонами существует, она будет заменена
            # Знаки ? - это параметризованные запросы для защиты от SQL-инъекций
            conn.execute("""
                INSERT OR REPLACE INTO triangles 
                (side1, side2, side3, triangle_type, error_message)
                VALUES (?, ?, ?, ?, ?)
            """, (side1, side2, side3, triangle_type, error_message))
            # Сохраняем изменения в БД
            conn.commit()
        finally:
            # Закрываем соединение
            conn.close()
    
    def get(self, side1: float, side2: float, side3: float) -> Optional[Tuple[str, Optional[str]]]:
        """
        Получает запись из базы данных.
        
        Args:
            side1, side2, side3: длины сторон треугольника
            
        Returns:
            Кортеж (triangle_type, error_message) или None, если запись не найдена
        """
        # Получаем соединение с БД
        conn = self._get_connection()
        try:
            # Выполняем SELECT-запрос для поиска записи по трём сторонам
            cursor = conn.execute("""
                SELECT triangle_type, error_message 
                FROM triangles 
                WHERE side1 = ? AND side2 = ? AND side3 = ?
            """, (side1, side2, side3))
            # Получаем первую (и единственную) найденную запись
            result = cursor.fetchone()
            # Возвращаем результат или None, если запись не найдена
            return result if result else None
        finally:
            # Закрываем соединение
            conn.close()
    
    def delete(self, side1: float, side2: float, side3: float):
        """
        Удаляет запись из базы данных.
        
        Args:
            side1, side2, side3: длины сторон треугольника
        """
        # Получаем соединение с БД
        conn = self._get_connection()
        try:
            # Выполняем DELETE-запрос для удаления записи по трём сторонам
            conn.execute("""
                DELETE FROM triangles 
                WHERE side1 = ? AND side2 = ? AND side3 = ?
            """, (side1, side2, side3))
            # Сохраняем изменения в БД
            conn.commit()
        finally:
            # Закрываем соединение
            conn.close()
