# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
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

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.TEST_CLOCK = 1
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, axisbg = '#838B83')
        self.ax.grid(True, color = 'w')
        FigureCanvas.__init__(self,  self.fig)
        FigureCanvas.setSizePolicy(self,  QtGui.QSizePolicy.Expanding,  QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax.set_xlabel("time ms", labelpad = -4)

        self.ax.set_ylabel("Amp")
        self.ax.set_xlim(X_MIN,  X_MAX)
        self.ax.set_ylim(Y_MIN,  Y_MAX)
        self.ax.set_xticks(np.round(np.linspace(X_MIN,  X_MAX,  X_TICKS), 2))
        self.curveObj = None
        self.gateObj = {'#ff0000': None, '#0000ff': None, '#00ff00': None}#, '#00ffff': None, '#ff00ff': None, '#ffff00': None}
        #self.gateObj = {QColor('#FF0000'): None, QColor(0,0,255): None, '#00FF00': None, '#FFFF00': None, '#FF00FF': None, '#00FFFF': None}
    
    def setADDelay(self, delay):
        start = delay
        end = delay + X_INTERVAL * x_len
        self.ax.set_xlim(start, end)
        self.ax.set_xticks(np.round(np.linspace(start, end,  X_TICKS), 2))
    
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
        #self.timer.start(500,  self)
        self.m_xStart = X_MIN
        self.m_xEnd = X_MAX
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
        self.xdata = np.linspace(self.m_xStart, self.m_xEnd, 1000)
        #self.xdata = range(X_MIN / x_resolution, X_MAX / x_resolution, X_INTERVAL/x_resolution)
        print len(self.ydata), len(self.xdata)
        self.canvas.plot(self.xdata, self.ydata)
    def syncADDelay(self, delay):
        self.canvas.setADDelay(delay)
        self.m_xStart = delay
        self.m_xEnd = delay + X_INTERVAL * x_len
        
    def drawGate(self, gate):
        self.canvas.plotGate(gate)
        
    def resetGate(self, gate):
        self.canvas.resetGate(gate)

class MplCanvasC(FigureCanvas):
    def __init__(self):
        self.TEST_CLOCK = 1
        self.fig = Figure((100, 100))
        self.fig.clear()
        FigureCanvas.__init__(self, self.fig)
        self.ax = self.fig.add_subplot(111)#, axisbg = '#838B83')
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,  QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        print self.ax.set_xlabel("time ms", labelpad = -15)
        self.ax.set_ylabel("pos")
        #self.ax.set_xticks(np.round(np.linspace(X_MIN,  X_MAX,  X_TICKS), 2))
        self.imgObj = None
        self.img = None
    def initAxis(self, xaxis, yaxis, tick):
        self.ax.set_xlim(xaxis.x(),  xaxis.y())
        self.ax.set_ylim(yaxis.x(),  yaxis.y())
        self.ax.set_xticks(np.round(np.linspace(xaxis.x(),  xaxis.y(),  10), 2))
        self.ax.set_yticks(np.round(np.linspace(yaxis.x(),  yaxis.y(),  10), 2))
        pass
        
    def plot(self, x, y, z):
        
        #self.ax.set_xlim(x.min(), x.max())
        #self.ax.set_ylim(y.min(), y.max())
        #z_max, z_min = np.abs(z).max(), np.abs(z).min()
        z_max, z_min = Y_MAX, 0
        self.fig.clear()
        cax = self.ax.imshow(z)
        #cax = self.ax.imshow(z, vmin = z_min, vmax = z_max, \
        #                     extent = [x.min(), x.max(), y.min(), y.max()], \
        #                     interpolation = 'nearest', origin= 'lower')
        if self.img:
            del self.img
        self.img = cax
        self.fig.colorbar(cax)
        #print "self.ax.imshow"
        #ticklabels = self.ax.xaxis.get_ticklabels()
        #for tick in ticklabels:
        #for tick in ticklabels:
        #    tick.set_rotation(25)
        self.draw()


class MplCanvasCWraper(QWidget):
    def __init__(self, parent):
        self.TEST_CLOCK = 1
        QtGui.QWidget.__init__(self, parent)
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.vbl = QVBoxLayout()
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.vbl.addWidget(self.ntb)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.imgObj = None
        self.axes = self.fig.add_subplot(111)
        self.timer = QtCore.QBasicTimer()
        self.timer.start(500, self)
        
    def initAxis(self, xaxis, yaxis):
        self.axes.set_xlim(xaxis.x(),  xaxis.y())
        self.axes.set_ylim(yaxis.x(),  yaxis.y())
        self.axes.set_xticks(np.round(np.linspace(xaxis.x(),  xaxis.y(),  10), 2))
        self.axes.set_yticks(np.round(np.linspace(yaxis.x(),  yaxis.y(),  10), 2))
        self.axes.grid(False)
        
    def setScanPos(self, posFrom, posTo, step):
        self.scanStep = step
        self.posFrom = posFrom
        self.posTo = posTo
        self.x, self.y = self.genXY()
        xaxis = QPoint(posFrom.x(), posTo.x())
        yaxis = QPoint(posFrom.y(), posTo.y())
        self.xaxis = xaxis
        self.yaxis = yaxis
        #self.initAxis(xaxis, yaxis)
        
    def genXY(self):
        dx, dy = self.scanStep.x(), self.scanStep.y()
        x, y = np.mgrid[slice(self.posFrom.x(), self.posTo.x(), dx), slice(self.posFrom.y(), self.posTo.y(), dy)]
        return [x, y]
        
    def genData(self):
        z = np.random.random(size = self.x.shape) * 100
        return [self.x, self.y, z]
        
    def drawImg(self):
        z_max, z_min = Y_MAX, 0
        [x, y, z] = self.genData()
        #self.fig.clear()
        #self.axes = self.fig.add_subplot(111)
        self.axes.clear()
        self.initAxis(self.xaxis, self.yaxis)
        self.axes.set_xlabel("time ms", labelpad = -2)
        self.axes.set_ylabel("pos")
        if self.imgObj:
            del self.imgObj
        self.imgObj = self.axes.imshow(z, vmin = z_min, vmax = z_max, \
                         extent = [x.min(), x.max(), y.min(), y.max()], \
                         interpolation = 'nearest', origin= 'lower')
        self.canvas.draw()
        #self.fig.colorbar(self.imgObj)
        
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.drawImg()
        else:
            QtGui.QWidget.timerEvent(self, event)
    
    
