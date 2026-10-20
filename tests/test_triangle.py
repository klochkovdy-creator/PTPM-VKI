import unittest
from src.triangle import classify_triangle


class TestTriangle(unittest.TestCase):
    def test_equilateral(self):
        self.assertEqual(classify_triangle(3, 3, 3), "Equilateral")

    def test_isosceles_first_two_equal(self):
        self.assertEqual(classify_triangle(5, 5, 3), "Isosceles")

    def test_isosceles_last_two_equal(self):
        self.assertEqual(classify_triangle(3, 5, 5), "Isosceles")

    def test_isosceles_first_and_last_equal(self):
        self.assertEqual(classify_triangle(5, 3, 5), "Isosceles")

    def test_scalene(self):
        self.assertEqual(classify_triangle(3, 4, 5), "Scalene")

    def test_not_triangle_inequality(self):
        self.assertEqual(classify_triangle(1, 2, 10), "Not a triangle")

    def test_not_triangle_zero_side(self):
        self.assertEqual(classify_triangle(0, 4, 5), "Not a triangle")

    def test_not_triangle_negative_side(self):
        self.assertEqual(classify_triangle(-3, 4, 5), "Not a triangle")

    def test_degenerate_triangle(self):
        self.assertEqual(classify_triangle(1, 2, 3), "Not a triangle")

    def test_large_scalene(self):
        self.assertEqual(classify_triangle(100, 101, 150), "Scalene")

    def test_degenerate_float_values(self):
        self.assertEqual(classify_triangle(0.1, 0.2, 0.3), "Not a triangle")

    def test_isosceles_with_float_sides(self):
        self.assertEqual(classify_triangle(0.5, 0.5, 0.3), "Isosceles")

    def test_equilateral_float(self):
        self.assertEqual(classify_triangle(1.5, 1.5, 1.5), "Equilateral")

    def test_not_triangle_equal_sides_violate_inequality(self):
        self.assertEqual(classify_triangle(5, 5, 10), "Not a triangle")

    def test_not_triangle_all_zero(self):
        self.assertEqual(classify_triangle(0, 0, 0), "Not a triangle")


if __name__ == '__main__':
    unittest.main()
