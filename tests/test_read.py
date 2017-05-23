import unittest
from tests.i2c import I2C
from ina219 import INA219


class TestRead(unittest.TestCase):

    def setUp(self):
        self.i2c = I2C(2)
        self.ina = INA219(0.1, self.i2c)

    def test_read_32v(self):
        self._set_expected_bus_voltage_read(bytes([0xfa, 0x00]))

        self.assertEqual(self.ina.voltage(), 32)
        self._assert_read_bus_voltage_args()

    def test_read_16v(self):
        self._set_expected_bus_voltage_read(bytes([0x7d, 0x00]))

        self.assertEqual(self.ina.voltage(), 16)
        self._assert_read_bus_voltage_args()

    def test_read_4_808v(self):
        self._set_expected_bus_voltage_read(bytes([0x25, 0x92]))

        self.assertEqual(self.ina.voltage(), 4.808)
        self._assert_read_bus_voltage_args()

    def _set_expected_bus_voltage_read(self, bytes):
        self.i2c.set_readfrom_mem_result(self.ina.__REG_BUSVOLTAGE, bytes)

    def _assert_read_bus_voltage_args(self):
        self.assertEqual(self._get_read_args(self.ina.__REG_BUSVOLTAGE),
                         [self.ina.__ADDRESS, self.ina.__REG_BUSVOLTAGE, 2])

    def _get_read_args(self, register):
        return self.i2c.get_readfrom_mem_arguments(register)


if __name__ == '__main__':
    unittest.main()
