from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

font = QFont()
font.setPointSize(12)
class TaskItemWidget(QWidget):
    def __init__(self, task_id, task_content, delete_callback, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.delete_callback = delete_callback

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(task_content, self)
        self.label.setFont(font)
        self.layout.addWidget(self.label)

        self.delete_button = QPushButton("delete", self)
        self.delete_button.setVisible(False)  
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.delete_button.setFixedSize(25, 25)
        self.layout.addWidget(self.delete_button)

    def on_delete_clicked(self):
        self.delete_callback(self.task_id)

    def enterEvent(self, event):
        self.delete_button.setVisible(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.delete_button.setVisible(False)
        super().leaveEvent(event)
