import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem 
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from dashboard_window import Ui_Dashboard_window
from Warning_delete import Warning_delete_window
from PyQt5.QtCore import Qt

class Warning_delete_func(QMainWindow, Warning_delete_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 

        self.confirm_button.clicked.connect(self.confirm_delete)

    def confirm_delete(self):
        '''
            delete all records in dashboard db
        '''
        print('deleting')
        conn = sqlite3.connect('dashboard.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dashboard")

        conn.commit()
        conn.close()

        self.close()


