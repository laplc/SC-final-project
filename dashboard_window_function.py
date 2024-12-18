import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem
from dashboard_window import Ui_Dashboard_window
from Warning_delete_func import Warning_delete_func
from Warning_archive_func import Warning_archive_func
from PyQt5.QtCore import Qt


class func_dashboardwindow(QMainWindow, Ui_Dashboard_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # connnect signals to functions
        self.dashboard_delete_button.clicked.connect(self.delete)
        self.dashboard_archive_button.clicked.connect(self.archive)
        self.dashboard_deleteall_button.clicked.connect(self.delete_all)
        self.dashboard_archiveall_button.clicked.connect(self.archive_all)

        self.delete_window = Warning_delete_func()
        self.archive_window = Warning_archive_func()

        self.delete_window.delete_completed.connect(self.refresh_list)
        self.archive_window.archive_completed.connect(self.refresh_list)

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
        '''
        move content from dashboard db to archive db
        '''
        selected_item = self.dashboard_list.currentItem()
        if selected_item:
            content = selected_item.text()
            record_id = selected_item.data(Qt.UserRole)

            conn_dashboard = sqlite3.connect('dashboard.db')
            cursor_dashboard = conn_dashboard.cursor()
            cursor_dashboard.execute(
                "SELECT time FROM dashboard WHERE id = ?", (record_id,))
            time = cursor_dashboard.fetchone()
            time = time[0]
            # delete archived content from the list and dashboard db
            cursor_dashboard.execute(
                "DELETE FROM dashboard WHERE id = ?", (record_id,))
            conn_dashboard.commit()
            self.dashboard_list.takeItem(
                self.dashboard_list.row(selected_item))
            conn_dashboard.close()

            conn_archive = sqlite3.connect('archive.db')
            cursor_archive = conn_archive.cursor()
            cursor_archive.execute('''
            CREATE TABLE IF NOT EXISTS archive (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                time TEXT NOT NULL
            )
            ''')
            cursor_archive.execute(
                '''INSERT INTO archive (content, time)
                VALUES (?, ?)''', (content, time))
            conn_archive.commit()
            conn_archive.close()

    def delete(self):
        selected_item = self.dashboard_list.currentItem()
        if selected_item:
            conn = sqlite3.connect('dashboard.db')
            cursor = conn.cursor()
            record_id = selected_item.data(Qt.UserRole)
            cursor.execute("DELETE FROM dashboard WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()

            self.dashboard_list.takeItem(
                self.dashboard_list.row(selected_item))

    def archive_all(self):
        # pop up warning window
        self.archive_window.show()

    def delete_all(self):
        '''
            when "delete all" is clicked, pop up a warning window
        '''
        self.delete_window.show()

    def list_content(self):
        conn = sqlite3.connect('dashboard.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, content FROM dashboard")
        rows = cursor.fetchall()

        for row in rows:
            item = QListWidgetItem(row[1])  # row[1] being content
            item.setData(Qt.UserRole, row[0])  # row[0] being id
            self.dashboard_list.addItem(item)

        conn.close()

    def refresh_list(self):
        '''
        refresh the list whenever needed(mainly when everything is deleted or archived)
        '''
        self.dashboard_list.clear()

        conn = sqlite3.connect('dashboard.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM dashboard")
        rows = cursor.fetchall()

        for row in rows:
            item = QListWidgetItem(row[1])  # row[1] being content
            item.setData(Qt.UserRole, row[0])  # row[0] being id
            self.dashboard_list.addItem(item)

        conn.close()


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)

#     window = func_dashboardwindow()
#     window.show()

#     sys.exit(app.exec_())
