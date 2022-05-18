# Pybricks imports
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from misc import notify_operation, speak

    
class Crane:
    def __init__(self,crane, robot, touch_sen) :
        self.m_crane = crane
        self.m_robot = robot
        self.m_touch_sen = touch_sen
        self.pallet_on = False

    def pick_up_pallet(self):
        """The function makes the robot pick upp a pallet."""
        #robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
        notify_operation("Pick up pallet")
        #self.m_crane.dc(100)
        i = 0
        while (i < 10):
            if self.m_touch_sen.pressed() is False:
                self.m_robot.straight(50)
            else:
                break
            i = i + 1
        if self.m_touch_sen.pressed() is False:
            self.pallet_on = False
            speak("Pickup failed")
            return False
        self.m_robot.stop()
        self.m_crane.dc(100)
        self.m_crane.run(-100)
        wait(750)
        self.m_crane.hold()
        wait(500)
        self.m_robot.straight(-i*50)
        self.pallet_on = True
        return True

    def elevated_pick_up(self):
        """lifts the crane to pick upp a pallet"""
        self.m_crane.run_until_stalled(50)
        wait(1000)
        self.m_crane.stop()
        self.m_crane.run(-100)
        wait(650)
        self.m_crane.hold()
        return self.pick_up_pallet()
    
    def abort_collect(self):
        self.m_crane.run_until_stalled(50)
        wait(1000)
        self.m_robot.straight(-500)
        speak("Aborting")



    





