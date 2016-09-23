from ctypes import *

motorDll = windll.LoadLibrary("DMC2410.dll")
XAxis = c_uint16(0)
YAxis = c_uint16(1)
ZAxis = c_uint16(2)
AxisList = [XAxis, YAxis, ZAxis]
def initMotorCard():
    ret = motorDll.d2410_board_init()
    if ret <= 0:
        return False
    return True
def isRunning(axis):
    ret = motorDll.d2410_check_done(axis)
    return ret == 0

def getPosition(axis):
    ret = motorDll.d2410_get_position(axis)
    return ret

def resetPosition(pos = [0, 0, 0]):
    for axis in AxisList:
        motorDll.d2410_set_position(axis, c_long(pos[axis]))

def decelStop(axis):
    motorDll.d2410_decel_stop(axis, c_double(0.1))

def imdStop(axis):
    motorDll.d2410_imd_stop(axis)

def emgStop():
    motorDll.d2410_emg_stop()
    d2410_check_done(0)
    motorDll.d2410_emg_stop()

def preConfig(axis, outMode, startVel, maxVel, speedUpTime, slowDownTime, sTime = 0.01, stopVel = 100):
    if isRunning(axis):
        return False
    motorDll.d2410_set_pulse_outmode(axis, c_uint16(outMode))
    #TMode
    motorDll.d2410_set_profile(axis,  c_double(startVel), c_double(maxVel), c_double(speedUpTime), c_double(slowDownTime))
    #SMode
    #motorDll.d2410_set_st_profile(axis, startVel, maxVel, speedUpTime, slowDownTime, sTime, stopVel)

def moveByDir(axis, dir):
    if isRunning(axis):
        return False
    #TMode
    motorDll.d2410_t_vmove(axis, c_uint16(dir))
    #SMode
    #motorDll.d2410_s_vmove(axis, dir)
    return True



    
