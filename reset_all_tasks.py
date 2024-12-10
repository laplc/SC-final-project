from PyQt5.QtWidgets import QMessageBox
import sqlite3

def reset_all_tasks(self):
    """
    Reset all tasks' time to zero after user c-uonfirmation.
    """
    confirm_dialog = QMessageBox(self)
    confirm_dialog.setWindowTitle("Reset Confirmation")
    confirm_dialog.setText("Are you sure you want to reset all tasks?")
    confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    confirm_dialog.setIcon(QMessageBox.Warning)
    response = confirm_dialog.exec_()

    if response == QMessageBox.Yes:
        conn = sqlite3.connect('tracker.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE tracker SET time = 0")
        conn.commit()
        conn.close()

        self.load_tracker()

        self.progressBar.set_tasks([], [], [])

        self.timer.stop()
        self.current_task_widget = None
        self.current_task_label.setText("No task selected")

        QMessageBox.information(self, "Reset Complete", "All tasks have been reset to zero.")
