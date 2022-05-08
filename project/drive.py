from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.parameters import Color
from misc import notify_operation
import pickup

import time


ev3 = EV3Brick
class DriveRobot:
    
    def __init__(self, drive_base, color_sen, crane):
        self.m_drive_base = drive_base
        self.m_color_sen = color_sen
        self.col = Color.GREEN
        self.change_col = Color.BROWN
        self.m_Crane = crane

    def drive(self,in_time=0, path= 20):
        '''Moves the car along a predetermined path, turning as need be'''
        change = True
        start_time = time.time()
        print((time.time()-start_time))
        while change and ((time.time()-start_time)<in_time or in_time == 0):
            turned = 1
            self.m_drive_base.drive(30,0)
            deviation = self.m_color_sen.reflection() - path
            
            while (deviation > path):
                self.m_drive_base.stop()
                turned = -2*turned
                self.m_drive_base.turn(turned)
                deviation = self.m_color_sen.reflection() - path
                if(turned > 180):
                    quit
                    #EmergencyMode()
        print("Hejsan svejsan",start_time-time.time())      
            #change = get_change(path, color_sen)

    def return_to_area(self,area):
        location_dict = {
            "Warehouse": 20, 
            "Blue Warehouse": 20,
            "Red Warehouse" : 20,
            "Pickup and delivery": 20}
        while(self.m_color_sen.reflection()!=location_dict[area]):
            self.drive(2)

        self.drive(0,location_dict[area]) 

    def emergency_mode(self):
        notify_operation("emergency mode")
        self.m_Crane.m_crane.run_until_stalled(-90)
        wait(2000)
        self.m_drivebase.drive(-55,0)
        for i in range(1,4):
            ev3.speaker.beep()
            wait(1000)
   

    def drive2(self,in_time=0, path= 20):
        current_operation = "Drive. follow path " + str(self.col)
        notify_operation(current_operation)
        change = True
        
        start_time = time.time()
        print((time.time()-start_time))
        while change and ((time.time()-start_time)<in_time or in_time == 0):
            turned = 1
            self.m_drive_base.drive(30,0)
            deviation = self.m_color_sen.color()
            if self.m_Crane.pallet_on == True:
                if self.m_Crane.m_touch_sen.pressed() == False:
                    self.emergency_mode(self)
                    quit
            
            while (deviation != self.col):
                
                if (deviation == self.change_col):
                    self.col = self.change_col
                    self.change_col = None
                elif deviation != Color.WHITE:
                    self.m_drive_base.straight(10)
                #elif deviation != Color.BLACK:
                 #   quit

                self.m_drive_base.stop()
                turned = -1.5*turned
                self.m_drive_base.turn(turned)
                deviation = self.m_color_sen.color()
                
                if(turned > 180):
                    ev3.speaker.say("Cant find line. Abort drive")
                    quit

    def return_to_area(self, area):
        color = color()
        location_dict = {
            "Warehouse": color.BOWN,
            "Blue Warehouse": color.BLUE,
            "Red Warehouse": color.RED,
            "Pickup and delivery": color.GREEN,
            "Center": color.GREEN}
        while(self.m_color_sen.color() != location_dict[area]):
            self.drive(1)

        self.drive(0, location_dict[area])


    def avoid_collision(self):
        if self.m_ultra_sen.distance() < 100:
            self.m_drive_base.run(-30)
            # Emergency mode
 
    def left_area(self, area):
        colour = Color()
        ev3 = EV3Brick()
        if self.m_color_sen.color() != colour.White and self.m_color_sen.color() != area:
            ev3.speaker.beep()
            print(self.Col)
            self.Col = self.m_color_sen.color()

    def set_color(self, str_color):
        color_dict = {
            "brown": Color.BROWN,
            "blue": Color.BLUE,
            "red": Color.RED,
            "green": Color.GREEN,}
        self.col = color_dict(str_color)
        return
            
    def set_color_change(self, str_color_change):
        color_dict = {
            "brown": Color.BROWN,
            "blue": Color.BLUE,
            "red": Color.RED,
            "green": Color.GREEN,}
        self.change_col = color_dict(str_color_change)
        return

    def return_to_circle(self):
        self.m_drive_base.turn(180)
        self.set_color_change("brown")

    def select_area(self, area):
        
        location_dict = {
            "Blue Warehouse": Color.BLUE,
            "Red Warehouse": Color.RED,
            "Pickup and delivery": Color.GREEN,}
        if self.col != Color.BROWN:
            self.return_to_circle(self)

        self.set_color_change(self, location_dict(area))
        self.set_color(self, "brown")
