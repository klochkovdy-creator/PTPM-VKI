from src.triangle import Triangle
from src.database import TriangleDatabase
from src.user_interface import IUserInterface
from src.external_service import IExternalService


class TriangleController:
    
    def __init__(self, user_interface: IUserInterface, 
                 external_service: IExternalService,
                 database: TriangleDatabase):
        self.user_interface = user_interface
        self.external_service = external_service
        self.database = database
        self.triangle = Triangle()
    
    def process(self) -> str:
        side1, side2, side3 = self.user_interface.get_input()
        
        db_result = self.database.get(side1, side2, side3)
        
        if db_result:
            triangle_type, error_message = db_result
            result = error_message if error_message else triangle_type
        else:
            triangle_type = self.triangle.classify(side1, side2, side3)
            
            if triangle_type == "Not a triangle":
                error_message = triangle_type
                result = error_message
            else:
                error_message = None
                result = triangle_type
            
            self.database.add(side1, side2, side3, triangle_type, error_message)
        
        data_to_send = f"Треугольник ({side1}, {side2}, {side3}): {result}"
        self.external_service.send_data(data_to_send)
        
        return result
