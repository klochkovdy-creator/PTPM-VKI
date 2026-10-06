import unittest
import datetime
from src.delivery import calculate_delivery_cost

class TestDeliveryService(unittest.TestCase):
    def test_standard_delivery_basic(self):
        cost, date = calculate_delivery_cost(2.0, 100, "обычный", False)
        self.assertEqual(cost, 700)
        self.assertEqual(date, "2026-09-04")

    def test_weight_boundary_min(self):
        cost, date = calculate_delivery_cost(0.1, 100, "обычный", False)
        self.assertEqual(cost, 700)

    def test_weight_boundary_max(self):
        cost, date = calculate_delivery_cost(50.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    def test_weight_invalid_too_low(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_invalid_too_high(self):
        cost, date = calculate_delivery_cost(55.0, 100, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_boundary_min(self):
        cost, date = calculate_delivery_cost(2.0, 1, "обычный", False)
        self.assertEqual(cost, 205)

    def test_distance_boundary_max(self):
        cost, date = calculate_delivery_cost(2.0, 5000, "обычный", False)
        self.assertEqual(cost, 27200)

    def test_distance_invalid_too_low(self):
        cost, date = calculate_delivery_cost(2.0, 0, "обычный", False)
        self.assertEqual(cost, -1)

    def test_distance_invalid_too_high(self):
        cost, date = calculate_delivery_cost(2.0, 5500, "обычный", False)
        self.assertEqual(cost, -1)

    def test_invalid_package_type(self):
        cost, date = calculate_delivery_cost(2.0, 100, "элитный", False)
        self.assertEqual(cost, -1)

    def test_package_type_fragile(self):
        cost, date = calculate_delivery_cost(2.0, 100, "хрупкий", False)
        self.assertEqual(cost, 1000)

    def test_package_type_dangerous(self):
        cost, date = calculate_delivery_cost(2.0, 100, "опасный", False)
        self.assertEqual(cost, 1700)

    def test_weight_medium_range(self):
        cost, date = calculate_delivery_cost(10.0, 100, "обычный", False)
        self.assertEqual(cost, 840)

    def test_weight_heavy_range(self):
        cost, date = calculate_delivery_cost(20.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    def test_express_delivery_cost(self):
        cost, date = calculate_delivery_cost(2.0, 100, "обычный", True)
        self.assertEqual(cost, 980)

    def test_express_delivery_days_short(self):
        cost, date = calculate_delivery_cost(2.0, 100, "обычный", True)
        self.assertEqual(date, "2026-09-04")

    def test_express_delivery_days_long(self):
        cost, date = calculate_delivery_cost(2.0, 2000, "обычный", True)
        self.assertEqual(date, "2026-09-05")

    def test_delivery_date_standard_long(self):
        cost, date = calculate_delivery_cost(2.0, 1500, "обычный", False)
        self.assertEqual(date, "2026-09-06")

    def test_fragile_express_combination(self):
        cost, date = calculate_delivery_cost(2.0, 100, "хрупкий", True)
        self.assertEqual(cost, 1400)

    def test_dangerous_heavy_combination(self):
        cost, date = calculate_delivery_cost(25.0, 100, "опасный", False)
        self.assertEqual(cost, 2050)

if __name__ == '__main__':
    unittest.main()