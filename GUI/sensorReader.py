from mainwindow import ui
from logger import mylog

import serial
import sys
import os
from datetime import datetime
from pyqtgraph.Qt import QtGui, QtCore


class Sample:
    @mylog.catch
    def __init__(self, glucose_value, hour, minute, second, day, month, year):
        """The glucose sample class.

        Attributes:
            glucose_value <float> : The glucose concentration in mM/L.
            hour <int> : The real-time hour of the measure.
            minute <int> : The real-time hour of the measure.
            seconde <int> : The real-time hour of the measure.
            day <int> : The real-time hour of the measure.
            month <int> : The real-time hour of the measure.
            year <int> : The real-time hour of the measure.
        """
        self.glucose_value = glucose_value
        self.hour = hour
        self.minute = minute
        self.second = second
        self.day = day
        self.month = month
        self.year = year

    @mylog.catch
    def data(self):
        """ Returns the sample's attributes in a list. """
        return [self.Num_meas,
                self.glucose_value,
                self.hour,
                self.minute,
                self.second,
                self.day,
                self.month,
                self.year
                ]


class SensorReader:
    @mylog.catch
    def __init__(self,  arduino_port, baudrate):
        """ The sensor reader class. Connects the machine to the arduino via serial port and returns the glucose values.

        Attributes
            arduino_port <char>: The Arduino port path."/dev/ttyACM0" on Linux, and "COM"" on Windows.
            baudrate <int>: The speed of serial data transfert.
        """
        # The sensor controller
        self.switch = False                     # The sensor reader switch
        self.switch_pasteState = False          # Memorizes the last state of switch_pasteState
        self.baudrate = baudrate
        self.arduino_port = arduino_port
        self.ser = serial.Serial()

        self.csv_buff = 0.00                                      # A buffer for data received from the Arduino

        # QTimer - Refreshes the read data
        self.timerReader = QtCore.QTimer()                          # Creates a timer based on the analog clock.
        self.timerReader.timeout.connect(self.connection_verif)     # Verifies the arduino connection with the timer
        self.timerReader.timeout.connect(self.read)                 # Updates the self.csv_buff with the timer
        self.timerReader.start(10)                                  #Starts the timer that sends a signal after 10 (ms)
        # TODO: Find the correct parameter for self.timer.start()

        # The logic behind the UI
        self.logic()

    @mylog.catch
    def switcher(self, *args):
        """ Starts/Stops the serial communication with the Arduino."""

        if (not self.isconnected()):
            mylog.warning("The Arduino is disconnected.\nPlease verify that you have entered the right Serial port address and that the Arduino is well connected to the computer.")
        else:
            if self.switch:             # If the reader is on, turn it off
                self.ser.close()
                self.switch = False
            else:                       # If the reader is off, turn it on
                self.ser = serial.Serial(self.arduino_port, self.baudrate)
                self.switch = True

    @mylog.catch
    def isconnected(self):
        """ Verifies that the Arduino is connected and returns a boolean. """
        return os.path.exists(self.arduino_port)

    @mylog.catch
    def button_checker(self):
        """ Checks/Unchecks the connect button according to the value of self.switch . """
        if self.switch:
            ui.pushButtonSerialConnect.setChecked(True)
        else:
            ui.pushButtonSerialConnect.setChecked(False)

    @mylog.catch
    def connection_verif(self):
        if (not self.isconnected()):                    # Checks if the Arduino got disconnected
            self.ser.close()
            self.switch = False

        if (self.switch_pasteState != self.switch):
            if self.switch:
                mylog.info("The Arduino just got connected to port " + self.arduino_port)
            else:
                mylog.info("The Arduino just got disconnected from port " + self.arduino_port)

        self.switch_pasteState = self.switch
        self.button_checker()                           # Updates the state of Connect button

    @mylog.catch
    def read(self):
        """ Reads data from the serial flow and saves it in self.csv_buff .
        """
        from plotter import rt_plotter                          # To avoid circuilar import
        if rt_plotter.switch:
            if self.switch:
                getData = str(self.ser.readline().decode('latin-1'))
                self.csv_buff = getData[0:][:-2]                # Buffer of data saved in the csv file
                # mylog.trace("Reading ==> " + str(self.csv_buff) +"     from :" + self.arduino_port)
            else:
                mylog.info("The Arduino is disconnected.\nPlease verify that you have entered the right Serial port address and that the Arduino is well connected to the computer.")

# ----------------------------------------------------------------------------------#
    # The logic behind the UI
    @mylog.catch
    def logic(self):
        ui.pushButtonSerialConnect.clicked.connect(self.switcher)         # Handles the connect button.
        ui.comboBoxBaudRates.currentIndexChanged.connect(self.baud)     # Handles the baudrate combobox.

    @mylog.catch
    def baud(self, *args):
        """ Sets self.baudrate to the value of the combobox ui.comboBoxBaudRates."""

        self.baudrate = int(ui.comboBoxBaudRates.currentText())
        mylog.debug("Requested (baudrate = %d)" % (self.baudrate))


# ----------------------------------------------------------------------------------#
# MAIN
arduino_port = "/dev/ttyACM0"                      # Serial port of the Arduino on Linux, change to "COM3" in Windows
baudrate = 9600                                    # TODO: baudrate should be variable

sensorReader = SensorReader(arduino_port, baudrate)     # Creates the SensorReader
