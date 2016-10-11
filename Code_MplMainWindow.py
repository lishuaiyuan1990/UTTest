# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pci import *
from copy import copy
import sys
import motor.motordriver as mdriver
print sys.path
import numpy as np


MAX_GATE_NUM = 6
COLORLIST = ["001", "010", "100"]#, "011", "110", "101"]
GATEDIC = ["m_color", "m_start", "m_len", "m_threshold"]
from Ui_MplMainWindow import Ui_MainWindow
from widget.gatetablewidget import GateTableWidgetItem, Gate
from Ui_ProbePara import Ui_Dialog as Ui_ProbeParaDialog
from Ui_ProbeBeam import Ui_Dialog as Ui_ProbeBeamDialog
class ProbeBeamDialog(Ui_ProbeBeamDialog):
    def __init__(self, parent = None):
        super(ProbeBeamDialog, self).__init__(parent)
        self.setupUi(self)

class ProbeParaDialog(Ui_ProbeParaDialog):
    def __init__(self, parent = None):
        super(ProbeParaDialog, self).__init__(parent)
        self.setupUi(self)
        self.exist = True
        self.m_freqStart = 0
        self.m_freqTo = 0
        self.m_ampResolution = 0.1
        self.m_fftCurve.toggled.connect(self.syncWidgetCurve)
        self.m_maxAmp = 0
        self.m_adDelay = 0
        self.m_fs = 100
        self.m_calulateBtn.clicked.connect(self.calProbePara)
    def calProbePara(self):
        self.setTimeAndFreqRange()
        self.getKeyAmp()
        freq = self.calFreqCenter()
        print freq
        bWBy6 = self.calBWBy6()
        bWBy20 = self.calBWBy20()
        vpp = self.calVPP()
        pluseWidth = self.calPluseWidth()
        self.m_freqCenterSpinBox.setValue(freq)
        self.m_bwby6SpinBox.setValue(bWBy6)
        self.m_lowFreqby6SpinBox.setValue(self.m_lowFreqBy6[1])
        self.m_highFreqby6SpinBox.setValue(self.m_highFreqBy6[1])
        self.m_lowFreqby20SpinBox.setValue(self.m_lowFreqBy20[1])
        self.m_highFreqby20SpinBox.setValue(self.m_highFreqBy20[1])
        self.m_bwby20SpinBox.setValue(bWBy20)
        self.m_probeSenseSpinBox.setValue(vpp)
        self.m_bwSpinBox.setValue(pluseWidth)

    def setADDelay(self, delay):
        self.m_adDelay = delay
        self.widget.setADDelay(self.m_adDelay)

    def syncWidgetCurve(self, checked):
        self.widget.setCurve(checked)
    def closeEvent(self,  event):
        self.exist = False
        self.widget.timer.stop()
        event.accept()
    def parseFreq(self, f):
        f = min(f, self.widget.m_fs / 2.0)
        f = max(f, 0)
        N = len(self.widget.m_fftData)
        n = float(f) * N / (self.widget.m_fs / 2.0)
        n = round(n)
        return int(n)
    def parseTime(self, t):
        n = (t - self.m_adDelay) * self.m_fs
        return int(n)
    def reverseFreq(self, n):
        N = len(self.widget.m_fftData)
        f = n * (self.widget.m_fs / 2.0) / N
        f = min(f, self.widget.m_fs / 2.0)
        f = max(f, 0)
        return f
    def findFreqAmpIndex(self, ampBydB, rangeFrom, rangeTo):
        lowFreq = [100, 0]
        step = 1
        if rangeFrom > rangeTo:
            step = -1
        for index in range(rangeFrom, rangeTo, step):
            if abs(self.widget.m_fftData[index] - ampBydB) < self.m_ampResolution:
                lowFreq[0] = abs(self.widget.m_fftData[index] - ampBydB)
                lowFreq[1] = index
                break
            if abs(self.widget.m_fftData[index] - ampBydB) < lowFreq[0]:
                lowFreq[0] = abs(self.widget.m_fftData[index] - ampBydB)
                lowFreq[1] = index
        index = lowFreq[1]
        return [self.widget.m_fftData[index], self.reverseFreq(index)]
    def maxAmpIndex(self, nfrom, nto):
        maxAmp = [-100, 0]
        for index in range(nfrom, nto):
            if maxAmp[0] < self.widget.m_fftData[index]:
                maxAmp[0] = self.widget.m_fftData[index]
                maxAmp[1] = index
        return maxAmp
    def getKeyAmp(self):
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
        lowFreq = self.m_lowFreqBy6[1]
        highFreq = self.m_highFreqBy6[1]
        centerFreq = (lowFreq * highFreq) ** 0.5
        self.m_centerFreq = centerFreq
        return centerFreq
    
    def calBWBy6(self):
        #[(fu-fl)/f0]×100%
        bwBy6 = float(self.m_highFreqBy6[1] - self.m_lowFreqBy6[1]) / self.m_centerFreq
        return bwBy6
    
    def calBWBy20(self):
        #[(fu-fl)/f0]×100%
        bwBy20 = float(self.m_highFreqBy20[1] - self.m_lowFreqBy20[1]) / self.m_centerFreq
        return bwBy20
        
    def setTimeAndFreqRange(self):
        self.m_freqStart = self.m_fromFreq.value()
        self.m_freqTo = self.m_toFreq.value()
        self.m_calTimeFrom = self.m_fromTime.value()
        self.m_calTimeTo = self.m_toTime.value()
        
    def calVPP(self):
        timeFrom = self.m_calTimeFrom
        timeTo = self.m_calTimeTo
        nfrom = self.parseTime(timeFrom)
        nto = self.parseTime(timeTo)
        vmin = 100
        minIndex = -1
        vmax = -100
        maxIndex = -1
        for index in range(nfrom, nto):
            if self.widget.m_rawData[index] < vmin:
                vmin = self.widget.m_rawData[index]
                minIndex = index
            if self.widget.m_rawData[index] > vmax:
                vmax = self.widget.m_rawData[index]
                maxIndex = index
        self.m_ampMax = [vmax, maxIndex]
        self.m_ampMin = [vmin, minIndex]
        self.m_vpp = vmax - vmin
        return self.m_vpp
    def findTimeAmpIndex(self, uniAmp, rangeFrom, rangeTo):
        retIndex = rangeFrom
        step = 1
        if rangeFrom > rangeTo:
            step = -1
        for index in range(rangeFrom, rangeTo, step):
            if abs(self.widget.m_rawData[index]) > abs(uniAmp):
                retIndex = index
        return retIndex
    def calPluseWidth(self):
        timeFrom = self.m_calTimeFrom
        timeTo = self.m_calTimeTo
        nfrom = self.parseTime(timeFrom)
        nto = self.parseTime(timeTo)
        uniAmp = self.m_vpp * 0.1
        maxIndex = self.m_ampMax[1]
        nStart = self.findTimeAmpIndex(uniAmp, maxIndex, nfrom)
        nEnd = self.findTimeAmpIndex(uniAmp, maxIndex, nto)
        timeWidth = float(nEnd - nStart) / self.m_fs
        return timeWidth
        
            
