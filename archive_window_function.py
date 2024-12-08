import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem 
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from archive_window import archive_MainWindow
from PyQt5.QtCore import Qt

class archive_window_function(archive_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.list_content()

        self.set_ui()

    def list_content(self):
        conn = sqlite3.connect('archive.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, content FROM archive")
        rows = cursor.fetchall()

        for row in rows:
            item = QListWidgetItem(row[1])  # row[1] being content
            item.setData(Qt.UserRole, row[0])  # row[0] being id
            self.listView.addItem(item)
        
        conn.close()
    
    def set_ui(self):
        self.listView.setStyleSheet("""
            QListWidget::item {
                border-bottom: 1px solid lightgray;  
                padding: 0px;                       
            }
            
            QListWidget::item:selected {
                background: lightblue;          
            }
           
            """)

