# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
#from matplotlib.dates import date2num,  MinuteLocator,  SecondLocator,  DateFormatter
#from pci import *
from pci import *

x_resolution = 0.01
x_len = 1000
X_INTERVAL = 0.01

Y_MAX = 100
Y_MIN = -100
X_MIN = X_INTERVAL
X_MAX = 10
X_TICKS = 11

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

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.TEST_CLOCK = 1
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
        self.ax.set_xticks(np.round(np.linspace(X_MIN,  X_MAX,  X_TICKS), 2))
        self.curveObj = None
        self.gateObj = {'#ff0000': None, '#0000ff': None, '#00ff00': None}#, '#00ffff': None, '#ff00ff': None, '#ffff00': None}
        #self.gateObj = {QColor('#FF0000'): None, QColor(0,0,255): None, '#00FF00': None, '#FFFF00': None, '#FF00FF': None, '#00FFFF': None}
    def plot(self,  datax,  datay):
        if self.curveObj is None:
            self.curveObj,  = self.ax.plot(np.array(datax), np.array(datay),  '#EEEE00')
        else:
            self.curveObj.set_data(np.array(datax),  np.array(datay))
        #ticklabels = self.ax.xaxis.get_ticklabels()
        #for tick in ticklabels:
        #for tick in ticklabels:
        #    tick.set_rotation(25)
        self.draw()
    def plotGate(self, gate):  
        datax = [gate.m_start, gate.m_start + gate.m_len]
        datay = [gate.m_threshold, gate.m_threshold]
        self.TEST_CLOCK += 1
        print self.TEST_CLOCK, gate.m_color.name(), gate.m_start, gate.m_len, gate.m_threshold
        colorStr = gate.m_color.name().toLatin1().data()
        if self.gateObj[colorStr] is None:
            self.gateObj[colorStr],  = self.ax.plot(np.array(datax),  np.array(datay), gate.m_color.name().toLatin1().data())
        else:
            self.gateObj[colorStr].set_data(np.array(datax),  np.array(datay))
        self.draw()
    def resetGate(self, gate):
        colorStr = gate.m_color.name().toLatin1().data()
        self.gateObj[colorStr].set_data(np.array([]),  np.array([]))
        self.draw()
        self.gateObj[colorStr] = None
        
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
        self.xdata = np.linspace(X_MIN, X_MAX, 1000)
        #self.xdata = range(X_MIN / x_resolution, X_MAX / x_resolution, X_INTERVAL/x_resolution)
        print len(self.ydata), len(self.xdata)
        self.canvas.plot(self.xdata, self.ydata)
    def drawGate(self, gate):
        self.canvas.plotGate(gate)
    def resetGate(self, gate):
        self.canvas.resetGate(gate)
        
        
        
        
        





















