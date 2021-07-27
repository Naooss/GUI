from mainwindow import *

from datetime import datetime
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import random

from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange


class Plotter():
    """ A class to plot graphs. """
    def __init__(self):
        self.x = 0



class RT_Plotter():
    """ A class to plot real-time graphs. """

    def __init__(self,ui,numero_valve):

        self.ui = ui

        # RT_plotter control
        self.switch = False                     # The RT_plotter switch
        self.switch_pasteState = False          # Memorizes the last state of switch
        self.numero = numero_valve

        self.a = 0

        self.graph()
        self.texte()
        self.boxc()
        self.box.toggled.connect(self.switcher)
        self.init()                             # Initializes the RT plotter.



        #QTimer - Refreshes the plot

        self.timerRTplotter = QtCore.QTimer()                        # Creates a timer based on the analog clock.
        self.timerRTplotter.timeout.connect(self.updateplot)         # Updates the plot with the timer
        self.timerRTplotter.start(300)                     # Starts the timer that sends a signal after each self.interval(ms)



    def graph (self):

        if ( self.numero  == 0):
            self.graph = self.ui.graphicsView_ch1
        elif (self.numero  == 1):
            self.graph = self.ui.graphicsView_ch2
        elif (self.numero  == 2):
            self.graph = self.ui.graphicsView_ch3
        elif (self.numero  == 3):
            self.graph = self.ui.graphicsView_ch4


    def texte (self):

        if ( self.numero  == 0):
            self.text = self.ui.textEdit_ch1
        elif (self.numero  == 1):
            self.text = self.ui.lineEdit_ch2
        elif (self.numero  == 2):
            self.text = self.ui.lineEdit_ch3
        elif (self.numero  == 3):
            self.text = self.ui.lineEdit_ch4



    def boxc (self):

        if ( self.numero  == 0):
            self.box = self.ui.radioButton_5
        elif (self.numero  == 1):
            self.box = self.ui.radioButton_4
        elif (self.numero  == 2):
            self.box = self.ui.radioButton_3
        elif (self.numero  == 3):
            self.box = self.ui.radioButton_2



    def init(self, f_plot = 100, timewindow =10.):
        """ Initializes the RT plotter.
        Attributes:
                f_plot <int> : Plotting frequency in Hz.
                timewindow <int> : The shown plot duration in s.
        """
        # Data stuff
        t_plot = 1/f_plot
        self.interval = int(100 * t_plot)                 # Number of points plotted = Plot refreshing period
        self.bufsize = int (timewindow/ t_plot)            # Buffer size
        self.data = np.array([0.00]* self.bufsize)               # Data buffer
        self.x = np.linspace(-timewindow, 0.0, self.bufsize)    # Defining the x-axe marges
        self.y = np.zeros(self.bufsize, dtype =float)           # Defining the y-axe marges
        # pyqtGraph stuff
        self.RT_plt = self.graph                                # Connecting the RT_plotter output to graphicsViewRT
        #self.RT_plt.setLabel("left", "Glucose concentration", "mM/L")   # y label
        self.RT_plt.setLabel("left", "Pression", "mbar")
        self.RT_plt.setLabel("bottom", "Time", "s")                     # x label
        self.RT_curve = self.RT_plt.plot(self.x, self.y, pen='b')                # Plotting the curve self.y = f(self.x). The pen argument is for the color.
        self.RT_plt.setBackground('w')                                 # Change the background to white


    def switcher(self):
        """ Starts/Stops the real-time plot"""
        if (self.box.isChecked() == True):
            self.switch = True
            self.updateplot()
        else:                       # If the plotter is off, turn it on
            self.switch = False




    def updateplot(self):
        """ Updates the plot data ."""

        self.a = fgt_get_pressure(self.numero)
        self.text.setText(str(self.a))

        if self.switch:

            self.data = np.append(self.data, self.a)        # Adds the new value to the buffer
            self.data = np.delete(self.data, 0)                     # Removes the oldest value from the buffer
            self.y[:] = self.data                                   # Copies the buffer into the plotted array
            self.RT_curve.setData(self.x, self.y)                   # Updates the plot
