# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\eric6ProDir\Demo\MplMainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from widget.gatetablewidget import GateTableWidget
from widget.mplcanvaswraper import MplCanvasCWraper, MplCanvasWraper

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
        MainWindow.resize(1330, 636)
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
        self.m_probePara = QtGui.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.m_probePara.setFont(font)
        self.m_probePara.setObjectName(_fromUtf8("m_probePara"))
        self.horizontalLayout_2.addWidget(self.m_probePara)
        self.m_probeBeamPara = QtGui.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.m_probeBeamPara.setFont(font)
        self.m_probeBeamPara.setObjectName(_fromUtf8("m_probeBeamPara"))
        self.horizontalLayout_2.addWidget(self.m_probeBeamPara)
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
        self.m_cscanWidget.setGeometry(QtCore.QRect(670, 10, 641, 441))
        self.m_cscanWidget.setObjectName(_fromUtf8("m_cscanWidget"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(670, 450, 641, 181))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget2 = QtGui.QWidget(self.groupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 30, 621, 141))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtGui.QLabel(self.layoutWidget2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.layoutWidget2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.layoutWidget2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.m_xMinus = QtGui.QPushButton(self.layoutWidget2)
        self.m_xMinus.setObjectName(_fromUtf8("m_xMinus"))
        self.verticalLayout_4.addWidget(self.m_xMinus)
        self.m_yMinus = QtGui.QPushButton(self.layoutWidget2)
        self.m_yMinus.setObjectName(_fromUtf8("m_yMinus"))
        self.verticalLayout_4.addWidget(self.m_yMinus)
        self.m_zMinus = QtGui.QPushButton(self.layoutWidget2)
        self.m_zMinus.setObjectName(_fromUtf8("m_zMinus"))
        self.verticalLayout_4.addWidget(self.m_zMinus)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.m_xPlus = QtGui.QPushButton(self.layoutWidget2)
        self.m_xPlus.setObjectName(_fromUtf8("m_xPlus"))
        self.verticalLayout_5.addWidget(self.m_xPlus)
        self.m_yPlus = QtGui.QPushButton(self.layoutWidget2)
        self.m_yPlus.setObjectName(_fromUtf8("m_yPlus"))
        self.verticalLayout_5.addWidget(self.m_yPlus)
        self.m_zPlus = QtGui.QPushButton(self.layoutWidget2)
        self.m_zPlus.setObjectName(_fromUtf8("m_zPlus"))
        self.verticalLayout_5.addWidget(self.m_zPlus)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 2, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.m_xPos = QtGui.QLabel(self.layoutWidget2)
        self.m_xPos.setObjectName(_fromUtf8("m_xPos"))
        self.verticalLayout_8.addWidget(self.m_xPos)
        self.m_yPos = QtGui.QLabel(self.layoutWidget2)
        self.m_yPos.setObjectName(_fromUtf8("m_yPos"))
        self.verticalLayout_8.addWidget(self.m_yPos)
        self.m_zPos = QtGui.QLabel(self.layoutWidget2)
        self.m_zPos.setObjectName(_fromUtf8("m_zPos"))
        self.verticalLayout_8.addWidget(self.m_zPos)
        self.gridLayout.addLayout(self.verticalLayout_8, 0, 3, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.m_xzStartPos = QtGui.QPushButton(self.layoutWidget2)
        self.m_xzStartPos.setObjectName(_fromUtf8("m_xzStartPos"))
        self.verticalLayout_10.addWidget(self.m_xzStartPos)
        self.m_xzEndPos = QtGui.QPushButton(self.layoutWidget2)
        self.m_xzEndPos.setObjectName(_fromUtf8("m_xzEndPos"))
        self.verticalLayout_10.addWidget(self.m_xzEndPos)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.m_xyStartPos = QtGui.QPushButton(self.layoutWidget2)
        self.m_xyStartPos.setObjectName(_fromUtf8("m_xyStartPos"))
        self.verticalLayout_9.addWidget(self.m_xyStartPos)
        self.m_xyEndPos = QtGui.QPushButton(self.layoutWidget2)
        self.m_xyEndPos.setObjectName(_fromUtf8("m_xyEndPos"))
        self.verticalLayout_9.addWidget(self.m_xyEndPos)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.horizontalLayout_4.addLayout(self.verticalLayout_10)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.m_setStartPos = QtGui.QPushButton(self.layoutWidget2)
        self.m_setStartPos.setObjectName(_fromUtf8("m_setStartPos"))
        self.verticalLayout_6.addWidget(self.m_setStartPos)
        self.m_setEndPos = QtGui.QPushButton(self.layoutWidget2)
        self.m_setEndPos.setObjectName(_fromUtf8("m_setEndPos"))
        self.verticalLayout_6.addWidget(self.m_setEndPos)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.m_startScan = QtGui.QPushButton(self.layoutWidget2)
        self.m_startScan.setObjectName(_fromUtf8("m_startScan"))
        self.verticalLayout_7.addWidget(self.m_startScan)
        self.m_stop = QtGui.QPushButton(self.layoutWidget2)
        self.m_stop.setObjectName(_fromUtf8("m_stop"))
        self.verticalLayout_7.addWidget(self.m_stop)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.m_emgStop = QtGui.QPushButton(self.centralWidget)
        self.m_emgStop.setGeometry(QtCore.QRect(1200, 650, 84, 27))
        self.m_emgStop.setObjectName(_fromUtf8("m_emgStop"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "中国特种设备检测研究院", None))
        self.label.setText(_translate("MainWindow", "延迟(us)", None))
        self.m_probePara.setText(_translate("MainWindow", "探头性能分析", None))
        self.m_probeBeamPara.setText(_translate("MainWindow", "探头声场分析", None))
        self.m_addGateBtn.setText(_translate("MainWindow", "添加闸门", None))
        self.m_rmGateBtn.setText(_translate("MainWindow", "删除闸门", None))
        self.groupBox.setTitle(_translate("MainWindow", "运动控制", None))
        self.label_2.setText(_translate("MainWindow", "水平-X轴", None))
        self.label_3.setText(_translate("MainWindow", "水平-Y轴", None))
        self.label_4.setText(_translate("MainWindow", "垂直-Z轴", None))
        self.m_xMinus.setText(_translate("MainWindow", "<<", None))
        self.m_yMinus.setText(_translate("MainWindow", "<<", None))
        self.m_zMinus.setText(_translate("MainWindow", "<<", None))
        self.m_xPlus.setText(_translate("MainWindow", ">>", None))
        self.m_yPlus.setText(_translate("MainWindow", ">>", None))
        self.m_zPlus.setText(_translate("MainWindow", ">>", None))
        self.m_xPos.setText(_translate("MainWindow", "0", None))
        self.m_yPos.setText(_translate("MainWindow", "0", None))
        self.m_zPos.setText(_translate("MainWindow", "0", None))
        self.m_xzStartPos.setText(_translate("MainWindow", "X-Z扫查起点", None))
        self.m_xzEndPos.setText(_translate("MainWindow", "X-Z扫查终点", None))
        self.m_xyStartPos.setText(_translate("MainWindow", "X-Y扫查起点", None))
        self.m_xyEndPos.setText(_translate("MainWindow", "X-Y扫查终点", None))
        self.m_setStartPos.setText(_translate("MainWindow", "C扫起点", None))
        self.m_setEndPos.setText(_translate("MainWindow", "C扫终点", None))
        self.m_startScan.setText(_translate("MainWindow", "开始扫描", None))
        self.m_stop.setText(_translate("MainWindow", "停止", None))
        self.m_emgStop.setText(_translate("MainWindow", "紧急停止", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

