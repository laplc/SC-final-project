import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem 
from Warning_delete import Warning_delete_window
from PyQt5.QtCore import pyqtSignal

class Warning_delete_func(QMainWindow, Warning_delete_window):
    delete_completed = pyqtSignal()
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

        self.delete_completed.emit()


