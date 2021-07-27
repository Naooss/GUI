from __future__ import print_function
import sys
from mainwindow import *
from plot2 import *
from plot_debit2 import *
from Fluigent.SDK import *
import random
from pop2 import ui2, Dialog
from PyQt5 import QtCore, QtGui
import threading
import time
from automat2 import*

from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_get_valveChannelCount
from Fluigent.SDK import fgt_get_valveRange, fgt_get_valvePosition, fgt_set_valvePosition

from Fluigent.SDK import fgt_get_sensorValue, fgt_get_sensorRange
from Fluigent.SDK import fgt_set_sensorRegulation, fgt_set_pressure

class pression :

    def __init__(self,ui):

        self.ui = ui
        self.valeur = 0
        self.deb = 0
        self.numero_switch = 0
        self.pressure = 0
        self.etat = True
        self.channel = 0
        self.pression = 0
        self.x =0
        self.count = 1



        self.btngroup1 = QtGui.QButtonGroup()
        self.btngroup2 = QtGui.QButtonGroup()
        self.btngroup3 = QtGui.QButtonGroup()


        self.btngroup1.addButton(self.ui.radioButton_5)
        self.btngroup1.addButton(self.ui.radioButton_4)
        self.btngroup1.addButton(self.ui.radioButton_3)
        self.btngroup1.addButton(self.ui.radioButton_2)



        self.btngroup2.addButton(self.ui.radioButton_6)
        self.btngroup2.addButton(self.ui.radioButton_7)
        self.btngroup2.addButton(self.ui.radioButton_8)
        self.btngroup2.addButton(self.ui.radioButton_9)


        self.btngroup3.addButton(self.ui.radioButton_flow)
        self.btngroup3.addButton(self.ui.radioButton_pressure)


        self.valve = fgt_get_valvePosition(0)

        if (self.valve == 0):
            self.ui.radioButton_6.setChecked(True)

        if (self.valve == 1):
            self.ui.radioButton_7.setChecked(True)

        if (self.valve == 2):
            self.ui.radioButton_8.setChecked(True)

        if (self.valve == 3):
            self.ui.radioButton_9.setChecked(True)




        self.clik()




    def select (self):

        if ( self.btngroup1.checkedButton() == self.ui.radioButton_5):
            self.numero_switch = 0

        elif ( self.btngroup1.checkedButton() == self.ui.radioButton_4):
            self.numero_switch = 1

        elif ( self.btngroup1.checkedButton() == self.ui.radioButton_3):
            self.numero_switch = 2

        elif ( self.btngroup1.checkedButton() == self.ui.radioButton_2):
            self.numero_switch = 3






    def clik (self):
        self.ui.radioButton_5.clicked.connect(self.select)
        self.ui.radioButton_4.clicked.connect(self.select)
        self.ui.radioButton_3.clicked.connect(self.select)
        self.ui.radioButton_2.clicked.connect(self.select)

        self.ui.pushButton_start.clicked.connect(self.init_stop)


        self.ui.doubleSpinBox_ch1.valueChanged.connect(self.set)
        self.ui.doubleSpinBox_ch2.valueChanged.connect(self.set)
        self.ui.doubleSpinBox_ch3.valueChanged.connect(self.set)
        self.ui.doubleSpinBox_ch4.valueChanged.connect(self.set)

        self.ui.doubleSpinBox_fu.valueChanged.connect(self.flow_regulation)

        self.ui.radioButton_6.clicked.connect(self.valve_ouverte_ferme)
        self.ui.radioButton_7.clicked.connect(self.valve_ouverte_ferme)
        self.ui.radioButton_8.clicked.connect(self.valve_ouverte_ferme)
        self.ui.radioButton_9.clicked.connect(self.valve_ouverte_ferme)

        self.ui.pushButton.clicked.connect(self.pop_up)

        ui2.pushButton_2.clicked.connect(self.boutons_pop_cancel)

        ui2.pushButton.clicked.connect(self.boutons_pop_ok)

        ui2.pushButton_3.clicked.connect(self.ajouter_ligne)

        ui2.pushButton_4.clicked.connect(self.supprimer_ligne)

        self.ui.radioButton.clicked.connect(self.prio)


    def init_stop (self):

            fgt_set_pressure(0, 0)
            fgt_set_pressure(1, 0)
            fgt_set_pressure(2, 0)
            fgt_set_pressure(3, 0)
            fgt_close()




    def valve_ouverte_ferme (self):

        if (self.ui.radioButton_5.isChecked() == True):
            fgt_set_valvePosition(0,0)   #(ID,valve_position)


        elif (self.ui.radioButton_4.isChecked() == True):
            fgt_set_valvePosition(0,1)   #(ID,valve_position)


        elif (self.ui.radioButton_3.isChecked() == True):
            fgt_set_valvePosition(0,2)   #(ID,valve_position)


        elif (self.ui.radioButton_2.isChecked() == True):
            fgt_set_valvePosition(0,3)   #(ID,valve_position)




    def set (self):
        if (self.ui.radioButton_pressure.isChecked() == True):

            if (self.numero_switch == 0):
                self.valeur = float(self.ui.doubleSpinBox_ch1.value())
                fgt_set_pressure(0, self.valeur)
            elif (self.numero_switch == 1):
                self.valeur = float(self.ui.doubleSpinBox_ch2.value())
                fgt_set_pressure(1, self.valeur)
            elif (self.numero_switch == 2):
                self.valeur = float(self.ui.doubleSpinBox_ch3.value())
                fgt_set_pressure(2, self.valeur)
            elif (self.numero_switch == 3):
                self.valeur = float(self.ui.doubleSpinBox_ch4.value())
                fgt_set_pressure(3, self.valeur)




    def flow_regulation (self):

        if ( self.ui.radioButton_flow.isChecked() == True):

            self.deb = float(self.ui.doubleSpinBox_fu.value())
            fgt_set_sensorRegulation(0, self.numero_switch, self.deb)





    def pop_up(self):
        Dialog.open()





    def boutons_pop_ok(self):
        m = MonThread(ui,ui2)          # crée le thread
        m.start()                  # démarre le thread,
        Dialog.close()




    def boutons_pop_cancel(self):
        ui2.tableWidget.clearContents()
        Dialog.close()




    def ajouter_ligne(self):
        ui2.tableWidget.insertRow(self.count)
        self.count = self.count + 1



    def supprimer_ligne(self):
        ui2.tableWidget.removeRow(self.count - 1)
        self.count = self.count - 1





    def prio(self):
        if (self.ui.radioButton.isChecked() == True):
            self.ui.radioButton_flow.setEnabled (False)
            self.ui.radioButton_pressure.setEnabled (False)
            self.ui.doubleSpinBox_ch1.setReadOnly(True)
            self.ui.doubleSpinBox_ch2.setReadOnly(True)
            self.ui.doubleSpinBox_ch3.setReadOnly(True)
            self.ui.doubleSpinBox_ch4.setReadOnly(True)
            self.ui.doubleSpinBox_fu.setReadOnly(True)
        if (self.ui.radioButton.isChecked() == False):
            self.ui.radioButton_flow.setEnabled (True)
            self.ui.radioButton_pressure.setEnabled (True)
            self.ui.doubleSpinBox_ch1.setReadOnly(False)
            self.ui.doubleSpinBox_ch2.setReadOnly(False)
            self.ui.doubleSpinBox_ch3.setReadOnly(False)
            self.ui.doubleSpinBox_ch4.setReadOnly(False)
            self.ui.doubleSpinBox_fu.setReadOnly(False)




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    p = pression(ui)
    r = RT_Plotter(ui,0)
    r2 = RT_Plotter(ui,1)
    r3 = RT_Plotter(ui,2)
    r4 = RT_Plotter(ui,3)
    r5 = RT_Plotter2(ui)
    MainWindow.show()
    sys.exit(app.exec_())
