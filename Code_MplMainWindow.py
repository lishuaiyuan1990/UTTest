# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pci import *
import sys
print sys.path

MAX_GATE_NUM = 6
COLORLIST = ["001", "010", "100"]#, "011", "110", "101"]
GATEDIC = ["m_color", "m_start", "m_len", "m_threshold"]
from Ui_MplMainWindow import Ui_MainWindow
from widget.gatetablewidget import GateTableWidgetItem, Gate
from Ui_ProbePara import Ui_Dialog

class ProbeParaDialog(Ui_Dialog):
    def __init__(self, parent = None):
        super(ProbeParaDialog, self).__init__(parent)
        self.setupUi(self)
        self.exist = True
        self.m_freqStart = 0
        self.m_freqTo = 0
        self.m_ampResolution = 0.1
        
        self.m_maxAmp = 0
        self.m_adDelay = 0
        self.m_fs = 100
    
    def closeEvent(self,  event):
        self.exist = False
        self.widget.timer.stop()
        event.accept()
    def parseFreq(self, f):
        f = min(f, self.widget.m_fs / 2.0)
        f = max(f, 0)
        N = len(self.widget.m_rawData)
        n = float(f) * N / self.widget.m_fs
        n = round(n)
        return n
    def findFreqAmpIndex(self, ampBydB, rangeFrom, rangeTo):
        lowFreq = [100, 0]
        step = 1
        if rangeFrom > rangeTo:
            step = -1
        for index in range(rangeFrom, rangeFrom, step):
            if abs(self.widget.m_fftData[index] - ampBydB) < self.m_ampResolution:
                lowFreq[0] = abs(self.widget.m_fftData[index] - ampBydB)
                lowFreq[1] = index
                break
            if abs(self.widget.m_fftData[index] - ampBydB) < lowFreq[0]:
                lowFreq[0] = abs(self.widget.m_fftData[index] - ampBydB)
                lowFreq[1] = index
        index = lowFreq[1]
        return [self.widget.m_fftData[index], index]
    def maxAmpIndex(self, nfrom, nto):
        maxAmp = [0, 0]
        for index in range(nfrom, nto):
            if maxAmp[0] < self.widget.m_fftData[index]:
                maxAmp[0] = self.widget.m_fftData[index]
                maxAmp[1] = index
        return maxAmp
    def getKeyAmp(self, nfrom, nto):
        nfrom = self.parseFreq(self.m_freqStart)
        nto = self.parseFreq(self.m_freqTo)
        if nfrom >= nto:
            return False
        self.m_maxAmp = self.maxAmpIndex(nfrom, nto)
        
        ampBy = self.m_maxAmp[0] * 0.5
        self.m_lowFreqBy6 = self.findFreqAmpIndex(ampBy, self.m_maxAmp[1], nfrom)
        self.m_highFreqBy6 = self.findFreqAmpIndex(ampBy, self.m_maxAmp[1], nto)
        
        ampBy = self.m_maxAmp[0] * 0.1
        self.m_lowFreqBy20 = self.findFreqAmpIndex(ampBy, self.m_maxAmp[1], nfrom)
        self.m_highFreqBy20 = self.findFreqAmpIndex(ampBy, self.m_maxAmp[1], nto)
        return True
        
    def calFreqCenter(self):
        centerFreq = (self.m_lowFreqBy6[0] * self.m_highFreqBy6[0]) ** 0.5
        self.m_centerFreq = centerFreq
        return centerFreq
    
    def calBWBy6(self):
        #[(fu-fl)/f0]×100%
        bwBy6 = float(self.m_highFreqBy6[0] - self.m_lowFreqBy6[1]) / self.m_centerFreq
        return bwBy6
    def calLowAndHighFreqBy6(self):
        high = self.m_highFreqBy6[0]
        low = self.m_lowFreqBy6[0]
        return [low, high]
    
    def calBWBy20(self):
        #[(fu-fl)/f0]×100%
        bwBy20 = float(self.m_highFreqBy20[0] - self.m_lowFreqBy20[1]) / self.m_centerFreq
        return bwBy20
    def calLowAndHighFreqBy20(self):
        high = self.m_highFreqBy20[0]
        low = self.m_lowFreqBy20[0]
        return [low, high]
    
    def calVPP(self, timeFrom, timeTo):
        pass
        
            
