import sys, sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window_1 import Ui_MainWindow
from dashboard_window_function import func_dashboardwindow
from archive_window_function import archive_window_function

class Func_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

        self.comboBox.addItems(["Deadline", "Todo", "Event", "Arrangement"])
        #connect signals to functions-page1
        self.archive_button.clicked.connect(self.pop_archive_window)
        self.dashboard_button.clicked.connect(self.pop_dashboard_window)
        self.add_text.clicked.connect(self.getText)

        #connect signals to functions -page2
        self.comboBox.activated.connect(self.new_task)

    
    def pop_archive_window(self):
        '''when "archive"is clicked, pop archive window'''
        self.subwindow = archive_window_function()
        self.subwindow.show()

    def pop_dashboard_window(self):
        '''when "dashboard"is clicked, pop dashboard window'''
        self.subwindow = func_dashboardwindow()
        self.subwindow.show()

    def getText(self):
        '''
        on page 1       
        when "save for later" button is clicked, save this into database:
            1-the content
            2-the time
        '''        
        text = self.textEdit.toPlainText()

        if text:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect('dashboard.db')
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS dashboard (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                time TEXT NOT NULL
            )
            ''')

            cursor.execute('''
            INSERT INTO dashboard (content, time)
            VALUES(?,?)
            ''',
            (text, current_time))

            conn.commit()
            conn.close()

            self.textEdit.clear()

    def new_task(self):
        
        task_text = self.add_task.toPlainText()

        if task_text:
            conn = sqlite3.connect('task.db')
            cursor = conn.cursor()
            date_selected = self.calendarWidget.selectedDate().toPyDate()
            category = self.comboBox.currentText()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL
            )
            ''')

            cursor.execute('''
            INSERT INTO task (task, date, category)
            VALUES(?,?,?)
            ''',
            (task_text, date_selected, category))

            conn.commit()
            conn.close()

            self.add_task.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Func_MainWindow()
    window.show()

    sys.exit(app.exec_())