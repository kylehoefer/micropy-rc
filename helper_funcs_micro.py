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


@rp2.asm_pio()
def pulsewidth():
    wrap_target()
    wait(1, pin, 0)                       # 0
    set(x, 0)                             # 1
    jmp(x_dec, "3")                       # 2
    label("3")
    jmp(x_dec, "4")                       # 3
    label("4")
    jmp(pin, "3")                         # 4
    mov(isr, x)                           # 5
    push(isr, block)                      # 6
    irq( 0)                               # 7
    wrap()
    
    
@rp2.asm_pio()
def pulsewidth2():
    wrap_target()
    wait(1, pin, 1)                       # 0
    set(y, 1)                             # 1
    jmp(y_dec, "3")                       # 2
    label("3")
    jmp(y_dec, "4")                       # 3
    label("4")
    jmp(pin, "3")                         # 4
    mov(isr, y)                           # 5
    push(isr, block)                      # 6
    irq( 1)                               # 7
    wrap()


def perc_to_duty(percent):
    duty = int((percent / 100.0) * 65535.0)
    return duty


def sleep_ms(ms):
    time.sleep(ms / 1000)
    return


def servo_duty_cycle(pulse_ms, frequency=50):
    period_ms = 1.0 / frequency * 1000.0
    duty_cycle = int(pulse_ms / (period_ms / 65535.0))
    return duty_cycle


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


def throttle_2_perc(throttle_pwm):
    dec = (throttle_pwm - 3042) / 895
    perc = int(dec * 100)
    return perc


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
