import unittest

class XXXTestCase(unittest.TestCase):

    def setUp(self):
        # import class and prepare everything here.
        pass

    def test_YYY(self):
        # place your test case here
        a = 1
        self.assertEqual(a, 1)
    def test_calculation(self):
        pass
    def test_input(self):
        pass
if __name__ == '__main__':
    unittest.main()