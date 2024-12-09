from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QDate, Qt

class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_dates = {}  # 保存任务日期和类型

    def set_task_dates(self, task_dates):
        """
        设置任务日期数据
        :param task_dates: dict，键为 QDate，值为任务类型的集合
        """
        self.task_dates = task_dates
        self.update()  # 刷新日历

    def paintCell(self, painter, rect, date):
        """
        自定义绘制每个日期单元格
        """
        super().paintCell(painter, rect, date)  # 保持默认绘制

        # 检查当前日期是否有任务
        if date in self.task_dates:
            categories = self.task_dates[date]

            # 设置小圆点的颜色和大小
            if "Deadline" in categories:
                painter.setBrush(QColor(255, 0, 0))  # 红色圆点
            elif "Todo" in categories:
                painter.setBrush(QColor(0, 255, 0))  # 绿色圆点
            elif "Arrangement" in categories or "Event" in categories:
                painter.setBrush(QColor(0, 0, 255))  # 蓝色圆点

            # 计算圆点位置
            center_x = rect.center().x()
            center_y = rect.bottom() - 5
            radius = 5  # 圆点半径

            # 绘制圆点
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center_x - radius, center_y - radius, 2 * radius, 2 * radius)
