from PyQt5.QtWidgets import QProgressBar, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
 
class MultiTaskBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_ratios = []  
        self.task_colors = []  

    def set_tasks(self, task_ratios, task_colors):
        
        if not task_ratios or not task_colors:
            print("Error: No tasks to display.")
            return

        self.task_ratios = task_ratios
        self.task_colors = task_colors
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # clear
        painter.setBrush(Qt.white)
        painter.drawRect(rect)

        x_start = rect.x()
        total_width = rect.width()


        for ratio, color in zip(self.task_ratios, self.task_colors):
            segment_width = total_width * ratio

            #for testing
            # print(f"Drawing Segment: Start={x_start}, Width={segment_width}, Color={color}")

            if segment_width > 0:
                painter.save()
                painter.setBrush(QColor(color))
                painter.drawRect(x_start, rect.y(), segment_width, rect.height())
                painter.restore()

                x_start += segment_width


