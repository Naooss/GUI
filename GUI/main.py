from mainwindow import *
from logger import mylog


@mylog.catch
def main_():
    if __name__ == "__main__":
        import ui_manag
        import sensorReader
        import plotter
        import sensorWriter
        import file_manag
        MainWindow.show()
        ui.statusbar.showMessage("Gluco_IMS (2021), made by M.Assaghour and G.Chaumont, ENSEIRB-MATMECA.")
        sys.exit(app.exec_())


main_()
