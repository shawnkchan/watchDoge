# import gpiozero
# import time
# import sys
# from gpiozero import OutputDevice as stepper


# def rotate_motor(signal):
#     IN1 = stepper(17)
#     IN2 = stepper(18)
#     IN3 = stepper(27)
#     IN4 = stepper(22)
#     stepPins = [IN1, IN2, IN3, IN4]  # Motor GPIO pins</p><p>
#     stepDir = -1        # Set to 1 for clockwise
#     # Set to -1 for anti-clockwise
#     mode = 1            # mode = 1: Low Speed ==> Higher Power
#     # mode = 0: High Speed ==> Lower Power
#     if mode:              # Low Speed ==> High Power
#         seq = [[1, 0, 0, 1],  # Define step sequence as shown in manufacturers datasheet
#                [1, 0, 0, 0],
#                [1, 1, 0, 0],
#                [0, 1, 0, 0],
#                [0, 1, 1, 0],
#                [0, 0, 1, 0],
#                [0, 0, 1, 1],
#                [0, 0, 0, 1]]
#     else:                    # High Speed ==> Low Power
#         seq = [[1, 0, 0, 0],  # Define step sequence as shown in manufacturers datasheet
#                [0, 1, 0, 0],
#                [0, 0, 1, 0],
#                [0, 0, 0, 1]]
#     stepCount = len(seq)

#     waitTime = 0.004
#     stepCounter = 0

#     if signal:                       # Start main loop
#         for pin in range(0, 4):
#             xPin = stepPins[pin]          # Get GPIO
#             if seq[stepCounter][pin] != 0:
#                 xPin.on()
#             else:
#                 xPin.off()
#         stepCounter += stepDir
#         if (stepCounter >= stepCount):
#             stepCounter = 0
#         if (stepCounter < 0):
#             stepCounter = stepCount+stepDir
#         time.sleep(waitTime)     # Wait before moving on

#     return 1


import time
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib


def turn_motor(is_ccwise):
    my_motor = RpiMotorLib.BYJMotor("MyMotor", "28BYJ")
    
    my_motor.motor_run(
        gpiopins=[17, 18, 27, 22], 
        wait=.001, 
        steps=50, 
        ccwise=is_ccwise, 
        verbose=False, 
        steptype="half", # has 512 steps for 360 degrees
        initdelay=0.05
    )

    GPIO.cleanup()
    return
