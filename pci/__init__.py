import pci
import pcitypes
ADDELAY_OFFSET = 0x2000
def openDevice():
    return pci.DmaSglChannelOpen()

def collectData():
    return pci.ADData()

def writeBar(offset, value):
    return pci.WriteBar(offset, value)
