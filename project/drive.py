


from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.parameters import Color
from misc import notify_operation, speak
import pickup
import time


class DriveRobot:

    def __init__(self, drive_base, color_sen, crane, ultra_sen):
        self.m_drive_base = drive_base
        self.m_color_sen = color_sen
        self.m_ultra_sen = ultra_sen
        self.m_crane = crane

        self.curr_col = Color.BLUE
        self.change_col = Color.BROWN
        self.second_change_col = Color.RED
        
    def drive(self, in_time=0):
        notify_operation("Driving")
        start_time = time.time()
        breaktime = True
        while ((time.time()-start_time) < in_time or in_time == 0 or breaktime):
            turned = -1
            self.avoid_collision()
            self.m_drive_base.drive(50, 0)
            # wait(500)
            while self.m_color_sen.color() in [Color.WHITE, Color.YELLOW]:
                turned = -1.75*turned
                self.m_drive_base.stop()
                self.m_drive_base.turn(turned)
                if turned > 180:
                    self.emergency_mode("Finding path")
                    self.m_drive_base.turn(-turned)
                    self.m_drive_base.straight(-100)

            if(self.m_color_sen.color() not in [self.change_col, self.curr_col, Color.BLACK, Color.YELLOW, Color.WHITE]):
                self.m_drive_base.straight(20)

            if(self.m_color_sen.color() == Color.BLACK):
                speak("Arrived at Warehouse")
                quit

            if(self.m_crane.pallet_on and not self.m_crane.m_touch_sen.pressed()):
                self.emergency_mode("Pallet")
                breaktime = not breaktime

            if(self.m_color_sen.color() == self.change_col):
                self.curr_col = self.change_col                
                self.change_col = self.second_change_col
                self.second_change_col = None
                speak("Left area")
                speak("Beep")

    def avoid_collision(self):
        notify_operation("Avoid Collision")
        start_time = time.time()
        while(self.m_ultra_sen.distance() < 100):
            self.m_drive_base.stop()
            print(start_time - time.time())
            if( time.time()- start_time > 10):
                speak("Item misplaced!")
                self.emergency_mode()

    def set_color(self, str_color):
        color_dict = {
            "brown": Color.BROWN,
            "blue": Color.BLUE,
            "red": Color.RED,

            "green": Color.GREEN, }
        self.curr_col = color_dict[str_color]

    def set_color_change(self, str_color_change, col_change2 = "brown"):

        color_dict = {
            "brown": Color.BROWN,
            "blue": Color.BLUE,
            "red": Color.RED,
            "green": Color.GREEN, }
        self.change_col = color_dict[str_color_change]
        self.second_change_col = color_dict[col_change2]

    def return_to_circle(self):
        self.set_color_change("brown")
    
    def select_area(self, area):
        location_dict = {
            "Blue Warehouse": "blue",
            "Red Warehouse": "red",
            "Pickup and delivery": "green" }
        self.set_color_change("brown",location_dict[area])

    def warehouse_drive(self, in_time=10, ):
        '''Help function for finding  crates in warehouses'''
        start_time = time.time()
        print((time.time()-start_time))
        while((time.time()-start_time) < in_time or in_time == 0):
            turned = -1
            self.m_drive_base.drive(50, 0)
            deviation = self.m_color_sen.reflection() - 20

            while (deviation < 20):
                self.m_drive_base.stop()
                turned = -2*turned
                self.m_drive_base.turn(turned)
                deviation = self.m_color_sen.reflection() - 20
                if(turned > 180):
                    quit
                    self.emergency_mode()

    def red_warehouse_adjust(self, part):
        notify_operation("Red warejouse adjust")
        self.m_drive_base.drive(60, 0)
        wait(4000)
        self.m_drive_base.drive(30, 130)
        wait(1000)
        counter = 0
        while(counter != part):
            self.m_drive_base.drive(50, 0)

            if(self.m_color_sen.color() != Color.YELLOW):
                wait(250)

            if(self.m_color_sen.color() == Color.YELLOW):
                counter = counter+1
                while(self.m_color_sen.color() == Color.YELLOW and counter != part):
                    wait(1000)
                print(counter)
        self.m_drive_base.drive(-30, -200)
        wait(500)
        self.warehouse_drive(13)
        self.m_crane.pick_up_pallet()
        self.m_drive_base.drive(-50, 0)
        while(self.m_color_sen.color() != Color.WHITE):
            wait(500)
        self.m_drive_base.drive_time(0, -360, 5000)
   
   
    def blue_warehouse_adjust(self, part):
        notify_operation("Red warejouse adjust")
        while(self.m_color_sen.color() != Color.YELLOW):
            self.m_drive_base.drive(-10,-40)
            wait(250)
        self.m_drive_base.stop()
        counter = 1
        while(counter != part):
            self.m_drive_base.drive(50, 0)

            if(self.m_color_sen.color() != Color.YELLOW):
                wait(250)

            if(self.m_color_sen.color() == Color.YELLOW):
                counter = counter+1
                while(self.m_color_sen.color() == Color.YELLOW and counter != part):
                    wait(1000)
        wait(500)
        while(not self.m_crane.m_touch_sen.pressed()):
            self.warehouse_drive(0.5)
        self.m_drive_base.stop()
        self.m_crane.pick_up_pallet()
        self.m_drive_base.drive(-50, 0)
        while(self.m_color_sen.color() != Color.WHITE):
            wait(500)
       
        self.m_drive_base.drive_time(-50,45, 4000)
        self.m_drive_base.drive(50, 0)
        while(self.m_color_sen.color() != Color.BLUE):
            wait(250)

    def emergency_mode(self, operation=""):
        notify_operation("emergency mode")
        speak(operation+" failed")
        self.m_crane.m_crane.run_until_stalled(90)
        wait(2000)
        self.m_drive_base.straight(-55)
        for i in range(4):
            speak("Beep")
            wait(1000)

