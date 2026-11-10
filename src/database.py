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
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    
    def _create_table(self):
        """Создаёт таблицу треугольников, если она не существует."""
        conn = self._get_connection()
        try:
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
            conn.commit()
        finally:
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
        conn = self._get_connection()
        try:
            conn.execute("""
                INSERT OR REPLACE INTO triangles 
                (side1, side2, side3, triangle_type, error_message)
                VALUES (?, ?, ?, ?, ?)
            """, (side1, side2, side3, triangle_type, error_message))
            conn.commit()
        finally:
            conn.close()
    
    def get(self, side1: float, side2: float, side3: float) -> Optional[Tuple[str, Optional[str]]]:
        """
        Получает запись из базы данных.
        
        Args:
            side1, side2, side3: длины сторон треугольника
            
        Returns:
            Кортеж (triangle_type, error_message) или None, если запись не найдена
        """
        conn = self._get_connection()
        try:
            cursor = conn.execute("""
                SELECT triangle_type, error_message 
                FROM triangles 
                WHERE side1 = ? AND side2 = ? AND side3 = ?
            """, (side1, side2, side3))
            result = cursor.fetchone()
            return result if result else None
        finally:
            conn.close()
    
    def delete(self, side1: float, side2: float, side3: float):
        """
        Удаляет запись из базы данных.
        
        Args:
            side1, side2, side3: длины сторон треугольника
        """
        conn = self._get_connection()
        try:
            conn.execute("""
                DELETE FROM triangles 
                WHERE side1 = ? AND side2 = ? AND side3 = ?
            """, (side1, side2, side3))
            conn.commit()
        finally:
            conn.close()
