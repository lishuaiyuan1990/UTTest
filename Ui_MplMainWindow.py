# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\eric6ProDir\Demo\MplMainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from widget.gatetablewidget import GateTableWidget
from widget.mplcanvaswraper import MplCanvasCWraper, MplCanvasWraper

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1382, 625)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.layoutWidget = QtGui.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 9, 641, 441))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.m_mplCanvas = MplCanvasWraper(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m_mplCanvas.sizePolicy().hasHeightForWidth())
        self.m_mplCanvas.setSizePolicy(sizePolicy)
        self.m_mplCanvas.setObjectName(_fromUtf8("m_mplCanvas"))
        self.verticalLayout.addWidget(self.m_mplCanvas)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.m_dsbDelay = QtGui.QSpinBox(self.layoutWidget)
        self.m_dsbDelay.setMaximum(255)
        self.m_dsbDelay.setObjectName(_fromUtf8("m_dsbDelay"))
        self.horizontalLayout.addWidget(self.m_dsbDelay)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.layoutWidget1 = QtGui.QWidget(self.centralWidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 460, 641, 151))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.m_gateTable = GateTableWidget(self.layoutWidget1)
        self.m_gateTable.setMouseTracking(False)
        self.m_gateTable.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.m_gateTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.m_gateTable.setRowCount(0)
        self.m_gateTable.setColumnCount(5)
        self.m_gateTable.setObjectName(_fromUtf8("m_gateTable"))
        self.horizontalLayout_3.addWidget(self.m_gateTable)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.m_addGateBtn = QtGui.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.m_addGateBtn.setFont(font)
        self.m_addGateBtn.setObjectName(_fromUtf8("m_addGateBtn"))
        self.verticalLayout_2.addWidget(self.m_addGateBtn)
        self.m_rmGateBtn = QtGui.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.m_rmGateBtn.setFont(font)
        self.m_rmGateBtn.setObjectName(_fromUtf8("m_rmGateBtn"))
        self.verticalLayout_2.addWidget(self.m_rmGateBtn)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.m_cscanWidget = MplCanvasCWraper(self.centralWidget)
        self.m_cscanWidget.setGeometry(QtCore.QRect(670, 10, 691, 601))
        self.m_cscanWidget.setObjectName(_fromUtf8("m_cscanWidget"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "延迟(us)", None))
        self.m_addGateBtn.setText(_translate("MainWindow", "添加闸门", None))
        self.m_rmGateBtn.setText(_translate("MainWindow", "删除闸门", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

