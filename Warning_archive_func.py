import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem 
from Warning_archive import Warning_archive_window
from PyQt5.QtCore import pyqtSignal

class Warning_archive_func(QMainWindow, Warning_archive_window):
    archive_completed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.confirm_button.clicked.connect(self.confirm_archive)
        self.dismiss_button.clicked.connect(self.dismiss)

    def confirm_archive(self):
        '''
            move all records in dashboard to archive
        '''
        conn_dashboard = sqlite3.connect('dashboard.db')
        cursor_dashboard = conn_dashboard.cursor()
        conn_archive = sqlite3.connect('archive.db')
        cursor_archive = conn_archive.cursor()
        
        cursor_archive.execute('''
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            time TEXT NOT NULL
        )
        ''')

        cursor_dashboard.execute("SELECT id, content, time FROM dashboard")
        rows = cursor_dashboard.fetchall()
        for row in rows:
            record_id, content, time = row
            cursor_archive.execute(
                "INSERT INTO archive (content, time) VALUES ( ?, ?)",
                (content, time)
            )
        cursor_dashboard.execute("DELETE FROM dashboard")

        conn_dashboard.commit()
        conn_archive.commit()
        conn_archive.close()
        conn_dashboard.close()
        self.close()

        self.archive_completed.emit()

    def dismiss(self):
        self.close()