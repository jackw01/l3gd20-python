# l3gd20-python
Python library for the L3GD20 I2C 3-axis gyroscope

## Usage
1. Install the Python `smbus` module for your platform (`sudo apt install python-smbus` for Debian or Ubuntu Linux)
2. `pip install l3gd20-python`
3. `sudo l3gd20_test`

## Example Code
```python
import time
import smbus
import l3gd20

i2c_channel = 1
bus = smbus.SMBus(i2c_channel)

# Will raise OSError if device is not connected
device = l3gd20.L3GD20(bus)

# Set range, 250 degrees/second is default
# Supported:
# RANGE_250DPS
# RANGE_500DPS
# RANGE_2000DPS
device.set_range(l3gd20.RANGE_250DPS)

# Wait for gyro to stabilize
time.sleep(0.5)

while True:
    # Returns x,y,z tuple with values in degrees/second
    data = device.read()
    print([round(v, 2) for v in data])
    time.sleep(0.1)
```
