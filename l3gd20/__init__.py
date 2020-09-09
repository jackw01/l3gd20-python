# Copyright 2020 jackw01. Released under the MIT license.
__version__ = "1.0.0"

import smbus
import struct
import time

L3GD20_ADDRESS = 0x6B # 1101011x
L3GD20_REGISTER_WHO_AM_I            = 0x0F
L3GD20_REGISTER_CTRL_REG1           = 0x20
L3GD20_REGISTER_CTRL_REG2           = 0x21
L3GD20_REGISTER_CTRL_REG3           = 0x22
L3GD20_REGISTER_CTRL_REG4           = 0x23
L3GD20_REGISTER_CTRL_REG5           = 0x24
L3GD20_REGISTER_REFERENCE           = 0x25
L3GD20_REGISTER_OUT_TEMP            = 0x26
L3GD20_REGISTER_STATUS_REG          = 0x27
L3GD20_REGISTER_OUT_X_L             = 0x28
L3GD20_REGISTER_OUT_X_H             = 0x29
L3GD20_REGISTER_OUT_Y_L             = 0x2A
L3GD20_REGISTER_OUT_Y_H             = 0x2B
L3GD20_REGISTER_OUT_Z_L             = 0x2C
L3GD20_REGISTER_OUT_Z_H             = 0x2D
L3GD20_REGISTER_FIFO_CTRL_REG       = 0x2E
L3GD20_REGISTER_FIFO_SRC_REG        = 0x2F
L3GD20_REGISTER_INT1_CFG            = 0x30
L3GD20_REGISTER_INT1_SRC            = 0x31
L3GD20_REGISTER_TSH_XH              = 0x32
L3GD20_REGISTER_TSH_XL              = 0x33
L3GD20_REGISTER_TSH_YH              = 0x34
L3GD20_REGISTER_TSH_YL              = 0x35
L3GD20_REGISTER_TSH_ZH              = 0x36
L3GD20_REGISTER_TSH_ZL              = 0x37
L3GD20_REGISTER_INT1_DURATION       = 0x38

RANGE_250DPS = 0x00
RANGE_500DPS = 0x10
RANGE_2000DPS = 0x20

L3GD20_DPS_PER_LSB = {
    RANGE_250DPS: 0.00875,
    RANGE_500DPS: 0.0175,
    RANGE_2000DPS: 0.07,
}

class L3GD20(object):
    'L3GD20 3-axis gyro'

    def __init__(self, i2c, hires=True):
        'Initialize the sensor'
        self._bus = i2c
        self._orientation = None

        # Enable the gyro - reset and set to normal mode with all 3 channels
        # Data rate left at 00 (12.5hz) but it works at higher speeds?
        self._bus.write_i2c_block_data(L3GD20_ADDRESS,
                                       L3GD20_REGISTER_CTRL_REG1,
                                       [0b00000000])
        self._bus.write_i2c_block_data(L3GD20_ADDRESS,
                                       L3GD20_REGISTER_CTRL_REG1,
                                       [0b00001111])

        # Set range
        self.set_range(RANGE_250DPS)

    def set_range(self, new_range):
        'Set range'
        self._range = new_range
        self._dps_per_lsb = L3GD20_DPS_PER_LSB[self._range]
        self._bus.write_i2c_block_data(L3GD20_ADDRESS,
                                       L3GD20_REGISTER_CTRL_REG4,
                                       [self._range])

    def read(self):
        'Read raw angular velocity values in degrees/second'
        # Read as signed 16-bit little endian values
        gyro_bytes = self._bus.read_i2c_block_data(L3GD20_ADDRESS,
                                                   L3GD20_REGISTER_OUT_X_L | 0x80,
                                                   6)
        gyro_raw = struct.unpack('<hhh', bytearray(gyro_bytes))

        return (
            gyro_raw[0] * self._dps_per_lsb,
            gyro_raw[1] * self._dps_per_lsb,
            gyro_raw[2] * self._dps_per_lsb,
        )

def _test():
    i2c_channel = 1
    bus = smbus.SMBus(i2c_channel)
    device = L3GD20(bus)
    while True:
        data = device.read()
        print([round(v, 2) for v in data])
        time.sleep(0.1)