class Code_MainWindow(Ui_MainWindow):
    signalXStopMove = pyqtSignal()
    signalYStopMove = pyqtSignal()
    signalEmgStopMove = pyqtSignal()
    signalUpdateCScan = pyqtSignal(list)
    clockLen = 100
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
        self.m_probeBeamPara.clicked.connect(self.probeBeamParse)
        self.currentRow = -1
        self.currentCol = -1
        self.m_clickMark = False
        self.setDelay(0)
        step = 1
        posFrom = {'x': 0, 'y': 0}
        posTo = {'x': 100, 'y': 100}
        self.initMDriver()
        self.m_cscanWidget.setScanPos(posFrom, posTo, step)
        self.timer = QtCore.QBasicTimer()
        self.m_scanStartPos = None
        self.m_scanEndPos = None
        self.initSgn()
        self.m_probeDialog = None
        self.signalXStopMove.connect(self.xStop)
        self.signalYStopMove.connect(self.yStop)
        self.signalEmgStopMove.connect(self.emgStopMove)
        self.signalUpdateCScan.connect(self.m_cscanWidget.drawImg)
        self.timer.start(self.clockLen, self)
        self.m_xScaning = False
        self.m_yScaning = False
        self.m_readyForScan = False
        self.m_dataInGate = []
        self.m_adDelay = 0
        self.m_fs = 100
        self.m_gateIndex = 0
    def parseTime(self, t):
        n = (t - self.m_adDelay) * self.m_fs
        return int(n)
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.m_probeDialog != None and self.m_probeDialog.exist:
                self.m_probeDialog.widget.setData(self.m_mplCanvas.m_rawData)
            else:
                del self.m_probeDialog
                self.m_probeDialog = None
            self.updateAxisPos()
        else:
            QtGui.QWidget.timerEvent(self, event)
    def probeBeamParse(self):
        self.m_probeBeamDialog = ProbeBeamDialog(self)
        self.m_probeBeamDialog.show()
    def fftParse(self):
        #self.timer.start(500, self)
        self.m_probeDialog = ProbeParaDialog(self)
        self.m_probeDialog.setADDelay(self.m_adDelay)
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
        self.m_adDelay = value
        print "setDelay: %f" % value
        
    def closeEvent(self,  event):
        self.stopAllMove()
        result = QtGui.QMessageBox.question(self,  "Confirm Exit...", 
        "Are you sure you want to exit?",  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        event.ignore()
        if result == QtGui.QMessageBox.Yes:
            event.accept()
    def updateAxisPosData(self):
        self.m_xAxisPos = self.getAxisPos(mdriver.XAxis)
        self.m_yAxisPos = self.getAxisPos(mdriver.YAxis)
        self.m_zAxisPos = self.getAxisPos(mdriver.ZAxis)
    def getCScanDataByPos(self):
        dataSlice = np.array(self.m_mplCanvas.m_rawData[self.m_scanDataFrom:self.m_scanDataTo + 1])
        maxData = max(np.abs(dataSlice))
        return maxData
    #update
    def updateAxisPos(self):
        self.updateAxisPosData()
        self.m_nowPos = {'x':self.m_xAxisPos, 'y':self.m_yAxisPos, 'z':self.m_zAxisPos} 
        self.m_xPos.setText(QString.number(self.m_xAxisPos))
        self.m_yPos.setText(QString.number(self.m_yAxisPos))
        self.m_zPos.setText(QString.number(self.m_zAxisPos))
        if self.m_xScaning:
            if abs(self.m_xAxisPos - self.m_dPos['x']) < mdriver.SPRECISION:
                self.signalEmgStopMove.emit()
                #self.signalXStopMove.emit()
                self.m_xScaning = False
                self.m_yScaning = True
                self.m_scanStartPos['x'] = self.m_xAxisPos
                self.m_scanEndPos['x'] = (self.m_scanEndPos['x'] - self.m_xAxisPos) / mdriver.POINT_LEN * mdriver.POINT_LEN + self.m_xAxisPos
                self.moveToPosByAxis(mdriver.YAxis, self.m_scanStartPos, self.startMove)
        elif self.m_yScaning:
            if abs(self.m_yAxisPos - self.m_dPos['y']) < mdriver.SPRECISION:
                self.signalEmgStopMove.emit()
                #self.signalYStopMove.emit()
                self.m_yScaning = False
                self.m_scanStartPos['y'] = self.m_yAxisPos
                self.m_scanEndPos['y'] = (self.m_scanEndPos['y'] - self.m_yAxisPos) / mdriver.POINT_LEN * mdriver.POINT_LEN + self.m_yAxisPos
                self.m_cscanWidget.setScanPos(self.m_scanStartPos, self.m_scanEndPos, mdriver.POINT_LEN)
                self.m_cScanDrawData = np.zeros(self.m_cscanWidget.x.shape)
                self.startScanMove()
        if self.m_readyForScan:
            if self.checkScanMove():
                return
            if self.checkXScanMove():
                self.scanMove(mdriver.XAxis)
            else:
                self.scanMove(mdriver.YAxis)
    def initMDriver(self):
        mdriver.initMotorCard()
        self.preConfigAllAxisByDefault()
        mdriver.resetPosition()
    def getAxisPos(self, axis):
        return mdriver.getPosition(axis)
    def preConfigAllAxisByDefault(self):
        self.preConfigAllAxis(1, 160, 320, 0.1,  0.1)
    def preConfigAllAxis(self, outMode, startVel, maxVel, speedUpTime, slowDownTime, sTime = 0.01, stopVel = 100):
        for axis in mdriver.AxisList:
            mdriver.preConfig(axis, outMode, startVel, maxVel, speedUpTime, slowDownTime)
    def startMove(self, axis, dir):
        mdriver.moveByDir(axis, dir)

    def pMove(self, axis, dir):
        mdriver.pMoveByDir(axis, dir)
    def stopMove(self, axis = None):
        mdriver.decelStop(axis)
    def stopAllMove(self):
        self.m_readyForScan = False
        for axis in mdriver.AxisList:
            mdriver.decelStop(axis)
    def emgStopMove(self):
        self.m_readyForScan = False
        mdriver.emgStop()
    def xStartMovePlus(self):
        print "plus"
        self.startMove(mdriver.XAxis, 1)
    def xStartMoveMinus(self):
        print "Minus"
        self.startMove(mdriver.XAxis, 0)
    def yStartMovePlus(self):
        self.startMove(mdriver.YAxis, 1)
    def yStartMoveMinus(self):
        self.startMove(mdriver.YAxis, 0)
    def zStartMovePlus(self):
        self.startMove(mdriver.ZAxis, 1)
    def zStartMoveMinus(self):
        self.startMove(mdriver.ZAxis, 0)
    def xStop(self):
        self.stopMove(mdriver.XAxis)
    def yStop(self):
        self.stopMove(mdriver.YAxis)
    def zStop(self):
        self.stopMove(mdriver.ZAxis)
    def normalizePos(self, pos):
        for key in pos.keys():
            pos[key] = pos[key] / mdriver.POINT_LEN * mdriver.POINT_LEN
        return pos
    
    def setScanStartPos(self):
        self.m_scanStartPos = self.normalizePos({'x':self.m_xAxisPos, 'y':self.m_yAxisPos, 'z':self.m_zAxisPos})
    def setScanEndPos(self):
        self.m_scanEndPos = self.normalizePos({'x':self.m_xAxisPos, 'y':self.m_yAxisPos, 'z':self.m_zAxisPos})
    
    def moveToPosByAxis(self, axis, pos, moveFunc):
        if axis == mdriver.XAxis:
            self.m_xScaning = True
        axisSign = 'x'
        self.m_dPos = pos
        if axis == mdriver.YAxis:
            axisSign = 'y'
        npos = self.m_nowPos[axisSign]
        dir = 1
        if pos[axisSign] - npos < 0:
            dir = -1
        moveFunc(axis, dir)
    
    def isMotorRunning(self):
        if mdriver.isRunning(mdriver.XAxis) or mdriver.isRunning(mdriver.YAxis):
            return True
        else:
            return False
    def scanMove(self, axis):
        if self.isMotorRunning():
            return
        self.m_scanDataByRow.append(self.getCScanDataByPos())
        
        if axis == mdriver.XAxis:
            dir = self.m_xScanDir
            self.m_xScanIndex += 1
            print "XScan:",  self.m_xAxisPos, self.m_yAxisPos
        elif axis == mdriver.YAxis:
            self.m_xScanDir *= -1
            self.m_scanData.append(self.m_scanDataByRow)
            drawData = copy(self.m_scanDataByRow)
            if self.m_xScanDir == -1:
                drawData.reverse()
            #draw c scan image
            cScanDrawDataT = self.m_cScanDrawData.T
            cScanDrawDataT[self.m_yScanIndex] = drawData
            self.m_cscanWidget.drawImg(cScanDrawDataT)        
            print self.m_xScanIndex, self.m_yScanIndex
            print "YScan:", self.m_xAxisPos, self.m_yAxisPos
            self.m_scanDataByRow = []
            dir = self.m_yScanDir
            self.m_xScanIndex = 0
            self.m_yScanIndex += 1
        self.pMove(axis, dir)
    def genCScanData(self, pop = False):
        self.m_scanData
    def checkXScanMove(self):
        if self.m_xScanDir == 1 and abs(self.m_nowPos['x'] - self.m_scanEndPos['x']) < mdriver.PRECISION:
            print "+", self.m_nowPos['x'], self.m_scanEndPos['x']
            #self.m_xScanDir *= -1
            return False
        if self.m_xScanDir == -1 and abs(self.m_nowPos['x'] - self.m_scanStartPos['x']) < mdriver.PRECISION:
            print "-", self.m_nowPos['x'],  self.m_scanStartPos['x']
            #self.m_xScanDir *= -1
            return False
        return True
    def checkScanMove(self):
        xDelta = abs(self.m_nowPos['x'] - self.m_scanEndPos['x'])
        yDelta = abs(self.m_nowPos['y'] - self.m_scanEndPos['y'])
        if xDelta < mdriver.PRECISION and yDelta < mdriver.PRECISION:
            self.m_readyForScan = False
            print self.m_scanData
            return True
        return False
    
    def returnStartPos(self):
        self.moveToPosByAxis(mdriver.XAxis, self.m_scanStartPos, self.startMove)
    
    def startScanMove(self):
        self.m_readyForScan = True
        self.m_xScanDir = 1
        self.m_xScanIndex = 0
        self.m_yScanIndex = 0
        self.m_scanData = []
        self.m_scanDataByRow = []
        if self.m_scanStartPos['x'] - self.m_scanEndPos['x'] > 0:
            self.m_xScanDir = -1
        self.m_yScanDir = 1
        if self.m_scanStartPos['x'] - self.m_scanEndPos['x'] > 0:
            self.m_yScanDir = -1
        self.m_scanDataFrom = 0
        self.m_scanDataTo = 0
        if len(self.m_gateSet) > 0:
            tFrom = self.m_gateSet[self.m_gateIndex].m_start
            tTo = self.m_gateSet[self.m_gateIndex].m_start + self.m_gateSet[self.m_gateIndex].m_len
            self.m_scanDataFrom = self.parseTime(tFrom)
            self.m_scanDataTo = self.parseTime(tTo)
    
    def startScan(self):
        self.returnStartPos()
    def initSgn(self):
        self.m_xMinus.pressed.connect(self.xStartMoveMinus)
        self.m_xMinus.released.connect(self.xStop)
        self.m_xPlus.pressed.connect(self.xStartMovePlus)
        self.m_xPlus.released.connect(self.xStop)
        
        self.m_yMinus.pressed.connect(self.yStartMoveMinus)
        self.m_yMinus.released.connect(self.yStop)
        self.m_yPlus.pressed.connect(self.yStartMovePlus)
        self.m_yPlus.released.connect(self.yStop)
        
        self.m_zMinus.pressed.connect(self.zStartMoveMinus)
        self.m_zMinus.released.connect(self.zStop)
        self.m_zPlus.pressed.connect(self.zStartMovePlus)
        self.m_zPlus.released.connect(self.zStop)
        
        self.m_setStartPos.clicked.connect(self.setScanStartPos)
        self.m_setEndPos.clicked.connect(self.setScanEndPos)
        self.m_startScan.clicked.connect(self.startScan)
        self.m_emgStop.clicked.connect(self.emgStopMove)
        self.m_stop.clicked.connect(self.stopAllMove)
if __name__ == "__main__":
    import sys
    print sys.path
    app = QtGui.QApplication(sys.argv)
    ui = Code_MainWindow()
    ui.show()
#sys.exit(app.exec_())
    
        
    
    
    
    
    
    
        
