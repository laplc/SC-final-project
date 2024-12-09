import sys, sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window_1 import Ui_MainWindow
from PyQt5.QtWidgets import QListWidgetItem, QCheckBox, QWidget, QHBoxLayout, QLabel
from dashboard_window_function import func_dashboardwindow
from archive_window_function import archive_window_function
from PyQt5.QtGui import QColor, QBrush

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
        # self.calendarWidget.selectionChanged.connect(self.refresh_list)

    
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
        '''
            on page 2
            store tasks into a database after clicking combobox
        '''
        task_text = self.add_task.toPlainText()

        if task_text:
            conn = sqlite3.connect('task.db')
            cursor = conn.cursor()
            date_selected = self.calendarWidget.selectedDate().toPyDate()
            category = self.comboBox.currentText()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                completed TEXT DEFAULT 'NO'
            )
            ''')

            cursor.execute('''
            INSERT INTO tasks (task, date, category, completed)
            VALUES(?,?,?,?)
            ''',
            (task_text, date_selected, category, 'NO'))

            conn.commit()
            conn.close()

            self.add_task.clear()

    # def refresh_list(self):
    #     '''
    #         on page2
    #         refresh the list whenever a new date is selected
    #         1. if category is "todo", add a checkbox 
    #         2. other categories are listed first without checkboxes.
    #     '''
    #     self.task_list.clear()
    #     conn = sqlite3.connect('task.db')
    #     cursor = conn.cursor()
    #     date_selected = self.calendarWidget.selectedDate().toPyDate()

    #     query = "SELECT task, category FROM task WHERE date = ?"
    #     cursor.execute(query, (date_selected,))
    #     tasks = cursor.fetchall()  

    #     deadlines = []  
    #     todos = []     
    #     arrangements = [] 
    #     events = []        

    #     for task, category in tasks:
    #         if category == "deadline":
    #             deadlines.append(task)
    #         elif category == "todo":
    #             todos.append(task)
    #         elif category == "arrangement":
    #             arrangements.append((task, category))
    #         elif category == "event":
    #             events.append((task, category))

    #     colors = {
    #         "deadline": QColor(255, 200, 200), 
    #         "todo": QColor(200, 255, 200),     
    #         "arrangement": QColor(255, 255, 200), 
    #         "event": QColor(255, 255, 255)         
    #     }
        
    #     def add_task_without_checkbox(task, category):
    #         item_widget = QWidget()
    #         layout = QHBoxLayout()
    #         checkbox = QCheckBox()
    #         checkbox.setText(task)
    #         layout.addWidget(checkbox)
    #         layout.setContentsMargins(0, 0, 0, 0)
    #         item_widget.setLayout(layout)

    #         item = QListWidgetItem(self.task_list)
    #         item.setSizeHint(item_widget.sizeHint())
    #         item.setBackground(QBrush(colors[category]))  
    #         self.task_list.addItem(item)
    #         self.task_list.setItemWidget(item, item_widget)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Func_MainWindow()
    window.show()

    sys.exit(app.exec_())