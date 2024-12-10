# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guii.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from CustomCalender import CustomCalendar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 604)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.page_tabs = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        self.page_tabs.setFont(font)
        self.page_tabs.setStyleSheet("QLabel{\n"
"background-color:rgb(169, 240, 255)\n"
"}")
        self.page_tabs.setObjectName("page_tabs")
        self.page1_tab = QtWidgets.QWidget()
        self.page1_tab.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.page1_tab.setObjectName("page1_tab")
        self.frame_2 = QtWidgets.QFrame(self.page1_tab)
        self.frame_2.setGeometry(QtCore.QRect(0, 480, 791, 131))
        self.frame_2.setStyleSheet("QFrame{\n"
"background-color:rgb(244, 255, 166)}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.archive_button = QtWidgets.QPushButton(self.frame_2)
        self.archive_button.setGeometry(QtCore.QRect(660, 30, 98, 26))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.archive_button.setFont(font)
        self.archive_button.setObjectName("archive_button")
        self.dashboard_button = QtWidgets.QPushButton(self.frame_2)
        self.dashboard_button.setGeometry(QtCore.QRect(540, 30, 111, 26))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.dashboard_button.setFont(font)
        self.dashboard_button.setObjectName("dashboard_button")
        self.textEdit = QtWidgets.QTextEdit(self.page1_tab)
        self.textEdit.setGeometry(QtCore.QRect(190, 170, 401, 141))
        self.textEdit.setObjectName("textEdit")
        self.add_text = QtWidgets.QPushButton(self.page1_tab)
        self.add_text.setGeometry(QtCore.QRect(440, 310, 151, 28))
        self.add_text.setObjectName("add_text")
        self.page_tabs.addTab(self.page1_tab, "")
        self.page2_tab = QtWidgets.QWidget()
        self.page2_tab.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.page2_tab.setObjectName("page2_tab")

        #replace with a custom calender
        self.calendarWidget = CustomCalendar(self.page2_tab)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 70, 411, 421))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setObjectName("calendarWidget")

        #-----------------------page2-------------------

        self.task_list = QtWidgets.QListWidget(self.page2_tab)
        self.task_list.setGeometry(QtCore.QRect(470, 110, 271, 271))
        self.task_list.setObjectName("task_list")
        self.add_task = QtWidgets.QTextEdit(self.page2_tab)
        self.add_task.setGeometry(QtCore.QRect(480, 400, 201, 41))
        self.add_task.setObjectName("add_task")
        self.comboBox = QtWidgets.QComboBox(self.page2_tab)
        self.comboBox.setGeometry(QtCore.QRect(690, 400, 51, 41))
        self.comboBox.setObjectName("comboBox")
        self.page_tabs.addTab(self.page2_tab, "")

        #-------------page3--------------------
        self.page3_tab = QtWidgets.QWidget()
        self.page3_tab.setObjectName("page3_tab")
        self.Focus_list = QtWidgets.QListWidget(self.page3_tab)
        self.Focus_list.setGeometry(QtCore.QRect(130, 130, 511, 311))
        self.Focus_list.setObjectName("Focus_list")
        self.textEdit_2 = QtWidgets.QTextEdit(self.page3_tab)
        self.textEdit_2.setGeometry(QtCore.QRect(220, 460, 281, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.Add_new_button = QtWidgets.QPushButton(self.page3_tab)
        self.Add_new_button.setGeometry(QtCore.QRect(520, 465, 75, 23))
        self.Add_new_button.setObjectName("Add_new_button")
        self.page_tabs.addTab(self.page3_tab, "")
        self.gridLayout.addWidget(self.page_tabs, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.current_task_label = QtWidgets.QLabel(self.page3_tab)
        self.current_task_label.setGeometry(QtCore.QRect(200, 100, 351, 20))  
        self.current_task_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.current_task_label.setText("No task selected") 
        self.current_task_label.setObjectName("current_task_label")
        self.current_task_label.setStyleSheet("""
                QLabel {
                        font-size: 12px;         
                        color: #555555;         
                        background-color: none; 
                        font-weight: bold;      
                }
                """)

        self.retranslateUi(MainWindow)
        self.page_tabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.archive_button.setText(_translate("MainWindow", "archive"))
        self.dashboard_button.setText(_translate("MainWindow", " dashboard"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:13.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.2pt;\"> </span></p></body></html>"))
        self.add_text.setText(_translate("MainWindow", "Save for later"))
        self.page_tabs.setTabText(self.page_tabs.indexOf(self.page1_tab), _translate("MainWindow", "Brain Dump"))
        self.page_tabs.setTabText(self.page_tabs.indexOf(self.page2_tab), _translate("MainWindow", "Calender"))
        self.Add_new_button.setText(_translate("MainWindow", "Add"))
        self.page_tabs.setTabText(self.page_tabs.indexOf(self.page3_tab), _translate("MainWindow", "Focusing"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
