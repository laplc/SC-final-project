import sqlite3
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from PyQt5 import QtWidgets
from archive_window import archive_MainWindow
from PyQt5.QtCore import Qt


class archive_window_function(archive_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.list_content()
        self.set_ui()

        self.archive_delete.clicked.connect(self.delete)
        self.archive_export.clicked.connect(self.export_to_txt)

    def list_content(self):
        conn = sqlite3.connect('archive.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, content FROM archive")
        rows = cursor.fetchall()

        for row in rows:
            item = QListWidgetItem(row[1])  # row[1] being content
            item.setData(Qt.UserRole, row[0])  # row[0] being id
            self.listView.addItem(item)

        conn.close()

    def set_ui(self):
        '''
            set UI
        '''
        self.listView.setStyleSheet("""
            QListWidget::item {
                border-bottom: 1px solid lightgray;  
                padding: 0px;                       
            }
            
            QListWidget::item:selected {
                background: lightblue;          
            }
           
            """)

    def delete(self):
        selected_item = self.listView.currentItem()
        if selected_item:
            conn = sqlite3.connect('archive.db')
            cursor = conn.cursor()
            record_id = selected_item.data(Qt.UserRole)
            cursor.execute("DELETE FROM archive WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()

            self.listView.takeItem(self.listView.row(selected_item))

    def export_to_txt(self):
        # Open database connection
        conn = sqlite3.connect('archive.db')
        cursor = conn.cursor()

        # Fetch all content and date from the archive
        cursor.execute("SELECT content, time FROM archive")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            QMessageBox.warning(
                self, "No Data", "There are no records to export.")
            return

        # Open file dialog for user to select save location
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save TXT File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if not file_path:
            return  # procedure is canceled

        # Ensure the file has .txt extension
        if not file_path.endswith(".txt"):
            file_path += ".txt"

        # Export to TXT file
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("Archive Export\n")
                file.write("================\n")
                for content, date in rows:
                    file.write(f"{content}\n")
                    file.write(f"Date: {date}\n")
                    file.write("\n")

            QMessageBox.information(
                self, "Export Successful", f"TXT exported successfully to {file_path}.")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An error occurred while saving the file: {str(e)}")
