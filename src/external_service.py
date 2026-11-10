from abc import ABC, abstractmethod


class IExternalService(ABC):
    """Интерфейс для взаимодействия со сторонними сервисами."""
    
    @abstractmethod
    def send_data(self, data: str) -> bool:
        """
        Отправляет данные стороннему сервису.
        
        Args:
            data: строка с данными для отправки
            
        Returns:
            True, если отправка успешна, иначе False
        """
        pass


class EmailService(IExternalService):
    """Класс для имитации отправки данных на email-сервер."""
    
    def send_data(self, data: str) -> bool:
        """
        Имитирует отправку данных на email-сервер.
        
        Args:
            data: строка с данными для отправки
            
        Returns:
            True (имитация успешной отправки)
        """
        # Имитация отправки данных
        print(f"[EmailService] Отправка данных: {data}")
        return True
