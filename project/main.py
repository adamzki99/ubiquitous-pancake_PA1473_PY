#!/usr/bin/env pybricks-micropython
import sys
import pickup
#from pickup import pick_up_pallet
#from pickup import elevated_pick_up, elevated_pick_up





from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.parameters import Color

from drive import DriveRobot
from pickup import Crane
import misc



def main():
    ev3 = EV3Brick()

    # Initialize the motors.
    left_motor=Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])
    right_motor=Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])
    crane_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE, gears=[12,20])
    touch_sen = TouchSensor(Port.S1)
    color_sen = ColorSensor(Port.S3)
    ultra_sen = UltrasonicSensor(Port.S4)
    #crane_motor.dc(100)
    # Initialize the drive base.
    robot = DriveBase(left_motor, right_motor, wheel_diameter=47, axle_track=128)
    pallet = False
    col = None
    b = Crane(crane_motor,robot,touch_sen)
    a = DriveRobot(robot,color_sen,b)
   
    
    #ev3.speaker.say(" Hi my name is wall EEEEEEEEv3. lets begin")

    crane_motor.run_until_stalled(-50)
    #wait(3000)
    #b.pick_up_pallet()
    #wait(2000)
    #while True:
       # col = color_sen.color()
       # print(col)
      #  if col == Color.BROWN:
       #     print("hej")
       # else:
       #     print("fuck u")
    #a.drive2()
    #a.return_to_circle()
    #wait(2000)
    #a.drive2()
    #b.pick_up_pallet()
    
    b.elevated_pick_up()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())