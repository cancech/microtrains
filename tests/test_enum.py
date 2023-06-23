import unittest
import src.enum as enum

class TestEnum(unittest.TestCase):
    def testEnnum(self):
            tmpEnum = enum.create('A', 'B', 'C', 'D', 'E')
            self.assertEqual(0, tmpEnum.A)
            self.assertEqual(1, tmpEnum.B)
            self.assertEqual(2, tmpEnum.C)
            self.assertEqual(3, tmpEnum.D)
            self.assertEqual(4, tmpEnum.E)

if __name__ == '__main__':
    unittest.main()