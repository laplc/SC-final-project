import sys, sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window_1 import Ui_MainWindow
from PyQt5.QtWidgets import QListWidgetItem
from dashboard_window_function import func_dashboardwindow
from archive_window_function import archive_window_function
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QDate, QTimer
from TaskItem import TaskItemWithCheckbox, TaskItemWithoutCheckbox
from TaskItemWidget import TaskItemWidget
from PyQt5 import QtCore, QtWidgets

class Func_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)  
        self.colors = {
            "Deadline": QColor(255, 200, 200), 
            "Todo": QColor(200, 255, 200),     
            "Arrangement": QColor(255, 243, 108), 
            "Event": QColor(255, 255, 255)         
        }
        self.comboBox.addItems(["Deadline", "Todo", "Event", "Arrangement"])

        #connect signals to functions-page1
        self.archive_button.clicked.connect(self.pop_archive_window)
        self.dashboard_button.clicked.connect(self.pop_dashboard_window)
        self.add_text.clicked.connect(self.getText)

        #connect signals to functions -page2
        self.comboBox.activated.connect(self.new_task)
        self.comboBox.activated.connect(self.refresh_calendar)
        self.calendarWidget.selectionChanged.connect(self.refresh_list)

        self.refresh_calendar()
        #---------------------------page3---------------
        #connect signals to functions -page3
        self.Add_new_button.clicked.connect(self.add_new_tracker)

        self.load_tracker()
        self.timer = QTimer()
        self.timer.setInterval(1000)  
        self.timer.timeout.connect(self.update_current_task_time)
        self.current_task_widget = None 

        
    
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
        self.refresh_calendar()

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
            self.refresh_list()

    
    def refresh_list(self):
        self.task_list.clear() #clear task list
        #refresh calendar

        conn = sqlite3.connect('task.db')
        cursor = conn.cursor()
        date_selected = self.calendarWidget.selectedDate().toPyDate()

        query = "SELECT task, category, completed FROM tasks WHERE date = ?"
        cursor.execute(query, (date_selected,))
        tasks = cursor.fetchall()
        conn.close()

        category_order = {'Deadline': 0, 'Arrangement': 1, 'Event': 2, 'Todo': 3}
        tasks.sort(key=lambda x: category_order.get(x[1], 4))

        for task, category, completed in tasks:
            if category in ['Todo', 'Deadline']:
                widget = TaskItemWithCheckbox(
                    task, category, completed, self.colors, self.task_list, 
                    self.update_task_status, 
                    on_task_deleted=self.refresh_calendar 
                )
            else:
                widget = TaskItemWithoutCheckbox(
                    task, category, self.colors, self.task_list, 
                    on_task_deleted=self.refresh_calendar
                )

            item = QListWidgetItem(self.task_list)
            item.setSizeHint(widget.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)


    def update_task_status(self, task, state):
        '''
        update the task's completed status in the database.
        '''
        conn = sqlite3.connect('task.db')
        cursor = conn.cursor()

        completed = "YES" if state == Qt.Checked else "NO"

        cursor.execute("UPDATE tasks SET completed = ? WHERE task = ?", (completed, task))
        conn.commit()
        conn.close()

    def get_task_dates(self):
        """
        get info from database
        """
        conn = sqlite3.connect('task.db')
        cursor = conn.cursor()

        query = "SELECT date, category FROM tasks"
        cursor.execute(query)
        tasks = cursor.fetchall()
        conn.close()

        date_task_map = {}
        for task_date, category in tasks:
            qdate = QDate.fromString(task_date, "yyyy-MM-dd")
            if not qdate.isValid():
                continue  

            if qdate not in date_task_map:
                date_task_map[qdate] = set()
            date_task_map[qdate].add(category)

        return date_task_map

    def refresh_calendar(self):
        task_dates = self.get_task_dates()
        self.calendarWidget.set_task_dates(task_dates)
        self.calendarWidget.update()

    #-----------------methods for page3-------------------
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
            self.load_tracker()


    def load_tracker(self):
        '''
            This method load task from database to list by calling add_task_to_list
        '''
        conn = sqlite3.connect('tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, time FROM tracker")
        rows = cursor.fetchall()
        conn.close()

        self.Focus_list.clear()
        for task_id, task_content, total_time in rows:
            self.add_task_to_list(task_id, task_content, total_time)
    
    def add_task_to_list(self, task_id, task_content, total_time):
        '''
            This method add customized item to list
        '''
        print('adding_1')
        item = QListWidgetItem(self.Focus_list)
        task_widget = TaskItemWidget(task_id, task_content, total_time, self.switch_timer, self.delete_task)        
        item.setSizeHint(task_widget.sizeHint())
        item.setSizeHint(task_widget.sizeHint().expandedTo(QtCore.QSize(0, 30)))
        self.Focus_list.addItem(item)
        self.Focus_list.setItemWidget(item, task_widget)
    
    def delete_task(self, task_id):
        conn = sqlite3.connect('tracker.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tracker WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

        for i in range(self.Focus_list.count()):
            item = self.Focus_list.item(i)
            task_widget = self.Focus_list.itemWidget(item)
            if task_widget.task_id == task_id:
                self.Focus_list.takeItem(i)
                break
    
    def switch_timer(self, task_id):
        '''
            switch timer: stop or go
        '''
        for i in range(self.Focus_list.count()):
            item = self.Focus_list.item(i)
            task_widget = self.Focus_list.itemWidget(item)
            if task_widget.task_id == task_id:
                if self.current_task_widget == task_widget:
                    #stop timing
                    self.timer.stop()
                    self.current_task_widget = None
                    self.current_task_label.setText("No task selected")
                else:
                    # switch to new task
                    if self.current_task_widget:
                        self.timer.stop()
                    self.current_task_widget = task_widget
                    self.current_task_label.setText(f"Focusing on: {task_widget.task_button.text().split(' - ')[0]}")
                    self.timer.start()
                    self.update_progress_bar() 
                return
    
    def update_current_task_time(self):
        '''
            update time to database
        '''
        if self.current_task_widget:
            self.current_task_widget.total_time += 1  #increase every 1s
            self.current_task_widget.update_time()
            self.update_progress_bar()  


            # add to database
            conn = sqlite3.connect('tracker.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tracker SET time = ? WHERE id = ?",
                (self.current_task_widget.total_time, self.current_task_widget.task_id)
            )
            conn.commit()
            conn.close()

    def update_progress_bar(self):
        total_time = sum(task.total_time for task in self.get_all_tasks())
        if total_time == 0:
            self.progressBar.set_tasks([], [])
            return

        task_ratios = [task.total_time / total_time for task in self.get_all_tasks()]
        task_colors = ["#FF9999", "#99CCFF", "#FFCC99", "#66CC66"][:len(task_ratios)]
        self.progressBar.set_tasks(task_ratios, task_colors)

    def get_all_tasks(self):
        tasks = []
        for i in range(self.Focus_list.count()):
            item = self.Focus_list.item(i)
            task_widget = self.Focus_list.itemWidget(item)  
            tasks.append(task_widget)
        return tasks
    
 


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Func_MainWindow()
    window.show()

    sys.exit(app.exec_())