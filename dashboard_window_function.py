import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem 
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from archive_window import archive_MainWindow
from dashboard_window import Ui_Dashboard_window
from Warning_delete import Warning_delete_window
from Warning_delete_func import Warning_delete_func
from PyQt5.QtCore import Qt

class func_dashboardwindow(QMainWindow, Ui_Dashboard_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #connnect signals to functions
        self.dashboard_delete_button.clicked.connect(self.delete)
        self.dashboard_archive_button.clicked.connect(self.archive)
        self.dashboard_deleteall_button.clicked.connect(self.delete_all)
        self.dashboard_archiveall_button.clicked.connect(self.archive_all)

        self.list_content()
        self.set_ui()
    
    def set_ui(self):
        self.dashboard_list.setStyleSheet("""
            QListWidget::item {
                border-bottom: 1px solid lightgray;  
                padding: 0px;                       
            }
            
            QListWidget::item:selected {
                background: lightblue;          
            }
           
            """)

    def archive(self):
        None

    def delete(self):
        selected_item = self.dashboard_list.currentItem()
        if selected_item:
            conn = sqlite3.connect('dashboard.db')
            cursor = conn.cursor()
            record_id = selected_item.data(Qt.UserRole)
            cursor.execute("DELETE FROM dashboard WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()

            self.dashboard_list.takeItem(self.dashboard_list.row(selected_item))

    def archive_all(self):
        #pop up warning window
        self.window = QtWidgets.QMainWindow()
        self.ui = Warning_delete_func()
        self.ui.setupUi(self.window)
        self.window.show()

    def delete_all(self):
        '''
            when "delete all" is clicked, pop up a warning window
        '''
        self.window = Warning_delete_func()
        self.window.show()
    
    def list_content(self):
        conn = sqlite3.connect('dashboard.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, content FROM dashboard")
        rows = cursor.fetchall()

        for row in rows:
            item = QListWidgetItem(row[1])  # row[1] being content
            item.setData(Qt.UserRole, row[0])  # row[0] being id
            self.dashboard_list.addItem(item)

            

            


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
    
#     window = func_dashboardwindow()
#     window.show()

#     sys.exit(app.exec_())