import sys, sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window_1 import Ui_MainWindow
from PyQt5.QtWidgets import QListWidgetItem
from dashboard_window_function import func_dashboardwindow
from archive_window_function import archive_window_function
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QDate
from main_window_funtcion import Func_MainWindow


class main_window_function_p3(Func_MainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.setupUi(self, parent = parent)  

        self.Add_new_button.clicked.connect(self.add_new_tracker)

    def add_new_tracker(self):
        text = self.textEdit_2.toPlainText()

        if not text:
            return

        if text:
            
            conn = sqlite3.connect('tracker.db')
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracker (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                time INTEGER DEFAULT 0
            )
            ''')

            cursor.execute('''
            INSERT INTO tracker (content, time)
            VALUES(?,?)
            ''',
            (text, 0))

            conn.commit()
            conn.close()

            self.textEdit_2.clear()

    def display_trackers(self):
        conn = sqlite3.connect('tracker.db')
        cursor = conn.cursor()

        cursor.execute("SELECT content, time FROM tracker")
        rows = cursor.fetchall()

        self.listWidget.clear()  

        for row in rows:
            content, time = row
            self.listWidget.addItem(f"{content} - {time} mins")

        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = main_window_function_p3()
    window.show()

    sys.exit(app.exec_())