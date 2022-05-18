#!/usr/bin/env pybricks-micropython
import sys


import __init__

def main():


import __init__


from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.parameters import Color

from drive import DriveRobot
from pickup import Crane



def main():
    ev3 = EV3Brick()

    # Initialize the motors.
    left_motor=Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])
    right_motor=Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])

    crane_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])
    touch_sen = TouchSensor(Port.S1)
    color_sen = ColorSensor(Port.S3)
    ultra_sen = UltrasonicSensor(Port.S4)

    # Initialize the drive base.
    robot = DriveBase(left_motor, right_motor, wheel_diameter=47, axle_track=128)
    pallet = False
    col = None
    b = Crane(crane_motor,robot,touch_sen)
    a = DriveRobot(robot,color_sen,b, ultra_sen)

    return 0

if __name__ == '__main__':
    sys.exit(main())