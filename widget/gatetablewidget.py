# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Gate(object):
    def __init__(self, color = QColor(255, 0, 0), start = 0.0, len = 1.0, threshold = 30.0):
        self.m_color = color
        self.m_start = start
        self.m_len = len
        self.m_threshold = threshold
    def reset(self):
        self.m_start = 0
        self.m_len = 0
        self.m_threshold = 0

class GateTableWidgetItem(QTableWidgetItem):
    def __init__(self, parent):
        QTableWidgetItem.__init__(self)
    def setValue(self, d):
        self.setData(Qt.DisplayRole, d)
        self.setData(Qt.EditRole, d)
        
    def getValue(self):
        return self.data(Qt.DisplayRole).toDouble()
    
class GateTableWidget(QTableWidget):
    gateInfoChanged = pyqtSignal(float)
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.itemChanged.connect(self.updateItemData)
        #self.setSelectionBehavior(0)
    def setGateHeaderInfo(self):
        header = QStringList()
        header.append(QString.fromUtf8(("闸门颜色")))# << "End" << "Len";  
        header.append(QString.fromUtf8(("闸门起始(us)")))#
        header.append(QString.fromUtf8(("闸门宽度(us)")))#
        header.append(QString.fromUtf8(("闸门阈值")))#
        self.setHorizontalHeaderLabels(header)
    
    def updateItemData(self, item):
        str = item.text()
        if not str:
            return
        value = str.toDouble()
        if value[1]:
            item.setValue(value[0])
            self.gateInfoChanged.emit(value[0])
    
    
