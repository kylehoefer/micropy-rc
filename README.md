# micropy-rc
MicroPython codebase to read/process PWM signals from RC receivers with micro-controllers to drive dynamic control for RC lighting, servos, and more.

##LATEST UPDATES:
- 3-30-23:
    - Initial Commit
    - Currently only supports microcontrollers using the RP2040
    - Absolute mess and hard-coded for my personal RX7 setup, needs to be cleaned up
        - Controls 2 headlights, 2 brakelights, a light-bucket servo, and a blue & orange LED for backfire
    - Recommended using Thonny for modifying/testing code

##Some basic functionality and possible examples which this codebase could be applied:
- Dynamic control (fade, blink, toggle) of LED's using throttle/steering/aux chn inputs
    - Toggle brake lights when throttle goes negative
    - Toggle reverse lights when throttle is negative for a certain amount of time
    - Toggle headlights
    - Toggle/fade blinkers based on left/right steering threshold
    - Toggle/fade backfire LED's at various rates depending on throttle input, allowing for realistic backfire effects
    - Use an RGB LED to make any light and color you like - could be used for underglow
    - Toggle hazards lights based on IMU input (e.g. sudden accelerometer decrease indicates a crash)
    - Place orange LED's near brake calipers, increase brightness depending on how long brakes have been pressed to "heat" them up
    - More to come!...Ideas welcome.
- Control of auxillary servos
    - Control a servo for light-bucket movement (e.g. RX7, Miata, etc.) raising/lowering/half-raising using your transmitter
    - Control a servo based on throttle input which is linked to your spoiler for active downforce control
    - Add a servo based on steering input to add a realist steering wheel effect
    - Add a servo based on brake input to trigger a scale e-brake in the cockpit
    - Add a servo based on gyro input attached to a GoPro in the cockpit, so the camera is always facing forward
    - More to come!...Ideas welcome.

##In-order short to long-term TODO's:
[] Clean-up the codebase
[] Add classes for increased modularity
[] Add endploint calibration procedure for throttle, steering, and aux RX channels
[] Add button and LED for mode-switching & calibration so no computer is needed
[] Add ability to plug in a small LCD screen to report mode/endpoints/calibration values
[] Continually add/simplify various functionality
[] Expand code to include ESP-based boards

## Some absurd future functionality which I personally think would be cool
- Add a tiny speaker inside your build, blast tunes or controller a synth in real-time using input to mimic realistic engine sounds!
- Phone app to control the system via Bluetooth
- Lambo. Doors.
- Roll the windows down
