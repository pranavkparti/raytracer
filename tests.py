import unittest
from vector import Vector

class TestVectors(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector(1.0, 2.0, -2.0)
        self.v2 = Vector(3.0, 6.0, 9.0)

    def test_magnitude(self):
        self.assertEqual(self.v1.magnitude(), 3.0)

    def test_addition(self):
        sum = self.v1 + self.v2
        self.assertEqual(getattr(sum, 'x'), 4.0)
    
    def test_subtraction(self):
        diff = self.v1 - self.v2
        self.assertEqual(getattr(diff, 'x'), -2.0)

    def test_multiplication(self):
        lproduct = self.v2 * 2
        rproduct = 2 * self.v2
        self.assertEqual(getattr(lproduct, 'x'), 6.0)
        self.assertEqual(getattr(rproduct, 'x'), getattr(lproduct, 'x'))
    
    def test_division(self):
        div = self.v2 / 2
        self.assertEqual(getattr(div, 'y'), 3.0)

if __name__ == '__main__':
    unittest.main()