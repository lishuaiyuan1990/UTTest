# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pci import *
import sys
print sys.path
MAX_GATE_NUM = 6
COLORLIST = ["001", "010", "100", "110", "011", "101"]
from Ui_MplMainWindow import Ui_MainWindow
class Gate(object):
    def __init__(self, color = QColor(255, 0, 0), start = 0, len = 1):
        self.m_color = color
        self.m_start = start
        self.m_len = len

class Code_MainWindow(Ui_MainWindow):
    def __init__(self,  parent = None):
        super(Code_MainWindow,  self).__init__(parent)
        self.setupUi(self)
        self.m_dsbDelay.valueChanged.connect(self.setDelay)
        header = QStringList()
        header.append(QString.fromUtf8(("闸门颜色")))# << "End" << "Len";  
        header.append(QString.fromUtf8(("闸门起始(us)")))#
        header.append(QString.fromUtf8(("闸门终止(us)")))#
        header.append(QString.fromUtf8(("闸门宽度(us)")))#
        
        self.m_gateTable.setHorizontalHeaderLabels(header)
        self.m_gateSet = []
        self.m_colorSet = []
        self.m_addGateBtn.clicked.connect(self.addGate)
        self.m_rmGateBtn.clicked.connect(self.rmGate)
    def rmGate(self):
        row = self.m_gateTable.currentRow()
        self.m_gateTable.removeRow(row)
        self.m_colorSet.pop(row)
        self.m_gateSet.pop(row)
    def addGate(self):
        gate = self.genGate()
        self.m_gateSet.append(gate)
        self.m_colorSet.append(gate.m_color)
        self.m_gateTable.setRowCount(self.m_gateTable.rowCount() + 1)
        colCount = self.m_gateTable.columnCount()
        curRow = self.m_gateTable.rowCount() - 1
        print curRow
        item = QTableWidgetItem("")
        item.setBackground(QBrush(gate.m_color))
        item.setFlags(Qt.NoItemFlags)
        self.m_gateTable.setItem(curRow,0, item)
        self.m_gateTable.setCellWidget(curRow,1, QDoubleSpinBox(self.m_gateTable))
        self.m_gateTable.setCellWidget(curRow,2, QDoubleSpinBox(self.m_gateTable))
        self.m_gateTable.setCellWidget(curRow,3, QDoubleSpinBox(self.m_gateTable))
        #for i in range(0, curRow + 1):
        #    self.m_gateTable.itemAt(i, 0).setBackground(QBrush(gate.m_color))
        #    print i
    def genColor(self):
        for item in COLORLIST:
            color = QColor(255 * int(item[0]), 255 * int(item[1]), 255 * int(item[2]))
            if color not in self.m_colorSet:
                return color
    def genGate(self):
        color = self.genColor()
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
    
        
    
    
    
    
    
    
        
