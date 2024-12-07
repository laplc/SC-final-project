import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from archive_window import archive_MainWindow
from dashboard_window_function import func_dashboardwindow

class Func_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

        #connect signals to functions
        self.add_text.clicked.connect(self.add_text_to_dashboard)
        self.archive_button.clicked.connect(self.pop_archive_window)
        self.dashboard_button.clicked.connect(self.pop_dashboard_window)

    def add_text_to_dashboard(self):
        #when "save for later button" is clicked, save text to database
        print("being clicked")
    
    def pop_archive_window(self):
        #when "archive"is clicked, pop archive window
        self.subwindow = func_dashboardwindow()
        self.subwindow.show()

    def pop_dashboard_window(self):
        #when "dashboard"is clicked, pop dashboard window
        self.subwindow = func_dashboardwindow()
        self.subwindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Func_MainWindow()
    window.show()

    sys.exit(app.exec_())