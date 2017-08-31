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

class ChopsawInterface:
    """Serial Interface to Gripper"""
    def __init__(self,port,debug=False, pub = False):
        self.debug = debug
        self.pub = pub
        if not port:
            self.port = serial.Serial()
        else:
            self.port = serial.Serial(port,9600,parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,xonxoff=False,timeout=10.0)
            self.port.close()
            self.port.open()

        time.sleep(2);
        if debug: "Start: ", self.port.read_all()

        self.__open();


    def __writeCommand(self,cmd):
            if self.port.isOpen() :
                self.port.read_all();
                nb_written = self.port.write(cmd)
                if (len(cmd) != nb_written) and self.debug :
                    print "Error only wrote %i not %i bytes"%(nb_written,len(cmd))
                received = self.port.read();
                if received != cmd: 
                    if self.debug :print "Error, recieved: %s\t expetected%s"%(received,cmd)  
                    return False
                return True

    def __move(self,cmd):
        if self.__writeCommand(cmd):
            response = self.port.read()
            while self.port.read() != 's':
                time.sleep(0.1)
            if self.pub: self.pub(True)


    def __stopped(self):
        if self.pub: self.pub(True)

    def test(self,cmd):
        self.__writeCommand(cmd)

    def blade(self,msg):
        if msg.data:
            self.__writeCommand('B')
        else:
            self.__writeCommand('b')

    def openclose(self,msg):
        if msg.data:
            self.__move('o')
        else:
            self.__move('c')



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
    full_param_name = rospy.search_param('b_channel')
    b_channel = rospy.get_param(full_param_name)
    
    pub = rospy.Publisher('Chopsaw_move', Bool, queue_size=1)

    AI = GripperInterface(port,debug,pub)
    
    rospy.Subscriber(oc_channel,Bool,AI.openclose)
    rospy.Subscriber(i_channel,Bool,AI.blade)
    rospy.spin()
    return 0

def cmd_line_main():
    "/dev/ttyACM0"
    print "Starting"
    debug = bool(input("Debug 1/0: "))
    print debug
    AI = GripperInterface("COM6",debug)
    cmd = ''
    while cmd != 'q' and cmd != 'Q':
        cmd = input("cmd: ")
        AI.test(cmd)
        time.sleep(0.5)
        print "Read: ", AI.port.read_all()
    return 0

if __name__ == '__main__':
    cmd_line_main()