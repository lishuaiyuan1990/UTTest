from ctypes import *
class POINT(Structure):
    _fields_ = [("x", c_int),
                ("y", c_int)]
                
class PCI_MEMORY(Structure):
    _fields_ = [("UserAddr", c_uint32), ("PhysicalAddr", c_void_p), 
                    ("Size", c_uint32)]    
    
class DEVICE_LOCATION(Structure):
    _fields_ = [("BusNumber", c_ubyte), ("SlotNumber", c_ubyte), 
                ("DeviceId", c_ushort), ("VendorId", c_ushort), 
                ("SerialNumber", 12 * c_ubyte)]
    
class ARRAY(Structure):
    _fields_ = [("Array", 4000 * c_uint)]

class DMA_CHANNEL_DESC(Structure):
    _fields_ = [("EnableReadyInput", c_uint, 1), ("EnableBTERMInput", c_uint, 1), ("EnableIopBurst", c_uint, 1), \
                ("EnableWriteInvalidMode", c_uint, 1), ("EnableDmaEOTPin", c_uint, 1),("DmaStopTransferMode", c_uint, 1),\
                ("HoldIopAddrConst", c_uint, 1),("HoldIopSourceAddrConst", c_uint, 1),("HoldIopDestAddrConst", c_uint, 1),\
                ("DemandMode", c_uint, 1),("SrcDemandMode", c_uint, 1),("DestDemandMode", c_uint, 1),("EnableTransferCountClear", c_uint, 1),\
                ("WaitStates", c_uint, 4),("IopBusWidth", c_uint, 2),("EOTEndLink", c_uint, 1),("ValidStopControl", c_uint,1),\
                ("ValidModeEnable", c_uint, 1),("EnableDualAddressCycles", c_uint, 1),("Reserved1", c_uint, 9),("TholdForIopWrites", c_uint, 4),\
                ("TholdForIopReads", c_uint, 4),("TholdForPciWrites", c_uint, 4),("TholdForPciReads", c_uint, 4),("EnableFlybyMode", c_uint, 1),\
                ("FlybyDirection", c_uint, 1),("EnableDoneInt", c_uint, 1),("Reserved2", c_uint, 13),("DmaChannelPriority", c_uint)]

class PLX_INTR(Structure):
    _fields_ = [("InboundPost", c_uint, 1), ("OutboundPost", c_uint, 1),("OutboundOverflow", c_uint, 1),("OutboundOption", c_uint, 1),\
                ("IopDmaChannel0", c_uint, 1),("PciDmaChannel0", c_uint, 1),("IopDmaChannel1", c_uint, 1),("PciDmaChannel1", c_uint, 1),\
                ("IopDmaChannel2", c_uint, 1),("PciDmaChannel2", c_uint, 1),("Mailbox0", c_uint, 1),("Mailbox1", c_uint, 1),("Mailbox2", c_uint, 1),\
                ("Mailbox3", c_uint, 1),("Mailbox4", c_uint, 1),("Mailbox5", c_uint, 1),("Mailbox6", c_uint, 1), ("Mailbox7", c_uint, 1),\
                ("IopDoorbell", c_uint, 1),("PciDoorbell", c_uint, 1),("SerialPort1", c_uint, 1),("SerialPort2", c_uint, 1),("BIST", c_uint, 1),\
                ("PowerManagement", c_uint, 1),("PciMainInt", c_uint, 1),("IopToPciInt", c_uint, 1),("IopMainInt", c_uint, 1),("PciAbort", c_uint, 1),\
                ("PciReset", c_uint, 1),("PciPME", c_uint, 1),("Enum", c_uint, 1),("PciENUM", c_uint, 1),("IopBusTimeout", c_uint, 1),("AbortLSERR", c_uint, 1),\
                ("ParityLSERR", c_uint, 1),("RetryAbort", c_uint, 1),("LocalParityLSERR", c_uint, 1),("PciSERR", c_uint, 1),\
                ("IopRefresh", c_uint, 1),("PciINTApin", c_uint, 1), ("IopINTIpin", c_uint, 1),("TargetAbort", c_uint, 1),("Ch1Abort", c_uint, 1),\
                ("Ch0Abort", c_uint, 1),("DMAbort", c_uint, 1),("IopToPciInt_2", c_uint, 1),("SwInterrupt", c_uint, 1),("DmaChannel3", c_uint, 1),("Reserved", c_uint, 16)]

class DMA_UNION(Union):
    _fields_ = [("UserVa", c_uint32), ("PciAddrLow", c_uint32), ("SourceAddr", c_uint32)]
    
class DMA_TRANSFER_ELEMENT(Structure):
    _fields_ = [("u", DMA_UNION),("PciAddrHigh", c_uint32), ("LocalAddr", c_uint32),("DestAddr", c_uint32),\
                ("TransferCount", c_uint32),("NextSglPtr", c_uint32),("PciSglLoc", c_uint, 1),\
                ("LastSglElement", c_uint, 1),("TerminalCountIntr", c_uint, 1),("LocalToPciDma", c_uint, 1)]

#DMA_CHANNEL_DESC.DmaStopTransferMode
AssertBLAST = (0)
#DMA_CHANNEL_PRIORITY
Channel0Highest,Channel1Highest,Channel2Highest,Channel3Highest,Rotational = map(lambda x: c_uint(x), range(0, 5)) 
#DMA_CHANNEL
IopChannel0, IopChannel1, IopChannel2, PrimaryPciChannel0, PrimaryPciChannel1, PrimaryPciChannel2, PrimaryPciChannel3 = map(lambda x: c_int(x), range(0, 7))
#A-Scan Length
DATALENGTH = 1000
