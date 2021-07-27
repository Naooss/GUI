from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

class MyWindow(QtWidgets.QWidget):
  def __init__(self):
    super(MyWindow,self).__init__()
    self.myButton = QtWidgets.QPushButton(self)
    self.myButton.setObjectName("myButton")
    self.myButton.setText("Test")
    self.myButton.clicked.connect(self.msg)

  def msg(self):
    directory1 = QFileDialog.getExistingDirectory(self,
                                     "Select Folder",
                                     "./") #Start path
    print(directory1)

    fileName1, filetype = QFileDialog.getOpenFileName(self,
                                     "Select File",
                  "./",
                                     "All Files (*);;Text Files (*.txt)") #Set the file extension filter, pay attention to the double semicolon interval
    print(fileName1,filetype)

    files, ok1 = QFileDialog.getOpenFileNames(self,
                                     "Multiple file selection",
                  "./",
                  "All Files (*);;Text Files (*.txt)")
    print(files,ok1)

    fileName2, ok2 = QFileDialog.getSaveFileName(self,
                                     "File Save",
                  "./",
                  "All Files (*);;Text Files (*.txt)")

if __name__=="__main__":
  import sys

  app=QtWidgets.QApplication(sys.argv)
  myshow=MyWindow()
  myshow.show()
  sys.exit(app.exec_()) 
