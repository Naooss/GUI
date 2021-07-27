from mainwindow import ui
from logger import mylog
from sensorReader import sensorReader
from file_manag import file_manager as fm

import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class SensorWriter:
    """The sensor writer class. Takes parameters' values from the GUI and sends them to the Arduino. """
    @mylog.catch
    def __init__(self):

        self.f_ech = 50                  # Sampling frequency (Hz)
        self.gain1 = 75                  # gain1
        self.gain2 = 25                  # gain2

        self.init()
        # The logic behind the UI
        self.logic()

    @mylog.catch
    def init(self):
        # Initializes f_ech slider and LineEditF_ech
        ui.lineEditF_ech.setText(str(self.f_ech))
        ui.horizontalSliderF_ech.setValue(self.f_ech)
        # Initializes gain1 slider and LineEditGain1
        ui.lineEditGain1.setText(str(self.gain1))
        ui.horizontalSliderGain1.setValue(self.gain1)
        # Initializes gain2 slider and LineEditGain2
        ui.lineEditGain2.setText(str(self.gain2))
        ui.horizontalSliderGain2.setValue(self.gain2)

    @mylog.catch
    def logic(self):
        # f_ech
        ui.horizontalSliderF_ech.valueChanged.connect(self.change_f_samp)
        ui.lineEditF_ech.returnPressed.connect(self.change_slider_fsamp)

        # gain1
        ui.horizontalSliderGain1.valueChanged.connect(self.change_gain1)
        ui.lineEditGain1.returnPressed.connect(self.change_slider_gain1)

        # gain2
        ui.horizontalSliderGain2.valueChanged.connect(self.change_gain2)
        ui.lineEditGain2.returnPressed.connect(self.change_slider_gain2)

    @mylog.catch
    def change_f_samp(self, *args):
        """ Sets f_ech and lineEditF_ech.text() to the sliders' value. """
        self.f_ech = str(ui.horizontalSliderF_ech.value())
        ui.lineEditF_ech.setText(self.f_ech)
        self.f_ech = int(self.f_ech)
        mylog.debug("Requested (f_ech = %d)" % (self.f_ech))
        # Updates the config file
        key = ("parameters", "f_ech")
        fm.current_manip.config.update(key, self.f_ech)

    @mylog.catch
    def change_gain1(self, *args):
        """ Sets gain1 and lineEditGain1.text() to the slider's value. """
        self.gain1 = str(ui.horizontalSliderGain1.value())
        ui.lineEditGain1.setText(self.gain1)
        self.gain1 = int(self.gain1)
        mylog.debug("Requested (gain1 = %d)" % (self.gain1))
        # Updates the config file
        key = ("parameters", "gain1")
        fm.current_manip.config.update(key, self.gain1)

    @mylog.catch
    def change_gain2(self, *args):
        """ Sets gain2 and lineEditGain2.text() to the slider's value. """
        self.gain2 = str(ui.horizontalSliderGain2.value())
        ui.lineEditGain2.setText(self.gain2)
        self.gain2 = int(self.gain2)
        mylog.debug("Requested (gain2 = %d)" % (self.gain2))
        # Updates the config file
        key = ("parameters", "gain2")
        fm.current_manip.config.update(key, self.gain2)

    @mylog.catch
    def change_slider_fsamp(self, *args):
        """ Sets f_ech and the slider's value to lineEditF_ech.text() """
        self.f_ech = int(ui.lineEditF_ech.text())
        ui.horizontalSliderF_ech.setValue(self.f_ech)

    @mylog.catch
    def change_slider_gain1(self, *args):
        """ Sets gain1 and the slider's value to lineEditGain1.text() """
        self.gain1 = int(ui.lineEditGain1.text())
        ui.horizontalSliderGain1.setValue(self.gain1)

    @mylog.catch
    def change_slider_gain2(self, *args):
        """ Sets gain2 and the slider's value to lineEditGain2.text() """
        self.gain2 = int(ui.lineEditGain2.text())
        ui.horizontalSliderGain2.setValue(self.gain2)


# ----------------------------------------------------------------------------------#
# MAIN
sensorWriter = SensorWriter()                         # Creates the SensorWriter
