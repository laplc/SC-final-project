import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from archive_window import archive_MainWindow

class func_archive_MainWindow(QMainWindow, archive_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