class Code_MainWindow(Ui_MainWindow):
    def __init__(self, parent = None):
        super(Code_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.m_dsbDelay.valueChanged.connect(self.setDelay)
        self.m_gateSet = []
        self.m_colorSet = []
        self.m_gateTable.setGateHeaderInfo()
        self.m_gateTable.itemChanged.connect(self.syncGateInfo)
        self.m_gateTable.currentCellChanged.connect(self.setCurrentPos)
        self.m_gateTable.cellClicked.connect(self.setClickMark)
        self.m_addGateBtn.clicked.connect(self.addGate)
        self.m_rmGateBtn.clicked.connect(self.rmGate)
        self.m_probePara.clicked.connect(self.fftParse)
        self.currentRow = -1
        self.currentCol = -1
        self.m_clickMark = False
        self.setDelay(0)
        step = QPoint(1, 1)
        posFrom = QPoint(0, 0)
        posTo = QPoint(100, 100)
        self.m_cscanWidget.setScanPos(posFrom, posTo, step)
        self.timer = QtCore.QBasicTimer()
                
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.m_probeDialog.exist:
                self.m_probeDialog.widget.setData(self.m_mplCanvas.m_rawData)
            else:
                self.timer.stop()
                del self.m_probeDialog
                print "timer Stop"
        else:
            QtGui.QWidget.timerEvent(self, event)
    def fftParse(self):
        self.timer.start(500, self)
        self.m_probeDialog = ProbeParaDialog(self)
        self.m_probeDialog.widget.setData(self.m_mplCanvas.m_rawData)
        self.m_probeDialog.show()
        
    def setClickMark(self):
        self.m_clickMark = True
        print "setClickMark"
        
    def setCurrentPos(self, row, col):
        self.currentRow = row
        self.currentCol = col
        
    def rmGate(self):
        if not (len(self.m_gateSet) > 0 and len(self.m_colorSet) > 0 and self.m_gateTable.rowCount() > 0):
            return
        row = self.currentRow
        self.m_gateTable.removeRow(row)
        self.m_colorSet.pop(row)
        gate = self.m_gateSet.pop(row)
        gate.reset()
        self.m_mplCanvas.resetGate(gate)
        
    def syncGateInfo(self, item):
        if not self.m_clickMark:
            return
        curRow = self.currentRow
        curCol = self.currentCol
        ret = item.data(Qt.DisplayRole).toDouble()
        if not ret[1]:
            return
        if curCol is 1:
            print "m_start"
            self.m_gateSet[curRow].m_start = ret[0]
        elif curCol is 2:
            print "m_len"
            self.m_gateSet[curRow].m_len = ret[0]
        elif curCol is 3:
            self.m_gateSet[curRow].m_threshold = ret[0]
            print "m_threshold"
        else:
            return
        self.m_mplCanvas.drawGate(self.m_gateSet[curRow])
        self.m_clickMark = False

    def addGate(self):
        gate = self.genGate()
        if not gate:
            return None
        self.m_gateTable.itemChanged.disconnect(self.syncGateInfo)
        self.m_gateSet.append(gate)
        self.m_colorSet.append(gate.m_color)
        self.m_gateTable.setRowCount(self.m_gateTable.rowCount() + 1)
        curRow = self.m_gateTable.rowCount() - 1
        item = QTableWidgetItem("")
        item.setBackground(QBrush(gate.m_color))
        item.setFlags(Qt.NoItemFlags)
        self.m_gateTable.setItem(curRow,0, item)
       
        gateStart = GateTableWidgetItem("")
        gateLen = GateTableWidgetItem("")
        gateThreshold = GateTableWidgetItem("")
        
        gateStart.setValue(gate.m_start)
        gateLen.setValue(gate.m_len)
        gateThreshold.setValue(gate.m_threshold)
                
        self.m_gateTable.setItem(curRow,1, gateStart)
        self.m_gateTable.setItem(curRow,2, gateLen)
        self.m_gateTable.setItem(curRow,3, gateThreshold)
        self.m_gateTable.setCurrentItem(gateStart)
        self.m_mplCanvas.drawGate(gate)
        self.m_gateTable.itemChanged.connect(self.syncGateInfo)

    def genColor(self):
        for item in COLORLIST:
            color = QColor(255 * int(item[0]), 255 * int(item[1]), 255 * int(item[2]))
            if color not in self.m_colorSet:
                return color
        return None
    def genGate(self):
        color = self.genColor()
        if not color:
            return None
        gate = Gate(color)
        return gate
    def setDelay(self, value):
        writeBar(ADDELAY_OFFSET, value)
        self.m_mplCanvas.syncADDelay(value)
        print "setDelay: %f" % value
        
    def closeEvent(self,  event):
        result = QtGui.QMessageBox.question(self,  "Confirm Exit...", 
        "Are you sure you want to exit?",  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        event.ignore()
        if result == QtGui.QMessageBox.Yes:
            event.accept()
    
if __name__ == "__main__":
    import sys
    print sys.path
    app = QtGui.QApplication(sys.argv)
    ui = Code_MainWindow()
    ui.show()
#sys.exit(app.exec_())
    
        
    
    
    
    
    
    
        
