import board
import busio
from adafruit_pca9685 import PCA9685
import yaml
import time
import os

config_filename = '../config/exomy.yaml'

def get_driving_pins():
    pin_list = []
    with open(config_filename, 'r') as file:
        param_dict = yaml.safe_load(file)

    exomy = param_dict['exomy']
    ros__parameters = exomy['ros__parameters']

    for key, value in ros__parameters.items():
        if 'pin_drive_' in key:
            print(key, value)
            pin_list.append(value)
    return pin_list

def get_drive_pwm_neutral():
    with open(config_filename, 'r') as file:
        param_dict = yaml.safe_load(file)

    exomy = param_dict['exomy']
    ros__parameters = exomy['ros__parameters']
    
    for key, value in ros__parameters.items():
        if 'drive_pwm_neutral' in key:
            return value

    default_value = 300
    print('The parameter drive_pwm_neutral could not be found in the exomy.yaml')
    print('It was set to the default value:', default_value)
    return default_value

if __name__ == "__main__":
    print(
        '''
$$$$$$$$\                     $$\      $$\           
$$  _____|                    $$$\    $$$ |          
$$ |      $$\   $$\  $$$$$$\  $$$$\  $$$$ |$$\   $$\ 
$$$$$\    \$$\ $$  |$$  __$$\ $$\$$\$$ $$ |$$ |  $$ |
$$  __|    \$$$$  / $$ /  $$ |$$ \$$$  $$ |$$ |  $$ |
$$ |       $$  $$<  $$ |  $$ |$$ |\$  /$$ |$$ |  $$ |
$$$$$$$$\ $$  /\$$\ \$$$$$$  |$$ | \_/ $$ |\$$$$$$$ |
\________|\__/  \__| \______/ \__|     \__| \____$$ |
                                           $$\   $$ |
                                           \$$$$$$  |
                                            \______/ 
        '''
    )
    print(
        '''
This script helps you to set the neutral values of PWM of the driving motors correctly.
It will send the intended signal for "not moving" to all the motors.
On each motor you have to turn the correction screw until the motor really stands still.
        '''
    )

    if not os.path.exists(config_filename):
        print("exomy.yaml does not exist. Finish config_motor_pins.py to generate it.")
        exit()

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pwm_frequency = 50.0  # Hz
    pca.frequency = pwm_frequency

    value = get_drive_pwm_neutral()
    pin_list = get_driving_pins()

    for pin in pin_list:
        pca.channels[pin].duty_cycle = int(value * 65535 / 4096)

    input('Press any button if you are done to complete configuration\n')

    for pin in pin_list:
        pca.channels[pin].duty_cycle = 0
