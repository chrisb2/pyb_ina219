# Using the Library on an ESP8266

On the NodeMCU clone I used to test with I got an out of memory error when trying to import the _ina219_ module, this is due to there being insufficient RAM to compile this module to byte code. If you encounter this issue then you can use the frozen byte code as explained below.

## Usage

This is an example script:

```python
from machine import Pin, I2C
from ina219 import INA219
from logging import INFO

SHUNT_OHMS = 0.1

i2c = I2C(-1, Pin(5), Pin(4))
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)
ina.configure()

print("Bus Voltage: %.3f V" % ina.voltage())
print("Current: %.3f mA" % ina.current())
print("Power: %.3f mW" % ina.power())
```

## Frozen Byte Code

This directory contains two frozen byte code modules; _ina219.mpy_ and _logging.mpy_ compiled with v1.9.1 of the [micropython esp8266 tool chain](https://github.com/micropython/micropython/tree/master/ports/esp8266). Copy these to the flash drive of your esp8266 in place of the source code modules, _logging.mpy_ is only required if you want to see log output. Restart the esp8266.