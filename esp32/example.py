from machine import Pin, I2C
from ina219 import INA219
from logging import INFO

SHUNT_OHMS = 0.1

i2c = I2C(-1, Pin(17), Pin(16))
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)
ina.configure()

print("Bus Voltage: %.3f V" % ina.voltage())
print("Current: %.3f mA" % ina.current())
print("Power: %.3f mW" % ina.power())