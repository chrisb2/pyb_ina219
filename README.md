# MicroPython Library for Voltage and Current Sensors Using the INA219

This MicroPython library for the [INA219](http://www.ti.com/lit/ds/symlink/ina219.pdf)
voltage, current and power monitor sensor from Texas Instruments. The intent of
the library is to make it easy to use the quite complex functionality of this
sensor.

The functionality is currently under development and is based on my [INA219 library for the Raspberry Pi](https://github.com/chrisb2/pi_ina219).

The library currently only supports _continuous_ reads of voltage and
power, but not _triggered_ reads.

The library supports the detection of _overflow_ in the current/power
calculations which results in meaningless values for these readings.

The low power mode of the INA219 is supported, so if only occasional
reads are being made in a battery based system, current consumption can
be minimised.

The library has been tested with the [Adafruit INA219 Breakout](https://www.adafruit.com/products/904) and the [pyboard](https://store.micropython.org/#/store), as well as a [NodeMCU (esp8266 12e) clone](http://www.dx.com/p/esp8266-esp-12e-development-board-serial-wi-fi-module-for-nodemcu-441215). and a [Lolin32 Lite (esp32)](https://wiki.wemos.cc/products:lolin32:lolin32_lite). For specific instructions for the esp8266 and esp32, see sub-directories.

If you successfully use this library with an WiPy, etc, please let me know.

## Usage

If you want to give it a try then copy _[ina219.py](https://raw.githubusercontent.com/chrisb2/pyb_ina219/master/ina219.py)_ and _[logging.py](https://raw.githubusercontent.com/micropython/micropython-lib/master/logging/logging.py)_ onto the flash drive of your pyboard, connect the sensor to the I2C(1) or I2C(2) interfaces on the pyboard,
then from a REPL prompt execute:

```python
from ina219 import INA219
from machine import I2C

I2C_INTERFACE_NO = 2
SHUNT_OHMS = 0.1

ina = INA219(SHUNT_OHMS, I2C(I2C_INTERFACE_NO))
ina.configure()
print("Bus Voltage: %.3f V" % ina.voltage())
print("Current: %.3f mA" % ina.current())
print("Power: %.3f mW" % ina.power())
```

Alternatively copy _[ina219.py](https://raw.githubusercontent.com/chrisb2/pyb_ina219/master/ina219.py)_, _[logging.py](https://raw.githubusercontent.com/micropython/micropython-lib/master/logging/logging.py)_
and _[example.py](https://raw.githubusercontent.com/chrisb2/pyb_ina219/master/example.py)_
to the flash drive and from the REPL prompt execute:

```python
execfile('example.py')
```

The address of the sensor unless otherwise specified is the default
of _0x40_.

Note that the bus voltage is that on the load side of the shunt resister,
if you want the voltage on the supply side then you should add the bus
voltage and shunt voltage together, or use the *supply_voltage()*
function.

### Simple - Auto Gain

This mode is great for getting started, as it will provide valid readings
until the device current capability is exceeded for the value of the
shunt resistor connected (3.2A for 0.1&Omega; shunt resistor). It does this by
automatically adjusting the gain as required until the maximum is reached,
when a _DeviceRangeError_ exception is thrown to avoid invalid readings being taken.

The downside of this approach is reduced current and power resolution.

```python
from ina219 import INA219
from ina219 import DeviceRangeError
from machine import I2C

I2C_INTERFACE_NO = 2
SHUNT_OHMS = 0.1

ina = INA219(SHUNT_OHMS, I2C(I2C_INTERFACE_NO))
ina.configure()

print("Bus Voltage: %.3f V" % ina.voltage())
try:
    print("Bus Current: %.3f mA" % ina.current())
    print("Power: %.3f mW" % ina.power())
    print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
except DeviceRangeError as e:
    # Current out of device range with specified shunt resister
    print e
```

### Advanced - Auto Gain, High Resolution

In this mode by understanding the maximum current expected in your system
and specifying this in the script you can achieve the best possible current
and power resolution. The library will calculate the best gain to achieve
the highest resolution based on the maximum expected current.

In this mode if the current exceeds the maximum specified, the gain will
be automatically increased, so a valid reading will still result, but at
a lower resolution.

As above when the maximum gain is reached, an exception is thrown to
avoid invalid readings being taken.

```python
from ina219 import INA219
from ina219 import DeviceRangeError
from machine import I2C

I2C_INTERFACE_NO = 2
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

ina = INA219(SHUNT_OHMS, I2C(I2C_INTERFACE_NO), MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

print("Bus Voltage: %.3f V" % ina.voltage())
try:
    print("Bus Current: %.3f mA" % ina.current())
    print("Power: %.3f mW" % ina.power())
    print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
except DeviceRangeError as e:
    # Current out of device range with specified shunt resister
    print e
```

### Advanced - Manual Gain, High Resolution

In this mode by understanding the maximum current expected in your system
and specifying this and the gain in the script you can always achieve the
best possible current and power resolution, at the price of missing current
and power values if a current overflow occurs.

```python
from ina219 import INA219
from ina219 import DeviceRangeError
from machine import I2C

I2C_INTERFACE_NO = 2
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

ina = INA219(SHUNT_OHMS, I2C(I2C_INTERFACE_NO), MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V, ina.GAIN_1_40MV)

print("Bus Voltage: %.3f V" % ina.voltage())
try:
    print("Bus Current: %.3f mA" % ina.current())
    print("Power: %.3f mW" % ina.power())
    print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
except DeviceRangeError as e:
    print("Current overflow")
```

### Sensor Address

The sensor address may be altered as follows:

```python
ina = INA219(SHUNT_OHMS, I2C(2), MAX_EXPECTED_AMPS, address=0x41)
```

### Low Power Mode

The sensor may be put in low power mode between reads as follows:

```python
ina.configure(ina.RANGE_16V)
while True:
    print("Voltage : %.3f V" % ina.voltage())
    ina.sleep()
    time.sleep(60)
    ina.wake()
```

Note that if you do not wake the device after sleeping, the value
returned from a read will be the previous value taken before sleeping.

## Functions

* `INA219()` constructs the class.
The arguments, are:
    * shunt_ohms: The value of the shunt resistor in Ohms (mandatory).
    * i2c: an instance of the I2C class from the _machine_ module, either
           _I2C(1)_ or _I2C(2)_ (mandatory).
    * max_expected_amps: The maximum expected current in Amps (optional).
    * address: The I2C address of the INA219, defaults to *0x40* (optional).
    * log_level: Set to _logging.INFO_ to see the detailed calibration
    calculations and _logging.DEBUG_ to see register operations (optional).
* `configure()` configures and calibrates how the INA219 will take measurements.
The arguments, which are all optional, are:
    * voltage_range: The full scale voltage range, this is either 16V or 32V,
    represented by one of the following constants (optional).
        * RANGE_16V: Range zero to 16 volts
        * RANGE_32V: Range zero to 32 volts (**default**). **Device only supports upto 26V.**
    * gain: The gain, which controls the maximum range of the shunt voltage,
        represented by one of the following constants (optional).
        * GAIN_1_40MV: Maximum shunt voltage 40mV
        * GAIN_2_80MV: Maximum shunt voltage 80mV
        * GAIN_4_160MV: Maximum shunt voltage 160mV
        * GAIN_8_320MV: Maximum shunt voltage 320mV
        * GAIN_AUTO: Automatically calculate the gain (**default**)
    * bus_adc: The bus ADC resolution (9, 10, 11, or 12-bit), or
        set the number of samples used when averaging results, represented by
        one of the following constants (optional).
        * ADC_9BIT: 9 bit, conversion time 84us.
        * ADC_10BIT: 10 bit, conversion time 148us.
        * ADC_11BIT: 11 bit, conversion time 276us.
        * ADC_12BIT: 12 bit, conversion time 532us (**default**).
        * ADC_2SAMP: 2 samples at 12 bit, conversion time 1.06ms.
        * ADC_4SAMP: 4 samples at 12 bit, conversion time 2.13ms.
        * ADC_8SAMP: 8 samples at 12 bit, conversion time 4.26ms.
        * ADC_16SAMP: 16 samples at 12 bit, conversion time 8.51ms
        * ADC_32SAMP: 32 samples at 12 bit, conversion time 17.02ms.
        * ADC_64SAMP: 64 samples at 12 bit, conversion time 34.05ms.
        * ADC_128SAMP: 128 samples at 12 bit, conversion time 68.10ms.
    * shunt_adc: The shunt ADC resolution (9, 10, 11, or 12-bit), or
        set the number of samples used when averaging results, represented by
        one of the following constants (optional).
        * ADC_9BIT: 9 bit, conversion time 84us.
        * ADC_10BIT: 10 bit, conversion time 148us.
        * ADC_11BIT: 11 bit, conversion time 276us.
        * ADC_12BIT: 12 bit, conversion time 532us (**default**).
        * ADC_2SAMP: 2 samples at 12 bit, conversion time 1.06ms.
        * ADC_4SAMP: 4 samples at 12 bit, conversion time 2.13ms.
        * ADC_8SAMP: 8 samples at 12 bit, conversion time 4.26ms.
        * ADC_16SAMP: 16 samples at 12 bit, conversion time 8.51ms
        * ADC_32SAMP: 32 samples at 12 bit, conversion time 17.02ms.
        * ADC_64SAMP: 64 samples at 12 bit, conversion time 34.05ms.
        * ADC_128SAMP: 128 samples at 12 bit, conversion time 68.10ms.
* `voltage()` Returns the bus voltage in volts (V).
* `supply_voltage()` Returns the bus supply voltage in volts (V). This
    is the sum of the bus voltage and shunt voltage. A _DeviceRangeError_
    exception is thrown if current overflow occurs.
* `current()` Returns the bus current in milliamps (mA).
	A _DeviceRangeError_ exception is thrown if current overflow occurs.
* `power()` Returns the bus power consumption in milliwatts (mW).
	A _DeviceRangeError_ exception is thrown if current overflow occurs.
* `shunt_voltage()` Returns the shunt voltage in millivolts (mV).
	A _DeviceRangeError_ exception is thrown if current overflow occurs.
* `current_overflow()` Returns 'True' if an overflow has
	occured. Alternatively handle the _DeviceRangeError_ exception
	as shown in the examples above.
* `sleep()` Put the INA219 into power down mode.
* `wake()` Wake the INA219 from power down mode.
* `reset()` Reset the INA219 to its default configuration.


## Performance

On v1.1 pyboard reading a bus voltage in a loop, a read occurred approximately
every 270&mu;s. Given that in _continuous_ mode a single 12-bit ADC
conversion takes 532&mu;s (p27 of the specification) each value returned
by the _voltage()_ function will likely be the result of a new conversion.

If multiple ADC conversions are configured (e.g. ADC_2SAMP, takes 1060&mu;s)
then the values returned by the _voltage()_ function will often be the result of
the same conversion and therefore identical.

## Debugging

Add the following to the imports
```Python
import logging
```
To understand the calibration calculation results and automatic gain increases, informational output can be enabled with:

```python
ina = INA219(SHUNT_OHMS, I2C(2), log_level=logging.INFO)
```

Detailed logging of device register operations can be enabled with:

```python
ina = INA219(SHUNT_OHMS, I2C(2), log_level=logging.DEBUG)
```

## Coding Standard

This library adheres to the *PEP8* standard and follows the *idiomatic*
style described in the book *Writing Idiomatic Python* by *Jeff Knupp*.
