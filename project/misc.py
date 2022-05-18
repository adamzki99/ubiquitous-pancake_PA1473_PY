from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.parameters import Color


ev3 = EV3Brick()

def notify_operation(current_operation):
    """displays current operation on the display screen and prints a status message in python terminal"""
    ev3.screen.draw_text(40, 50, current_operation)
    ev3.speaker.say("performing" + current_operation)
    print("current operation is" + current_operation)


def speak(line):
    if(line == "Beep"):
        ev3.speaker.beep()
    else:
        ev3.speaker.say(line)

def get_colour(color_sen):
    while(True):
        print(color_sen.rgb())
        wait(5000)