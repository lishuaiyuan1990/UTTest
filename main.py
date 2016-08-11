from PyQt4 import QtGui
from Code_MplMainWindow import *
if __name__ == "__main__":
    import sys
    print sys.path
    app = QtGui.QApplication(sys.argv)
    ui = Code_MainWindow()
    ui.show()
sys.exit(app.exec_())
