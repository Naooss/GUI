from mainwindow import ui, MainWindow
from logger import mylog
from file_manag import file_manager
from PyQt5.QtWidgets import QTreeWidgetItem

import os


class Ui_manager():
    """ Handles the general look of the the UI. """
    def __init__(self):
        self.sidebar = [ui.pushButtonDashboard, ui.pushButtonGlucose, ui.pushButtonFluigent, ui.pushButtonDocs, ui.pushButtonArduino]
        self.stackedpages = [ui.pageDashboard, ui.pageGlucose, ui.pageFgt, ui.pageDocs, ui.pageArduino]
        self.stackeddict = {}
        for x, y in zip(self.sidebar, self.stackedpages):
            self.stackeddict[x] = y

        ui.pushButtonDashboard.setChecked(True)
        ui.stackedWidget.setCurrentWidget(ui.pageDashboard)           # TODO: Change to ui.pageDashboard
        self.logic()

    def button2page(self, button):
        """ Changes the current page according the sidebar's buttons. """
        button.setChecked(True)
        ui.stackedWidget.setCurrentWidget(self.stackeddict[button])
        for x in self.stackeddict:
            if x != button:
                x.setChecked(False)

    def logic(self):
        ui.pushButtonDashboard.clicked.connect(lambda: self.button2page(ui.pushButtonDashboard))
        ui.pushButtonGlucose.clicked.connect(lambda: self.button2page(ui.pushButtonGlucose))
        ui.pushButtonFluigent.clicked.connect(lambda: self.button2page(ui.pushButtonFluigent))
        ui.pushButtonDocs.clicked.connect(lambda: self.button2page(ui.pushButtonDocs))
        ui.pushButtonArduino.clicked.connect(lambda: self.button2page(ui.pushButtonArduino))
        ui.lineEditComment.returnPressed.connect(lambda: file_manager.current_manip.commentbook.append(ui.lineEditComment.text()))


class Treeview():
    """ Represents the data structure of the manip."""
    def __init__(self):
        self.tree = ui.treeWidget

    def update(self, path):
        """ Updates the treeView widget. """
        from PyQt5.QtGui import QIcon
        parent_itm = QTreeWidgetItem(self.tree, [os.path.basename(path)])
        parent_itm.setIcon(0, QIcon('assets/file.ico'))
        for element in os.listdir(path):
            QTreeWidgetItem(parent_itm, [os.path.basename(element)])


ui_manager = Ui_manager()
treeview = Treeview()
