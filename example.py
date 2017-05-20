"""Example script.

Edit the I2C interface constant to match the one you have
connected the sensor to.
"""

from ina219 import INA219
from machine import I2C

# Edit to match interface the sensor is connect to (1 or 2).
I2C_INTERFACE_NO = 2
SHUNT_OHMS = 0.1

ina = INA219(SHUNT_OHMS, I2C(I2C_INTERFACE_NO))
ina.configure()
print("Bus Voltage: %.3f V" % ina.voltage())
print("Current: %.3f mA" % ina.current())
print("Power: %.3f mW" % ina.power())
