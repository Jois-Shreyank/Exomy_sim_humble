#!/usr/bin/env python

import time
import board
import busio
from adafruit_pca9685 import PCA9685

class Motors():
    '''
    Motors class contains all functions to control the steering and driving motors.
    '''

    # Define wheel names
    FL, FR, CL, CR, RL, RR = range(0, 6)

    # Motor commands are assuming positive=driving_forward, negative=driving_backwards.
    # The driving direction of the left side has to be inverted for this to apply to all wheels.
    wheel_directions = [-1, 1, -1, 1, -1, 1]

    # 1 fl-||-fr 2
    #      ||
    # 3 cl-||-cr 4
    # 5 rl====rr 6

    def __init__(self, parameters):

        # Dictionary containing the pins of all motors
        self.pins = {
            'drive': {},
            'steer': {}
        }

        # Set variables for the GPIO motor pins
        self.pins['drive'][self.FL] = parameters['pin_drive_fl']
        self.pins['steer'][self.FL] = parameters['pin_steer_fl']

        self.pins['drive'][self.FR] = parameters['pin_drive_fr']
        self.pins['steer'][self.FR] = parameters['pin_steer_fr']

        self.pins['drive'][self.CL] = parameters['pin_drive_cl']
        self.pins['steer'][self.CL] = parameters['pin_steer_cl']

        self.pins['drive'][self.CR] = parameters['pin_drive_cr']
        self.pins['steer'][self.CR] = parameters['pin_steer_cr']

        self.pins['drive'][self.RL] = parameters['pin_drive_rl']
        self.pins['steer'][self.RL] = parameters['pin_steer_rl']

        self.pins['drive'][self.RR] = parameters['pin_drive_rr']
        self.pins['steer'][self.RR] = parameters['pin_steer_rr']

        # PWM characteristics
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pwm = PCA9685(i2c)
        self.pwm.frequency = 50  # Hz

        self.steering_pwm_neutral = [None] * 6

        self.steering_pwm_neutral[self.FL] = parameters['steer_pwm_neutral_fl']
        self.steering_pwm_neutral[self.FR] = parameters['steer_pwm_neutral_fr']
        self.steering_pwm_neutral[self.CL] = parameters['steer_pwm_neutral_cl']
        self.steering_pwm_neutral[self.CR] = parameters['steer_pwm_neutral_cr']
        self.steering_pwm_neutral[self.RL] = parameters['steer_pwm_neutral_rl']
        self.steering_pwm_neutral[self.RR] = parameters['steer_pwm_neutral_rr']
        self.steering_pwm_range = parameters['steer_pwm_range']

        self.driving_pwm_neutral = parameters['drive_pwm_neutral']
        self.driving_pwm_range = parameters['drive_pwm_range']

        # Set the GPIO to software PWM at 'Frequency' Hertz
        self.driving_motors = [None] * 6
        self.steering_motors = [None] * 6

        # Set steering motors to neutral values (straight)
        for wheel_name, motor_pin in self.pins['steer'].items():
            self.pwm.channels[motor_pin].duty_cycle = int(self.steering_pwm_neutral[wheel_name] * 65535 / 4096)
            time.sleep(0.1)

        self.wiggle()

    def wiggle(self):
        # Wiggle the two front wheels on startup to confirm functionality
        time.sleep(0.1)
        self.pwm.channels[self.pins['steer'][self.FL]].duty_cycle = int(
            (self.steering_pwm_neutral[self.FL] + self.steering_pwm_range * 0.3) * 65535 / 4096)
        time.sleep(0.1)
        self.pwm.channels[self.pins['steer'][self.FR]].duty_cycle = int(
            (self.steering_pwm_neutral[self.FR] + self.steering_pwm_range * 0.3) * 65535 / 4096)
        time.sleep(0.3)
        self.pwm.channels[self.pins['steer'][self.FL]].duty_cycle = int(
            (self.steering_pwm_neutral[self.FL] - self.steering_pwm_range * 0.3) * 65535 / 4096)
        time.sleep(0.1)
        self.pwm.channels[self.pins['steer'][self.FR]].duty_cycle = int(
            (self.steering_pwm_neutral[self.FR] - self.steering_pwm_range * 0.3) * 65535 / 4096)
        time.sleep(0.3)
        self.pwm.channels[self.pins['steer'][self.FL]].duty_cycle = int(self.steering_pwm_neutral[self.FL] * 65535 / 4096)
        time.sleep(0.1)
        self.pwm.channels[self.pins['steer'][self.FR]].duty_cycle = int(self.steering_pwm_neutral[self.FR] * 65535 / 4096)
        time.sleep(0.3)

    def setSteering(self, steering_command):
        # Loop through pin dictionary. The items key is the wheel_name and the value the pin.
        for wheel_name, motor_pin in self.pins['steer'].items():
            duty_cycle = int(
                (self.steering_pwm_neutral[wheel_name] + steering_command[wheel_name] / 90.0 * self.steering_pwm_range) * 65535 / 4096)
            self.pwm.channels[motor_pin].duty_cycle = duty_cycle

    def setDriving(self, driving_command):
        # Loop through pin dictionary. The items key is the wheel_name and the value the pin.
        for wheel_name, motor_pin in self.pins['drive'].items():
            duty_cycle = int(
                (self.driving_pwm_neutral + driving_command[wheel_name] / 100.0 * self.driving_pwm_range * self.wheel_directions[wheel_name]) * 65535 / 4096)
            self.pwm.channels[motor_pin].duty_cycle = duty_cycle

    def stopMotors(self):
        # Set driving wheels to neutral position to stop them
        duty_cycle = int(self.driving_pwm_neutral * 65535 / 4096)

        for wheel_name, motor_pin in self.pins['drive'].items():
            self.pwm.channels[motor_pin].duty_cycle = duty_cycle
