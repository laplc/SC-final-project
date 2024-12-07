import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from archive_window import archive_MainWindow
from dashboard_window import Ui_Dashboard_window

class Func_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

        self.add_text.clicked.connect(self.add_text_to_dashboard)
        self.archive_button.clicked.connect(self.pop_archive_window)
        self.dashboard_button.clicked.connect(self.pop_dashboard_window)

        self.archive_window = archive_MainWindow()

    def add_text_to_dashboard(self):
        #when "save for later button" is clicked, save text to database
        print("being clicked")
    
    def pop_archive_window(self):
        #when "archive"is clicked, pop archive window
        self.window = QtWidgets.QMainWindow()
        self.ui = archive_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def pop_dashboard_window(self):
        #when "dashboard"is clicked, pop dashboard window
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dashboard_window()
        self.ui.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Func_MainWindow()
    window.show()

    sys.exit(app.exec_())