import unittest
from src.triangle import classify_triangle

class TestTriangle(unittest.TestCase):
    def test_equilateral(self):
        self.assertEqual(classify_triangle(3, 3, 3), "Equilateral")

    def test_isosceles_1(self):
        self.assertEqual(classify_triangle(5, 5, 3), "Isosceles")

    def test_isosceles_2(self):
        self.assertEqual(classify_triangle(3, 5, 5), "Isosceles")

    def test_isosceles_3(self):
        self.assertEqual(classify_triangle(5, 3, 5), "Isosceles")

    def test_scalene(self):
        self.assertEqual(classify_triangle(3, 4, 5), "Scalene")

    def test_not_triangle_inequality(self):
        self.assertEqual(classify_triangle(1, 2, 10), "Not a triangle")

    def test_not_triangle_zero(self):
        self.assertEqual(classify_triangle(0, 4, 5), "Not a triangle")

    def test_not_triangle_negative(self):
        self.assertEqual(classify_triangle(-3, 4, 5), "Not a triangle")

    def test_degenerate_triangle(self):
        self.assertEqual(classify_triangle(1, 2, 3), "Not a triangle")

    def test_large_scalene(self):
        self.assertEqual(classify_triangle(100, 101, 150), "Scalene")

if __name__ == '__main__':
    unittest.main()