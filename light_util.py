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
import random as rnd
from ulab import numpy as np
import rp2
from pwm_util import perc_to_duty


def double_backfire(led):
    # Scale down
    for i in range(100, 1, -1):
        led.duty_u16(perc_to_duty(i))
        sleep_ms(1)

    # Pause between fires
    pause_time = rnd.choice(range(70, 120, 10))
    sleep_ms(pause_time)  # Pause

    #  Scale down again
    secondary_fire_decay = rnd.choice(np.arange(1.0, 5.0, 0.2))
    brightness = rnd.randrange(20, 70, 1)
    for i in range(brightness, 1, -1):
        led.duty_u16(perc_to_duty(i))
        sleep_ms(secondary_fire_decay)

    # Return to zero
    led.duty_u16(perc_to_duty(0))
    return


def single_backfire(led):
    decay_time = rnd.choice(np.arange(0.2, 2.0, 0.1))
    brightness = rnd.randrange(20, 100, 5)

    # Scale up
    #for i in range(0, brightness, -1):
        #led.duty_u16(perc_to_duty(i))
        #sleep_ms(decay_time / 1.5)
    led.duty_u16(perc_to_duty(brightness))


    # Scale down
    for i in range(brightness, 1, -1):
        led.duty_u16(perc_to_duty(i))
        sleep_ms(decay_time)

    # Return to zero
    led.duty_u16(perc_to_duty(0))
    return


def tailights_on(left):
    left.duty_u16(perc_to_duty(100))
    #right.duty_u16(perc_to_duty(100))
    return
    
    
def tailights_off(left):
    left.duty_u16(perc_to_duty(0))
    #right.duty_u16(perc_to_duty(99))
    return


def blue_backfire(led):
    decay_time = rnd.choice(np.arange(0.01, 0.1, 0.2))
    brightness = rnd.randrange(20, 80, 5)

    led.duty_u16(perc_to_duty(brightness))
    sleep_ms(20)

    # Return to zero
    led.duty_u16(perc_to_duty(0))
    return
