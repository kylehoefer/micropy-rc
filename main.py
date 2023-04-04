# micropy-rc -- MicroPython-based controller for RC interfacing
# Copyright (C) 2023 Kyle Hoefer
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from machine import Pin, PWM, I2C
from utils.pwm import *
from utils.general import *
from utils.light import *
from lsm6dsox import LSM6DSOX
import _thread


def throttle_handler(sm):
    global throttle_result
    # x-reg counts down
    #print("Should be 1 : {}".format(sm0.get()))
    throttle_value = 0x100000000 - sm0.get()
    throttle_baton.acquire()
    throttle_result = throttle_value  # 0.5 us resolution, so expect 2000 to 4000
                    #                       for    1ms  to 2ms
    #print(throttle_result)
    throttle_baton.release()
    

def ch4_handler(sm):
    global ch4_result
    # x-reg counts down
    #print("Should be 2 : {}".format(sm1.get()))
    ch4_value = 0x100000000 - sm1.get()
    ch4_baton.acquire()
    ch4_result = ch4_value  # 0.5 us resolution, so expect 2000 to 4000
                    #                       for    1ms  to 2ms
    #print(ch4_result)
    ch4_baton.release()


'''INIT EXHAUST LEDS'''
exhaust_pin_blue = Pin(16, Pin.OUT)  # 6 is default onboard light
exhaust_led_blue = PWM(exhaust_pin_blue)
exhaust_led_blue.freq(50)
exhaust_pin_orange = Pin(17, Pin.OUT)  # 6 is default onboard light
exhaust_led_orange = PWM(exhaust_pin_orange)
exhaust_led_orange.freq(50)

'''INIT HEADLIGHT LEDS'''
headlight_L_pin = Pin(18, Pin.OUT)  # 6 is default onboard light
headlight_L_led = PWM(headlight_L_pin)
headlight_L_led.freq(50)

'''INIT TAIL LIGHTS'''
taillight_L_pin = Pin(19, Pin.OUT)
tailight_L_led = PWM(taillight_L_pin)
tailight_L_led.freq(50)

'''INIT THROTTLE INPUT'''
throttle_pin = Pin(25, Pin.IN, Pin.PULL_UP)
sm0 = rp2.StateMachine(0, pulsewidth, freq=4_000_000, in_base=throttle_pin, jmp_pin=throttle_pin)
throttle_result = 0
throttle_baton = _thread.allocate_lock()
sm0.irq(throttle_handler)
sm0.active(1)

'''INIT CH4 INPUT'''
ch4_pin = Pin(21, Pin.IN, Pin.PULL_UP)
sm1 = rp2.StateMachine(4, pulsewidth2, freq=4_000_000, in_base=ch4_pin, jmp_pin=ch4_pin)
ch4_result = 0
ch4_baton = _thread.allocate_lock()
sm1.irq(ch4_handler)
sm1.active(1)

'''INIT HEADLIGHT SERVO'''
light_servo_pin = Pin(5, Pin.OUT)
light_servo = PWM(light_servo_pin)
light_servo.freq(50)
light_servo.duty_u16(1000)    #  RESET IT ON STARTUP

'''INIT IMU'''
#lsm_i2c = I2C(0, scl=Pin(13), sda=Pin(12))
#lsm = LSM6DSOX(lsm_i2c, gyro_odr=26, accel_odr=26, gyro_scale=250, accel_scale=4)

'''INIT OTHER VALS'''
imu_accel_old = None
ch4_old = 0

while (True):

    # Get throttle & ch4 pwm values and convert to percentage values
    throttle_pwm = throttle_result
    throttle_perc = throttle_2_perc(throttle_pwm)
    ch4_pwm = ch4_result
    ch4_perc = ch4_2_perc(ch4_pwm)

    
    # Light bucket controller
    if ch4_perc != ch4_old:
        if ch4_perc > 5:
            lights_on(headlight_L_led)
        else:
            lights_off(headlight_L_led)
        perc_2_lightbuck(ch4_perc, light_servo)
    ch4_old = ch4_perc
    

    # Backfire if throttle is past this percentage
    if throttle_perc > 45:
        blue_backfire(exhaust_led_blue)
        single_backfire(exhaust_led_orange)
    
    # Trigger tailights when braking or reversing
    if throttle_perc < -2:
        lights_on(tailight_L_led)
    else:
        lights_off(tailight_L_led)
        
    #if imu_accel != imu_accel_old:
        #print(imu_accel)
    #imu_accel_old = imu_accel

    time.sleep(0.01)

