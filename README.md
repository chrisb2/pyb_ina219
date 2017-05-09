# MicroPython Library for Voltage and Current Sensors Using the INA219

This MicroPython library for the [pyboard](https://store.micropython.org/#/store)
supports the [INA219](http://www.ti.com/lit/ds/symlink/ina219.pdf) voltage,
current and power monitor sensor from Texas Instruments. The intent of the library
is to make it easy to use the quite complex functionality of this sensor.

The functionality is currently under development and is based on my [INA219 library for the Raspberry Pi](https://github.com/chrisb2/pi_ina219). The README of the linked library describes
the functionality provided in detail.

If you want to give it a try then drop _ina219.py_ and _[logging.py](https://github.com/micropython/micropython-lib/blob/master/logging/logging.py)_
onto the flash drive of your pyboard, connect the sensor to the I2C(1) or I2C(2)
interfaces on the pyboard, then from a REPL prompt execute:

```python
from ina219 import INA219
from pyb import I2C
import logging
ina = INA219(0.1, I2C(2, I2C.MASTER), log_level=logging.INFO)
ina.configure()
print("Bus Voltage: %.3f V" % ina.voltage())
print("Bus Current: %.3f mA" % ina.current())
print("Power: %.3f mW" % ina.power())
```
