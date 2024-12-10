from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class MultiTaskProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_ratios = [] 
        self.task_colors = [] 

    def set_tasks(self, task_ratios, task_colors):
        self.task_ratios = task_ratios
        self.task_colors = task_colors
        self.update() 

    def paintEvent(self, event):
        # 绘制白色背景（调试用）
        painter = QPainter(self)
        rect = self.rect()
        painter.setBrush(Qt.white)
        painter.drawRect(rect)

        painter.setBrush(Qt.white)
        painter.drawRect(rect)
        x_start = rect.x()
        total_width = rect.width()
        print(f"Total Width: {total_width}, Ratios: {self.task_ratios}")

        for ratio, color in zip(self.task_ratios, self.task_colors):
            segment_width = total_width * ratio
            print(f"Drawing - Start: {x_start}, Width: {segment_width}, Color: {color}")
            painter.setBrush(QColor(color))
            painter.drawRect(x_start, rect.y(), segment_width, rect.height())
            x_start += segment_width

        painter.setPen(Qt.black)
        painter.drawRect(rect)

        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignCenter, self.text())