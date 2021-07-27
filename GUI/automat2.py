from __future__ import print_function
import threading
import time

import sys
from mainwindow import *
from Fluigent.SDK import *
import random
from pop2 import ui2, Dialog
from PyQt5 import QtCore


from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_get_valveChannelCount
from Fluigent.SDK import fgt_get_valveRange, fgt_get_valvePosition, fgt_set_valvePosition

from Fluigent.SDK import fgt_get_sensorValue, fgt_get_sensorRange
from Fluigent.SDK import fgt_set_sensorRegulation, fgt_set_pressure



class MonThread (threading.Thread):
    def __init__(self, ui,ui2):      # jusqua = donnée supplémentaire
        threading.Thread.__init__(self)  # ne pas oublier cette ligne
        # (appel au constructeur de la classe mère)
        self.ui = ui
        self.etat = True

    def run(self):

        while self.etat:
            x = 0
            if (self.ui.radioButton.isChecked() == True):

                while x < int(ui2.spinBox.value()) :

                    for i in range(ui2.tableWidget.rowCount()):

                        self.type = ui2.tableWidget.item(i,0).text()
                        self.channel = int(ui2.tableWidget.item(i,1).text())
                        self.temps = float(ui2.tableWidget.item(i,2).text())
                        self.pression = float(ui2.tableWidget.item(i,3).text())


                        if (self.type == 'pressure'):
                            fgt_set_pressure(self.channel-1, self.pression)
                        if (self.type == 'flow'):
                            fgt_set_sensorRegulation(0, self.channel-1, self.pression)

                        fgt_set_valvePosition(0,self.channel-1)

                        if (self.channel == 1):
                            self.ui.radioButton_5.setChecked(True)
                            self.ui.radioButton_6.setChecked(True)
                        if (self.channel == 2):
                            self.ui.radioButton_7.setChecked(True)
                            self.ui.radioButton_4.setChecked(True)
                        if (self.channel == 3):
                            self.ui.radioButton_8.setChecked(True)
                            self.ui.radioButton_3.setChecked(True)
                        if (self.channel == 4):
                            self.ui.radioButton_9.setChecked(True)
                            self.ui.radioButton_2.setChecked(True)

                        if (self.ui.radioButton.isChecked() == False):
                            break

                        time.sleep(self.temps)


                    x = x+1
                fgt_set_pressure(0, 0)
                fgt_set_pressure(1, 0)
                fgt_set_pressure(2, 0)
                fgt_set_pressure(3, 0)
                self.etat = False

    def stop(self):
        self.etat = False
