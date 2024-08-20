import time
import sys
import board
import busio
from adafruit_pca9685 import PCA9685

'''
This script helps to test PWM motors with the Adafruit PCA9685 board 
Example usage:
python motor_test.py 3

Performs a motor test for the motor connected to pin 3 of the PWM board
'''

# Check if the pin number is given as an argument
if len(sys.argv) < 2:
    print('You must give the pin number of the motor to be tested as argument.')
    print('E.g: python motor_test.py 3')
    print('Tests the motor connected to pin 3.')
    exit()

# Set the pin of the motor
pin = int(sys.argv[1])
print('Pin: ' + str(pin))

# Create the I2C bus interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create the PCA9685 class instance
pca = PCA9685(i2c)
# Set the PWM frequency to 50Hz
pca.frequency = 50

# The cycle is the inverted frequency converted to milliseconds
pwm_frequency = 50.0 # Hz
cycle = 1.0 / pwm_frequency * 1000.0 # ms

selection = ''

while selection != '0':

    print("What do you want to test?")
    print("1. Min to Max oscillation")
    print('2. Incremental positioning')
    print('0. Abort')
    selection = input()

    if int(selection) == 1:
        min_t = 0.5 # ms
        max_t = 2.5 # ms
        mid_t = (min_t + max_t) / 2

        print("pulsewidth_min = {:.2f}, pulsewidth_max = {:.2f}".format(min_t, max_t))

        # *_dc is the percentage of a cycle the signal is on
        min_dc = min_t / cycle
        max_dc = max_t / cycle
        mid_dc = mid_t / cycle
        
        dc_list = [min_dc, mid_dc, max_dc, mid_dc]
        for dc in dc_list:
            pca.channels[pin].duty_cycle = int(dc * 65535.0)
            time.sleep(2.0)
            
    if int(selection) == 2:
        curr_t = 1.5 # ms
        curr_dc = curr_t / cycle
        step_size = 0.1 # ms
        step_size_scaling = 0.2
        
        dc_selection = ''
        
        while dc_selection != '0':
            dc_selection = input('a-d: change pulsewidth | w-s: change step size | 0: back to menu\n')
            if dc_selection == 'a':
                curr_t -= step_size
            elif dc_selection == 'd':
                curr_t += step_size
            elif dc_selection == 's':
                step_size *= (1 - step_size_scaling)
            elif dc_selection == 'w':
                step_size *= (1 + step_size_scaling)

            curr_dc = curr_t / cycle
            curr_pwm = int(curr_dc * 65535.0)
            print("t_current:\t{0:.4f} [ms]\nstep_size:\t{1:.4f} [ms]\ncurr_pwm: {2:.2f}".format(curr_t, step_size, curr_pwm))
                        
            pca.channels[pin].duty_cycle = curr_pwm

# Reset the PWM signal
pca.channels[pin].duty_cycle = 0
