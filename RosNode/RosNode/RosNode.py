#!/usr/bin/env python
from enum import IntEnum
import serial
import struct
import time
import os
if os.name!='nt':
    import rospy
    from std_msgs.msg import *


class Servo:
    def __init__(self,channel,min,max):
        self.channel = channel
        self.min = min
        self.max = max
        self.pos = min

class GripperInterface:
    """Serial Interface to Gripper"""
    def __init__(self,port,debug=False):
        self.debug = debug
        if not port:
            self.port = serial.Serial()
        else:
            self.port = serial.Serial(port,9600,parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,xonxoff=False,timeout=10.0)
            self.port.close()
            self.port.open()

        time.sleep(2);
        if debug: "Start: ", self.port.read_all()

        self.servos = [Servo(0,401,824), Servo(1,251,1009)]
        self.__open()
        self.__writeCommand(1,630)
        time.sleep(1.5)
        self.__writeCommand(1,0)
        self.__writeCommand(0,0)


    def __writeCommand(self,servo,ums):
        if servo < len(self.servos):
            s = self.servos[servo]
            if ums>s.min and ums<s.max: s.pos = ums
            cmd = struct.pack('B',s.channel)+struct.pack('H',ums)
            if self.port.isOpen() :
                nb_written = self.port.write(cmd)
                if self.debug:
                    if (3 != nb_written):print "Error only wrote %i not %i bytes"%(nb_written,nb)
                    print "On Channel %i send %i"%(s.channel,ums)
                    print "wrote:", cmd
                    time.sleep(0.5)
                    print "read: ", self.port.read_all()

    def __open(self):
        self.__writeCommand(self.servos[0].channel,self.servos[0].min)
        time.sleep(0.1)
        self.__writeCommand(self.servos[0].channel,0)
    
    def __close(self,amount):
        if amount <=2:
            self.__writeCommand(self.servos[0].channel,self.servos[0].max)
        else:
            self.__writeCommand(self.servos[0].channel,640)
        time.sleep(0.1)
        self.__writeCommand(self.servos[0].channel,0)

    def __mmToUms(self,amount):
        # D = 60, r = 30mm
        '''
        Delta_L = D/2 * Delta_Theta
        Delta_Theta = Range_Theta / Range_UMS * Delta_UMS
        Delta_L = D/2*Range_Theta/Range_UMS * Delta_UMS
        Delta_UMS = Range_UMS/Range_Theta * 1/r * Delta_L = A * Delta_L
        Range_UMS = 760
        Range Theta = 8 * 2*pi = 50.265
        1/r = 1/30
        A = 0.504
        '''
        return amount*0.503

    def test(self,servo,ammount):
        self.__writeCommand(self.servos[servo].channel, ammount)

    def increment(self,msg):
        self.__writeCommand(self.servos[1].channel, self.servos[1].pos+self.__mmToUms(msg.data))

    def openclose(self,msg):
        if msg.data == 0:
            self.__open()
        elif msg.data == 1:
            self.__close(1)
        elif msg.data == 2:
            self.__close(2)


def rosmain():
    rospy.init_node('gripper', anonymous=True)
    full_param_name = rospy.search_param('port')
    port = rospy.get_param(full_param_name)

    full_param_name = rospy.search_param('debug')
    d = rospy.get_param(full_param_name)
    debug = False
    if d: debug = bool(d)

    full_param_name = rospy.search_param('oc_channel')
    oc_channel = rospy.get_param(full_param_name)
    full_param_name = rospy.search_param('i_channel')
    i_channel = rospy.get_param(full_param_name)
    
    AI = GripperInterface(port,debug)
    
    rospy.Subscriber(oc_channel,Int32,AI.openclose)
    rospy.Subscriber(i_channel,Float32,AI.increment)
    rospy.spin()
    return 0

def cmd_line_main():
    "/dev/ttyACM0"
    print "Starting"
    debug = bool(input("Debug 1/0: "))
    print debug
    AI = GripperInterface("COM4",debug)
    val = 0
    channel = 0
    while channel >=0 and channel < 4:
        channel = input("channel: ")
        while val <2000 and val>=0:
            val = input("val: ")
            if (val >= 0) and (channel >= 0): AI.test(channel,val)
    return 0

if __name__ == '__main__':
    cmd_line_main()