# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\eric6ProDir\Demo\ProbeBeam.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from widget.mplcanvaswraper import MplCanvasCWraper

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

class Ui_Dialog(QtGui.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(828, 637)
        Dialog.setSizeGripEnabled(True)
        self.m_xyScanWidget = MplCanvasCWraper(Dialog)
        self.m_xyScanWidget.setGeometry(QtCore.QRect(20, 340, 381, 281))
        self.m_xyScanWidget.setObjectName(_fromUtf8("m_xyScanWidget"))
        self.m_xzScanWidget = MplCanvasCWraper(Dialog)
        self.m_xzScanWidget.setGeometry(QtCore.QRect(20, 30, 381, 281))
        self.m_xzScanWidget.setObjectName(_fromUtf8("m_xzScanWidget"))
        self.m_yzScanWidget = MplCanvasCWraper(Dialog)
        self.m_yzScanWidget.setGeometry(QtCore.QRect(420, 30, 381, 281))
        self.m_yzScanWidget.setObjectName(_fromUtf8("m_yzScanWidget"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 320, 181, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 181, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(420, 10, 181, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "垂直声束方向X-Y平面C扫图像", None))
        self.label_3.setText(_translate("Dialog", "平行声束方向X-Z平面C扫图像", None))
        self.label_4.setText(_translate("Dialog", "平行声束方向Y-Z平面C扫图像", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

