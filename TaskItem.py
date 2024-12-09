import sys, sqlite3
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QListWidgetItem, QCheckBox, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt


class TaskItemBase(QWidget):
    def __init__(self, task, category, colors, list_widget, parent=None):
        super().__init__(parent)
        self.task = task
        self.category = category
        self.colors = colors
        self.list_widget = list_widget

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 创建删除按钮，默认隐藏
        self.delete_button = QPushButton("Delete")
        self.delete_button.setVisible(False)
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        # 设置鼠标事件来控制删除按钮的显示
        self.setMouseTracking(True)

    def enterEvent(self, event):
        """鼠标移入时显示删除按钮"""
        self.delete_button.setVisible(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标移出时隐藏删除按钮"""
        self.delete_button.setVisible(False)
        super().leaveEvent(event)

    def delete_task(self):
        """从数据库和列表中删除任务"""
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


class TaskItemWithCheckbox(TaskItemBase):
    def __init__(self, task, category, completed, colors, list_widget, update_status_callback, parent=None):
        super().__init__(task, category, colors, list_widget, parent)

        self.checkbox = QCheckBox(task)
        self.checkbox.setChecked(completed == 'YES')
        self.checkbox.stateChanged.connect(
            lambda state: update_status_callback(self.task, state)
        )
        self.layout.insertWidget(0, self.checkbox)  # 把checkbox放在布局的左侧
