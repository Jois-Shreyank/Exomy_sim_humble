import time
import sys
import board
import busio
from adafruit_pca9685 import PCA9685

'''
This script simply stops all the motors, in case they were left in a running state. 
'''

# Create the I2C bus interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create the PCA9685 class instance
pca = PCA9685(i2c)
# Set the PWM frequency to 50Hz
pca.frequency = 50

# Stop all motors by setting duty cycle to 0 for all 16 channels
for pin_number in range(16):
    pca.channels[pin_number].duty_cycle = 0
