from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtGui import QPainter, QColor, QTextCharFormat
from PyQt5.QtCore import QDate, Qt

class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_dates = {}  

    def set_task_dates(self, task_dates):
        self.task_dates = task_dates

        self.setDateTextFormat(QDate(), QTextCharFormat())

        self.update()

    def paintCell(self, painter, rect, date):
        """
        """
        super().paintCell(painter, rect, date)  #default painting

        # check for task
        if date in self.task_dates:
            categories = self.task_dates[date]
            colors = {
                "Deadline": QColor(255, 0, 0), 
                "Todo": QColor(0, 255, 0),    
                "Event": QColor(255,255,0),   
            }

            radius = 4  
            padding = 2 
            center_x = rect.center().x()
            center_y = rect.bottom() - radius - padding
            start_x = center_x - ((len(categories) - 1) * (radius + padding)) / 2

            for i, category in enumerate(categories):
                if category in colors:
                    painter.setBrush(colors[category])
                    painter.setPen(Qt.NoPen)
                    x = start_x + i * (2 * radius + padding)
                    painter.drawEllipse(x - radius, center_y - radius, 2 * radius, 2 * radius)

