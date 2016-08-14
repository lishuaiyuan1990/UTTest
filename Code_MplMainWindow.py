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
from mplcanvaswraper import Gate
import gatetablewidget 
from gatetablewidget import GateTableWidgetItem

class Code_MainWindow(Ui_MainWindow):
    def __init__(self,  parent = None):
        super(Code_MainWindow,  self).__init__(parent)
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
        self.currentRow = -1
        self.currentCol = -1
        self.m_clickMark = False
    
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
        self.m_gateTable.itemChanged.disconnect(self.syncGateInfo)
        gate = self.genGate()
        if not gate:
            return None
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
    
        
    
    
    
    
    
    
        
