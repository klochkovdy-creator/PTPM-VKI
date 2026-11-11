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
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = TriangleDatabase(self.temp_db.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_full_workflow_with_calculation(self):
        mock_ui = Mock(spec=ConsoleUserInterface)
        mock_ui.get_input.return_value = (3.0, 4.0, 5.0)
        
        mock_service = Mock(spec=EmailService)
        mock_service.send_data.return_value = True
        
        controller = TriangleController(mock_ui, mock_service, self.db)
        
        result = controller.process()
        
        self.assertEqual(result, "Scalene")
        
        db_result = self.db.get(3.0, 4.0, 5.0)
        self.assertIsNotNone(db_result)
        self.assertEqual(db_result[0], "Scalene")
        
        mock_service.send_data.assert_called_once()
        call_args = mock_service.send_data.call_args[0][0]
        self.assertIn("Scalene", call_args)
    
    def test_full_workflow_from_database(self):
        self.db.add(5.0, 5.0, 5.0, "Equilateral", None)
        
        mock_ui = Mock(spec=ConsoleUserInterface)
        mock_ui.get_input.return_value = (5.0, 5.0, 5.0)
        
        mock_service = Mock(spec=EmailService)
        mock_service.send_data.return_value = True
        
        controller = TriangleController(mock_ui, mock_service, self.db)
        
        result = controller.process()
        
        self.assertEqual(result, "Equilateral")
        
        mock_service.send_data.assert_called_once()
        call_args = mock_service.send_data.call_args[0][0]
        self.assertIn("Equilateral", call_args)
    
    def test_full_workflow_with_invalid_triangle(self):
        mock_ui = Mock(spec=ConsoleUserInterface)
        mock_ui.get_input.return_value = (1.0, 2.0, 10.0)
        
        mock_service = Mock(spec=EmailService)
        mock_service.send_data.return_value = True
        
        controller = TriangleController(mock_ui, mock_service, self.db)
        
        result = controller.process()
        
        self.assertEqual(result, "Not a triangle")
        
        db_result = self.db.get(1.0, 2.0, 10.0)
        self.assertIsNotNone(db_result)
        self.assertEqual(db_result[1], "Not a triangle")
        
        mock_service.send_data.assert_called_once()
        call_args = mock_service.send_data.call_args[0][0]
        self.assertIn("Not a triangle", call_args)
    
    @patch('builtins.input', side_effect=['6', '8', '10'])
    def test_console_user_interface_integration(self, mock_input):
        ui = ConsoleUserInterface()
        
        side1, side2, side3 = ui.get_input()
        
        self.assertEqual(side1, 6.0)
        self.assertEqual(side2, 8.0)
        self.assertEqual(side3, 10.0)
        
        mock_service = Mock(spec=EmailService)
        mock_service.send_data.return_value = True
        
        controller = TriangleController(ui, mock_service, self.db)
        
        with patch('builtins.input', side_effect=['3', '3', '3']):
            result = controller.process()
        
        self.assertEqual(result, "Equilateral")
    
    def test_database_operations_integration(self):
        self.db.add(7.0, 7.0, 7.0, "Equilateral", None)
        
        result = self.db.get(7.0, 7.0, 7.0)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Equilateral")
        self.assertIsNone(result[1])
        
        self.db.delete(7.0, 7.0, 7.0)
        
        result = self.db.get(7.0, 7.0, 7.0)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
