from abc import ABC, abstractmethod


class IExternalService(ABC):
    
    @abstractmethod
    def send_data(self, data: str) -> bool:
        pass


class EmailService(IExternalService):
    
    def send_data(self, data: str) -> bool:
        print(f"[EmailService] Отправка данных: {data}")
        return True
