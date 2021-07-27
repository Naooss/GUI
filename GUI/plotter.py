import mainwindow
from mainwindow import ui
from logger import mylog
from sensorReader import sensorReader, Sample
from sensorWriter import sensorWriter
from file_manag import file_manager as fm

from datetime import datetime
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class Plotter():
    """ A class to plot graphs. """
    def __init__(self):
        self.x = 0


class RT_Plotter():
    """ A class to plot real-time graphs. """
    @mylog.catch
    def __init__(self):
        self.threadpool = QtCore.QThreadPool()

        # RT_plotter control
        self.switch = False                 # The RT_plotter switch
        self.switch_pasteState = False      # Memorizes the last state of switch

        # Initializes the RT plotter.
        self.init()

        # The logic behind the UI
        self.logic()

        self.worker = self.run()
        self.worker.timerRTplotter.start(10)

        # QTimer - Refreshes the plot
        sensorReader.timerReader.timeout.connect(self.reader_verif)  # Checks if screenshot turned off

        self.timerRT = QtCore.QTimer()
        self.timerRT.timeout.connect(self.updateRTplot)
        self.timerRT.start(10)         # NOTE: Minimum value is 3, otherwhise the GUI will freeze

        self.timerfull = QtCore.QTimer()
        self.timerfull.timeout.connect(self.updateFullplot)
        self.timerfull.start(1000)         # NOTE: Minimum value is 3, otherwhise the GUI will freeze

    def run(self):
        worker = Worker(self.updatedata)
        self.threadpool.start(worker)
        return worker

    @mylog.catch
    def init(self, f_plot=100, timewindow=90.):
        """ Initializes the RT plotter.

        Attributes:
                f_plot <int> : Plotting frequency in Hz.
                timewindow <int> : The shown plot duration in s.
        """
        # Data stuff
        # RT data
        t_plot = 1/f_plot
        self.interval = int(100 * t_plot)                 # Number of points plotted = Plot refreshing period
        self.bufsize = int(timewindow / t_plot)            # Buffer size
        self.rtdata = np.array([0.00] * self.bufsize)               # RT Data buffer
        self.x = np.linspace(-timewindow, 0.0, self.bufsize)    # Defining the x-axe marges
        self.y = np.zeros(self.bufsize, dtype=float)           # Defining the y-axe marges
        # Full data
        self.full_y = [0.00]                                 # Full data buffer
        self.full_x = [0]
        # pyqtGraph stuff
        self.RT_plt = ui.graphicsViewRT                                 # Connecting the RT_plotter output to graphicsViewRT
        self.full_plt = ui.graphicsViewRT_full

        # RT plot
        # self.RT_plt.setLabel("left", "Glucose concentration", "mM/L")   # y label
        self.RT_plt.setLabel("left", "Voltage", "mV")
        self.RT_plt.setLabel("bottom", "Time", "s")                     # x label
        self.RT_curve = self.RT_plt.plot(self.x, self.y, pen='y')                # Plotting the curve self.y = f(self.x). The pen argument is for the color.
        # self.RT_plt.setBackground('w')                                 # Change the background to white

        # Full plot
        # self.full_plt.setLabel("left", "Glucose concentration", "mM/L")   # y label
        self.full_plt.setLabel("left", "Voltage", "mV")
        self.full_plt.setLabel("bottom", "Time", "s")                     # x label
        self.full_curve = self.full_plt.plot(self.full_x, self.full_y, pen='g')                # Plotting the curve self.y = f(self.x). The pen argument is for the color.
        # self.full_plt.setBackground('w')                                 # Change the background to white

    @mylog.catch
    def switcher(self, *args):
        """ Starts/Stops the real-time plot"""
        if (not sensorReader.switch):
            mylog.info("Impossible to plot, the sensorReader is disconnected")
        else:
            if self.switch:             # If the plotter is on, turn it off
                self.switch = False
            else:                       # If the plotter is off, turn it on
                self.switch = True

    @mylog.catch
    def readerOn(self):
        """ Verifies that the sensorReader is on """
        return sensorReader.switch

    @mylog.catch
    def button_checker(self):
        """ Checks/Unchecks the connect button according to the value of self.switch . """
        if self.switch:
            ui.pushButtonDisableTableLog.setChecked(True)
        else:
            ui.pushButtonDisableTableLog.setChecked(False)

    @mylog.catch
    def reader_verif(self):
        if (not self.readerOn()):                   # Checks if the Arduino got disconnected
            self.switch = False

        if (self.switch_pasteState != self.switch):
            if self.switch:
                mylog.info("RT_plotter just started plotting. ")
            else:
                mylog.info("RT_plotter just stopped plotting. ")

        self.switch_pasteState = self.switch
        self.button_checker()                       # Updates the state of Enable button

    @mylog.catch
    def getdata(self):
        """ Gets the data from sensorReader, and returns a sample from it """
        if self.switch:
            glucose_value = float(sensorReader.csv_buff)                     # Reads the data from sensorReader
            now = datetime.now()
            hour = int(now.strftime("%H"))
            minute = int(now.strftime("%M"))
            second = int(now.strftime("%S"))
            day = int(now.strftime("%d"))
            month = int(now.strftime("%m"))
            year = int(now.strftime("%Y"))
            sample = Sample(glucose_value, hour, minute, second, day, month, year)
            if (not fm.current_manip.empty):
                fm.current_manip.csv.append(sample, fm.current_manip.empty)     # Saves data in the csv file
            return sample

    @mylog.catch
    def updateRTdata(self):
        """ Updates the plot data ."""
        if self.switch:
            sample = self.getdata()
            self.rtdata = np.append(self.rtdata, sample.glucose_value)        # Adds the new value to the buffer
            self.rtdata = np.delete(self.rtdata, 0)                     # Removes the oldest value from the buffer
            self.y[:] = self.rtdata                                   # Copies the buffer into the plotted array

    @mylog.catch
    def updatefulldata(self):
        """ Updates the plot data ."""
        if self.switch:
            y = self.y[-1]
            x = self.full_x[-1] + 1
            self.full_y.append(y)        # Adds the new value to the buffer
            self.full_x.append(x)

    @mylog.catch
    def updatedata(self):
        """ Updates data for the RT-plot and the full plot."""
        self.updateRTdata()
        self.updatefulldata()

    @mylog.catch
    def updateRTplot(self):
        """ Updates the RT graph. """
        if self.switch:
            self.RT_curve.setData(self.x, self.y)                   # NOTE: updateRTplot is separated from updateRTdata because it's only possible to update the GUI on the main thread

    @mylog.catch
    def updateFullplot(self):
        """ Updates the RT graph. """
        if self.switch:
            self.full_curve.setData(self.full_x, self.full_y)                   # NOTE: updateFullplot is separated from updateRTdata because it's only possible to update the GUI on the main thread

    def screenshot(self):
        """ Takes a screenshot of the plot when the user presses the comment button. """
        exporter = pg.exporters.ImageExporter(self.RT_plt)          # Create an exporter instance with the item to export as an argument
        exporter.parameters()['width'] = 370                        # It also affects height parameter

        now = datetime.now()
        name = now.strftime("comment__%d/%m/%Y__H:%M:%S")

        exporter.export(name)                                       # Save to files

# ----------------------------------------------------------------------------------#
    # The logic behind the UI
    @mylog.catch
    def logic(self):
        ui.pushButtonDisableTableLog.clicked.connect(self.switcher)

    @mylog.catch
    def clear(self, *args):
        self.data = np.array([0.00]*self.bufsize)
        mylog.info("Plot buffer cleared")


class Worker(QtCore.QRunnable):
    def __init__(self, bgProcess):
        super(Worker, self).__init__()
        self.bgProcess = bgProcess
        self.signals = WorkerSignals()

        self.timerRTplotter = QtCore.QTimer()                        # Creates a timer based on the analog clock.
        self.timerRTplotter.timeout.connect(self.bgProcess)         # Updates the plot with the timer

    @QtCore.pyqtSlot()
    def run(self):
        self.signals.finished.emit()


class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal()


# ----------------------------------------------------------------------------------#
# MAIN
rt_plotter = RT_Plotter()                                       # Creates the RT_plotter and starts real-time plotting
