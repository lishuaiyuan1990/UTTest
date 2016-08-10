from PyQt4 import QtGui, QtCore
from pci import *
import sys
print sys.path

from Ui_MplMainWindow import Ui_MainWindow
class Code_MainWindow(Ui_MainWindow):
    def __init__(self,  parent = None):
        super(Code_MainWindow,  self).__init__(parent)
        self.setupUi(self)
        self.m_dsbDelay.valueChanged.connect(self.setDelay)
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

sys.exit(app.exec_())
    
        
    
    
    
    
    
    
        
