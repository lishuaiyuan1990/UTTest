from ctypes import *
from pcitypes import *
from win32event import *
from win32con import *
from win32api import *
from win32gui import *

pciDll = cdll.LoadLibrary("PlxApi.dll")
hDeviceList = [0, 0]

def OpenDevice():
    deviceNum = c_uint32(0)
    pKey = DEVICE_LOCATION()
    memset(byref(pKey), -1, sizeof(pKey))
    pKey.BusNumber = c_ubyte(-1)
    pKey.SlotNumber = c_ubyte(-1)
    pKey.DeviceId = 0x5406
    pKey.VendorId = 0x10b5
    pKey.SerialNumber[0] = c_ubyte(0)
    hDevice = c_ulong()
    rc = pciDll.PlxPciDeviceFind(pointer(pKey), byref(deviceNum))
    #print "PlxPciDeviceFind: %x" % rc
    rc = pciDll.PlxPciDeviceOpen(byref(pKey), byref(hDevice))
    #print "PlxPciDeviceOpen: %x" % rc
    #print "hDevice: %x"% hDevice.value
    return hDevice

def DmaSglChannelOpen():
    hDevice = OpenDevice()
    hDeviceList[0] = hDevice
    DmaDesc = DMA_CHANNEL_DESC()
    DmaDesc.EnableReadyInput         = (1);
    DmaDesc.EnableBTERMInput         = (0);
    DmaDesc.EnableIopBurst           = (1);
    DmaDesc.EnableWriteInvalidMode   = (0);
    DmaDesc.EnableDmaEOTPin          = (0);
    DmaDesc.DmaStopTransferMode      = 0;
    DmaDesc.HoldIopAddrConst         = (1);
    DmaDesc.DemandMode               = (0);
    DmaDesc.EnableTransferCountClear = (0);
    DmaDesc.WaitStates               = (0);
    DmaDesc.IopBusWidth              = (2); # 32-bit
    DmaDesc.DmaChannelPriority       = Rotational;    
    rc = pciDll.PlxDmaSglChannelOpen(hDevice,PrimaryPciChannel0,byref(DmaDesc))
    #print "PlxDmaSglChannelOpen: %x" % rc

def initIntr():
    hDevice = hDeviceList[0]
    PlxInterrupt = PLX_INTR()
    #memset(pointer(PlxInterrupt), 0, sizeof(PLX_INTR))    
    rc = pciDll.PlxIntrStatusGet(hDevice, byref(PlxInterrupt));
    #print "PlxIntrStatusGet: %x" % rc
    hInterruptEvent = c_int()
    PlxInterrupt.PciDmaChannel0 = (1) # PCI DMA Channel 0
    PlxInterrupt.PciMainInt = (1)
    PlxInterrupt.IopToPciInt = (1) # Messaging Unit Inbound Post    
    rc = pciDll.PlxIntrAttach(hDevice, PlxInterrupt, byref(hInterruptEvent))
    #print "PlxIntrAttach: %x" % rc
    rc = pciDll.PlxIntrEnable(hDevice, byref(PlxInterrupt))
    #print "PlxIntrEnable: %x" % rc

def DmaSglTransfer():
    hDevice = hDeviceList[0]
    buffer = (c_int32 * 1000)()
    DmaData = DMA_TRANSFER_ELEMENT()
    DmaData.u.UserVa = addressof(buffer) 
    DmaData.LocalAddr = 0x00008000;
    DmaData.TransferCount = c_uint(4000);
    DmaData.LocalToPciDma = (1)# Local to PCI
    DmaData.TerminalCountIntr = (0);
    DmaData.PciSglLoc = (1)
    DmaData.LastSglElement= (1)
    
    rc = pciDll.PlxDmaSglTransfer(hDevice, PrimaryPciChannel0, pointer(DmaData), c_uint32(0));
    #print "PlxDmaSglTransfer: %x" % rc
    return buffer
    
def WriteBar(offset, value):
    ctypeList = (c_uint, c_int, c_ulong, c_long)
    if not isinstance(value, ctypeList):
        value = c_uint(value)
    hDevice = hDeviceList[0]
    rc = pciDll.PlxBusIopWrite(hDevice, 0, offset, FALSE, byref(value),4, 2)
    return rc

def ADData():
    initIntr()
    buffer = DmaSglTransfer()  
    retList = []
    for i in range(0, DATALENGTH):
        retList.append(buffer[i])
    return retList

if __name__ == "__main__":
    DmaSglChannelOpen()
    ADData()
