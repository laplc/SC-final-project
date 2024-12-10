from PyQt5.QtWidgets import QProgressBar, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
 
class MultiTaskBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_ratios = []  
        self.task_colors_with_names = []

    def set_tasks(self, task_ratios, task_colors, task_names):
        
        if not task_ratios or not task_colors:
            print("Error: No tasks to display.")
            return

        self.task_ratios = task_ratios
        self.task_colors_with_names = list(zip(task_colors, task_names))
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # clear
        painter.setBrush(Qt.white)
        painter.drawRect(rect)

        x_start = rect.x()
        total_width = rect.width()


        for ratio, (color, task_name) in zip(self.task_ratios, self.task_colors_with_names):
            segment_width = total_width * ratio

            #for testing
            # print(f"Drawing Segment: Start={x_start}, Width={segment_width}, Color={color}")

            if segment_width > 0:
                painter.save()
                painter.setBrush(QColor(color))
                painter.drawRect(x_start, rect.y(), segment_width, rect.height())
                painter.restore()
                painter.setPen(Qt.black if ratio > 0.15 else Qt.white)  # 小比例用白字，大比例用黑字
                text_rect = QtCore.QRectF(x_start, rect.y(), segment_width, rect.height())
                painter.drawText(text_rect, Qt.AlignCenter, task_name)

                x_start += segment_width


