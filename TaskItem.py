import sys, sqlite3
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QListWidgetItem, QCheckBox, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QColor, QBrush, QFont
from PyQt5.QtCore import Qt

font = QFont()
font.setPointSize(12)

class TaskItemBase(QWidget):
    def __init__(self, task, category, colors, list_widget, on_task_deleted=None, parent=None):
        super().__init__(parent)
        self.task = task
        self.category = str(category)
        self.colors = {
            "Deadline": QColor(255, 200, 200), 
            "Todo": QColor(200, 255, 200),     
            "Event": QColor(255, 243, 108)         
        }
        self.list_widget = list_widget
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        #create delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setVisible(False)
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        # track mouse location to display delete button
        self.setMouseTracking(True)

        self.on_task_deleted = on_task_deleted

    def enterEvent(self, event):
        '''
            set the button to visible when the mouse enters
        '''
        self.delete_button.setVisible(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        '''
            set the button to invisible when the mouse leaves
        '''
        self.delete_button.setVisible(False)
        super().leaveEvent(event)

    def delete_task(self):
        '''
            delete the task from  dataset and list widget
        '''
        conn = sqlite3.connect('task.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task = ?", (self.task,))
        conn.commit()
        conn.close()

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if self.list_widget.itemWidget(item) == self:
                self.list_widget.takeItem(i)
                break
        
        if self.on_task_deleted:
            self.on_task_deleted()
    
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        color = self.colors.get(self.category, QColor(255, 255, 255))
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())  
        super().paintEvent(event)

class TaskItemWithoutCheckbox(TaskItemBase):
    def __init__(self, task, category, colors, list_widget, on_task_deleted=None, parent=None):
        super().__init__(task, category, colors, list_widget, on_task_deleted=on_task_deleted, parent=parent)
        self.label = QLabel(self.task)
        self.label.setTextInteractionFlags(Qt.NoTextInteraction)
        self.label.setStyleSheet("color: black;")  
        self.label.setFont(font)
        self.layout.insertWidget(0, self.label)
        self.label.setFixedHeight(20)



class TaskItemWithCheckbox(TaskItemBase):
    def __init__(self, task, category, completed, colors, list_widget, update_status_callback, on_task_deleted=None, parent=None):
        super().__init__(task, category, colors, list_widget, on_task_deleted=on_task_deleted, parent=parent)
        self.checkbox = QCheckBox(task)
        self.checkbox.setChecked(completed == 'YES')
        self.checkbox.stateChanged.connect(
            lambda state: update_status_callback(self.task, state)
        )
        self.checkbox.setFont(font)
        self.layout.insertWidget(0, self.checkbox)
        self.setFixedHeight(20)  


