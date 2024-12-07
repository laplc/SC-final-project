import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from archive_window import archive_MainWindow
from dashboard_window import Ui_Dashboard_window
from Warning_archive import Warning_archive_window
from Warning_delete import Warning_delete_window

class func_dashboardwindow(QMainWindow, Ui_Dashboard_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #connnect signals to functions
        self.dashboard_delete_button.clicked.connect(self.delete)
        self.dashboard_archive_button.clicked.connect(self.archive)
        self.dashboard_deleteall_button.clicked.connect(self.delete_all)
        self.dashboard_archiveall_button.clicked.connect(self.archive_all)


    def archive(self):
        None

    def delete(self):
        None

    def archive_all(self):
        #pop up warning window
        self.window = QtWidgets.QMainWindow()
        self.ui = Warning_archive_window()
        self.ui.setupUi(self.window)
        self.window.show()

    def delete_all(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Warning_delete_window()
        self.ui.setupUi(self.window)
        self.window.show()
        None

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    window = func_dashboardwindow()
    window.show()

    sys.exit(app.exec_())