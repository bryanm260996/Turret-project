# bno055_test.py Simple test program for MicroPython bno055 driver

# Copyright (c) Peter Hinch 2019
# Released under the MIT licence.

import machine
import time
from bno055 import *
# Tested configurations
# Pyboard hardware I2C
#  i2c = machine.I2C(1)

# Pico: hard I2C doesn't work without this patch
# https://github.com/micropython/micropython/issues/8167#issuecomment-1013696765
i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))  # EIO error almost immediately

# All platforms: soft I2C requires timeout >= 1000μs
# i2c = machine.SoftI2C(sda=machine.Pin(16), scl=machine.Pin(17), timeout=1_000)
# ESP8266 soft I2C
# i2c = machine.SoftI2C(scl=machine.Pin(2), sda=machine.Pin(0), timeout=100_000)
# ESP32 hard I2C
# i2c = machine.I2C(1, scl=machine.Pin(21), sda=machine.Pin(23))
imu = BNO055(i2c)
calibrated = False
while True:
    time.sleep(1)
    if not calibrated:
        calibrated = imu.calibrated()
        print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))

    print('Gyro      x {:5.0f}     y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))

