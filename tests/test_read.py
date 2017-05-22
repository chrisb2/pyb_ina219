import unittest
from tests.i2c import I2C
from ina219 import INA219


class TestRead(unittest.TestCase):

    def setUp(self):
        self.ina = INA219(0.1, I2C(2))

    def test_read_32v(self):
        self.assertEqual(self.ina.voltage(), 32)


if __name__ == '__main__':
    unittest.main()
