from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

font = QFont()
font.setPointSize(12)
class TaskItemWidget(QWidget):
    def __init__(self, task_id, task_content, total_time, timer_callback, delete_callback, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.delete_callback = delete_callback

        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;  
                border: 1px solid #D3D3D3; 
                border-radius: 20px;       
                padding: 5px;              
            }
            QPushButton {
                background-color: transparent; 
                border: none;                 
                font-size: 12px;
            }
            QPushButton:hover {
                color: #007BFF; 
            }
        """)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)  # 设置内部边距
        self.total_time = total_time

        # self.layout = QHBoxLayout(self)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.total_time = total_time

        self.task_button = QPushButton(f"{task_content} - {self.format_time(self.total_time)}", self)
        self.task_button.setFont(font)
        self.task_button.clicked.connect(self.on_task_clicked)
        self.layout.addWidget(self.task_button)

        self.delete_button = QPushButton("delete", self)
        self.delete_button.setVisible(False)  
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.delete_button.setFixedSize(50, 25)
        self.layout.addWidget(self.delete_button)

        self.total_time = total_time  
        self.timer_callback = timer_callback
        self.delete_callback = delete_callback

    def on_delete_clicked(self):
        self.delete_callback(self.task_id)

    def enterEvent(self, event):
        self.delete_button.setVisible(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.delete_button.setVisible(False)
        super().leaveEvent(event)
    
    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_time(self):
        '''
            update time_displayed
        '''
        self.task_button.setText(f"{self.task_button.text().split(' - ')[0]} - {self.format_time(self.total_time)}")

    def on_task_clicked(self):
        '''
            when button is clicked
        '''
        self.timer_callback(self.task_id) #call method in main window