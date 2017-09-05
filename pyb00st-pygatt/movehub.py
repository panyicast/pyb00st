#!/usr/bin/env python3

import pygatt
from constants import *

#
# To Do:
# - exception handling
# - validate connection
#


class MoveHub:
    address = ""
    controller = ""
    last_color = ''

    def __init__(self, address, controller):
        ''' Constructor for this class. '''
 
        self.address=address
        self.controller=controller

#        self.req = GATTRequester(self.address,False,self.controller)
#        self.connect()

        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.connect()

    def connect(self):

        self.device = self.adapter.connect(self.address)

    def is_connected(self):
        ### Needs thinking
        return True

    def getaddress(self):
        return self.address

    def getname(self):
        self.connect()
        devicename=self.device.char_read_handle(0x07)
        return devicename.decode("utf-8")

    def set_led_color(self, color):
        if color in LED_COLORS :
            self.device.write_handle(MOVE_HUB_HARDWARE_HANDLE, SET_LED_COLOR[LED_COLORS.index(color)] )

    def motor_timed(self, motor, time_ms, dutycycle_pct):
        if motor in MOTORS :
            if dutycycle_pct in range (-100,101) :
                command = MOTOR_TIMED_INI
                command += motor
                command += MOTOR_TIMED_MID
                t = time_ms.to_bytes(2, byteorder='little')
                command += t
                if dutycycle_pct < 0 :
                    dutycycle_pct += 255
                command += bytes( bytes( chr(dutycycle_pct), 'latin-1' ) )
                command += MOTOR_TIMED_END

#                print("Final Command:", command)
#                i=0
#                for x in command:
#                    print( i, x )
#                    i+=1

                self.device.write_handle(MOVE_HUB_HARDWARE_HANDLE, command )


    def motors_timed(self, motor, time_ms, dutycycle_pct_A, dutycycle_pct_B):
        if motor in MOTOR_PAIRS :
            if dutycycle_pct_A in range (-100,101) and dutycycle_pct_B in range (-100,101) :
                command = MOTORS_TIMED_INI
                command += motor
                command += MOTORS_TIMED_MID
                t = time_ms.to_bytes(2, byteorder='little')
                command += t
                if dutycycle_pct_A < 0 :
                    dutycycle_pct_A += 255
                command += bytes( bytes( chr(dutycycle_pct_A), 'latin-1' ) )
                if dutycycle_pct_B < 0 :
                    dutycycle_pct_B += 255
                command += bytes( bytes( chr(dutycycle_pct_B), 'latin-1' ) )
                command += MOTORS_TIMED_END

#                print("Final Command:", command)
#                i=0
#                for x in command:
#                    print( i, x )
#                    i+=1

                self.device.write_handle(MOVE_HUB_HARDWARE_HANDLE, command )

    def subscribe(self, callback_function):
        self.device.subscribe(MOVE_HUB_HARDWARE_UUID, callback_function)


    def init_color_sensor(self, port):
        if port == 'C' :
            self.device.char_write_handle(MOVE_HUB_HARDWARE_HANDLE, COLOR_SENSOR_ON_C)
        elif port == 'D' :
            self.device.char_write_handle(MOVE_HUB_HARDWARE_HANDLE, COLOR_SENSOR_ON_D)

    def read_color_sensor(self, handle, value):
        # to be used as callback when subscribing notifications
        if handle == MOVE_HUB_HARDWARE_HANDLE :
            if value[4] != 0xFF :
                 self.last_color = COLOR_SENSOR_COLORS[value[4]]


