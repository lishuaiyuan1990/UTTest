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
Y_MIN = 0
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
        self.ax.set_xlabel("time us", labelpad = -4)
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
        self.timer.start(500,  self)
        self.m_xStart = X_MIN
        self.m_xEnd = X_MAX
        self.m_rawData = None
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
        self.m_rawData = np.array(collectData())
        #self.m_rawData = (self.m_rawData - 50) * 2
        self.ydata = np.array(self.m_rawData)
        self.xdata = np.linspace(self.m_xStart, self.m_xEnd, 1000)
        #self.xdata = range(X_MIN / x_resolution, X_MAX / x_resolution, X_INTERVAL/x_resolution)
        #print len(self.ydata), len(self.xdata)
        self.canvas.plot(self.xdata, self.ydata)
    def syncADDelay(self, delay):
        self.canvas.setADDelay(delay)
        self.m_xStart = delay
        self.m_xEnd = delay + X_INTERVAL * x_len
        
    def drawGate(self, gate):
        self.canvas.plotGate(gate)
        
    def resetGate(self, gate):
        self.canvas.resetGate(gate)
        
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
        #self.timer.start(500, self)
        self.colorBarMark = False
        
    def initAxis(self, xaxis, yaxis):
        self.axes.set_xlim(xaxis.x(),  xaxis.y())
        self.axes.set_ylim(yaxis.x(),  yaxis.y())
        self.axes.set_xticks(np.round(np.linspace(xaxis.x(),  xaxis.y(),  10), 2))
        self.axes.set_yticks(np.round(np.linspace(yaxis.x(),  yaxis.y(),  10), 2))
        self.axes.grid(False)
    def setScanAxis(self, x, y):
        self.xAxis = x
        self.yAxis = y
    def setScanPos(self, posFrom, posTo, step):
        self.scanStep = step
        self.posFrom = posFrom
        self.posTo = posTo
        self.x, self.y = self.genXY()
        xaxis = QPoint(posFrom[self.xAxis], posTo[self.xAxis])
        yaxis = QPoint(posFrom[self.yAxis], posTo[self.yAxis] - self.scanStep)
        self.xaxis = xaxis
        self.yaxis = yaxis
        #self.initAxis(xaxis, yaxis)
        
    def genXY(self):
        dx, dy = self.scanStep, self.scanStep
        if self.posFrom[self.xAxis] - self.posTo[self.xAxis] < 0:
            xData = slice(self.posFrom[self.xAxis], self.posTo[self.xAxis] + dx, dx)
        elif self.posFrom[self.xAxis] - self.posTo[self.xAxis] > 0:
            xData = slice(self.posTo[self.xAxis], self.posFrom[self.xAxis] + dx, dx)
        if self.posFrom[self.yAxis] - self.posTo[self.yAxis] < 0:
            yData = slice(self.posFrom[self.yAxis], self.posTo[self.yAxis], dy)
        elif self.posFrom[self.yAxis] - self.posTo[self.yAxis] > 0:
            yData = slice(self.posTo[self.yAxis], self.posFrom[self.yAxis], dy)
        x, y = np.mgrid[xData, yData]
        return [x, y]
        
    def genData(self, data):
        #z = np.random.random(size = self.x.shape) * 100
        z = data
        #print "ZSHAPE: ", z.shape
        return [self.x, self.y, z]
        
    def drawImg(self, data):
        z_max, z_min = Y_MAX, 0
        [x, y, z] = self.genData(data)
        #self.fig.clear()
        #self.axes = self.fig.add_subplot(111)
        self.axes.clear()
        self.initAxis(self.xaxis, self.yaxis)
        self.axes.set_xlabel("mm", labelpad = -2)
        self.axes.set_ylabel("mm")
        if self.imgObj:
            del self.imgObj
        self.imgObj = self.axes.imshow(z, vmin = z_min, vmax = z_max, \
                         extent = [x.min(), x.max(), y.min(), y.max()], \
                         interpolation = 'nearest', origin= 'lower')
        self.canvas.draw()
        if not self.colorBarMark:
            self.fig.colorbar(self.imgObj)
            self.colorBarMark = True
        
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.drawImg()
        else:
            QtGui.QWidget.timerEvent(self, event)

class MplCanvasProbeWraper(QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.axes = self.fig.add_subplot(111, axisbg = '#838B83')
        self.axes.grid(True, color = 'w')
        self.axes.set_ylabel("Amp")
        self.curveObj = None
        self.vbl = QVBoxLayout()
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.vbl.addWidget(self.ntb)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.timer = QtCore.QBasicTimer()
        self.m_fs = 100 
        self.m_adDelay = 0
        self.m_rawData = None
        self.m_isFFT = False
        self.m_rawDataMark = False
        self.axes.set_ylim(Y_MIN, Y_MAX)
        self.axes.set_yticks(np.round(np.linspace(Y_MIN, Y_MAX,  8), 2))
        self.timer.start(500, self)
    
    def setADDelay(self, delay):
        self.m_adDelay = delay
        self.rawAxis()
    def setCurve(self, isFFT):
        self.m_isFFT = isFFT
        if self.m_isFFT:
            self.fftAxis()
        else:
            self.rawAxis()
        
    def setData(self, data):
        self.m_rawData = data
        self.m_rawDataMark = True
        datay = np.abs(np.fft.fft(self.m_rawData))
        sign = max(datay)
        datay = datay / sign * Y_MAX
        self.m_fftData = datay[0:len(datay)/2]
        
    def rawAxis(self):
        self.m_isFFT = False
        start = self.m_adDelay
        end = self.m_adDelay + X_INTERVAL * x_len
        self.axes.set_xlabel("us", labelpad = -4)
        self.axes.set_xlim(start, end)
        self.axes.set_xticks(np.round(np.linspace(start, end,  X_TICKS), 2))
        
    def fftAxis(self):
        self.m_isFFT = True
        self.axes.set_xlabel("MHz", labelpad = -4)
        self.axes.set_xlim(0, self.m_fs / 2.0)
        self.axes.set_xticks(np.round(np.linspace(0, self.m_fs / 2.0,  8), 2))
    def genData(self):
        if self.m_isFFT:
            return self.genFFTData()
        else:
            return self.genRawData()
    def genRawData(self):
        start = self.m_adDelay
        end = self.m_adDelay + X_INTERVAL * x_len
        xdata = np.linspace(start, end, 1000)
        return [xdata, self.m_rawData]
    def syncADDelay(self, delay):
        self.canvas.setADDelay(delay)
        self.m_xStart = delay
        self.m_xEnd = delay + X_INTERVAL * x_len
        
    def genFFTData(self):
        if not self.m_rawDataMark:
            return [None, None]
        else:
            self.m_rawDataMark = False
        N = len(self.m_rawData)
        n = np.linspace(0, N - 1, N)
        datax = n / N * self.m_fs
        datay = np.abs(np.fft.fft(self.m_rawData))
        sign = max(datay)
        datay = (datay / sign * Y_MAX)
        self.m_fftData = datay[0:len(datay)/2]
        return [datax[0:len(datax)/2], datay[0:len(datay)/2]]
        
    def plotFFT(self):
        datax, datay = self.genData()
        if datax is None or datay is None:
            return
        if self.curveObj is None:
            self.curveObj,  = self.axes.plot(np.array(datax), np.array(datay),  '#EEEE00')
        else:
            self.curveObj.set_data(np.array(datax),  np.array(datay))
        self.canvas.draw()
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.plotFFT()
        else:
            QtGui.QWidget.timerEvent(self, event)
    
    
