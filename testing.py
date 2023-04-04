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
#from lsm6dsox import LSM6DSOX
import _thread

headlight = LightController(25)

while True:
    headlight.on()
    sleep_ms(100)
    headlight.off()
    sleep_ms(1000)