import unittest
from tests.i2c import I2C
from ina219 import INA219


class TestConstructor(unittest.TestCase):

    def test_default(self):
        self.ina = INA219(0.1, I2C(2))
        self.assertEqual(self.ina._shunt_ohms, 0.1)
        self.assertIsNotNone(self.ina._i2c)
        self.assertIsNone(self.ina._max_expected_amps)
        self.assertIsNone(self.ina._gain)
        self.assertFalse(self.ina._auto_gain_enabled)
        self.assertAlmostEqual(self.ina._min_device_current_lsb, 6.25e-6, 2)

    def test_with_max_expected_amps(self):
        self.ina = INA219(0.1, I2C(2), 0.4)
        self.assertEqual(self.ina._shunt_ohms, 0.1)
        self.assertIsNotNone(self.ina._i2c)
        self.assertEqual(self.ina._max_expected_amps, 0.4)


if __name__ == '__main__':
    unittest.main()
