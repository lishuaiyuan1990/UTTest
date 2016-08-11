from PyQt4 import QtCore
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
#from matplotlib.dates import date2num,  MinuteLocator,  SecondLocator,  DateFormatter
#from pci import *
from pci import *

X_INTERVAL = 1
Y_MAX = 100
Y_MIN = -100
X_MIN = 0
X_MAX = 1000
X_TICKS = 11

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, axisbg = '#838B83')
        self.ax.grid(True, color = 'w')
        FigureCanvas.__init__(self,  self.fig)
        FigureCanvas.setSizePolicy(self,  QtGui.QSizePolicy.Expanding,  QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax.set_xlabel("time ms")

        self.ax.set_ylabel("Amp")
        self.ax.set_xlim(X_MIN,  X_MAX)
        self.ax.set_ylim(Y_MIN,  Y_MAX)
        self.ax.set_xticks(np.linspace(X_MIN,  X_MAX,  X_TICKS))
        self.curveObj = None
    def plot(self,  datax,  datay):
        if self.curveObj is None:
            self.curveObj,  = self.ax.plot(np.array(datax),  np.array(datay),  '#EEEE00')
        else:
            self.curveObj.set_data(np.array(datax),  np.array(datay))
        ticklabels = self.ax.xaxis.get_ticklabels()
        for tick in ticklabels:
            tick.set_rotation(25)
        self.draw()
        

class MplCanvasWraper(QtGui.QWidget):
    def __init__(self,  parent):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.ntb = NavigationToolbar(self.canvas,  parent)
        self.vbl.addWidget(self.ntb)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.dataX = []
        self.dataY = []
        openDevice()
        self.timer = QtCore.QBasicTimer()
        self.timer.start(500,  self)
        #self.initDataGenerator()
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.draw()
        else:
            QtGui.QWidget.timerEvent(self, event)
    def startPlot(self):
        self.__generating = True    
    
    def pausePlot(self):
        self.__generating = False
        pass
        
    def releasePlot(self):
         self.__exit  = True

    def draw(self):
        newdata = collectData()
        self.ydata = newdata
        self.xdata = range(X_MIN, X_MAX, X_INTERVAL)
        self.canvas.plot(self.xdata, self.ydata)
        
        
        
        
        





















