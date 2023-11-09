from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QDateTime
from PyQt5.QtGui import *

from PlatformDriver.Drive.GUI.UI_Data import globals

def buttonAddSL():  # SettingList add button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()
    
    if isinstance(my_window, Ui_MainWindow):
        newItem = my_window.spinBox_SS.value()
        newSpeed = QTableWidgetItem(str(newItem) + ' rpm')
        newSpeed.setTextAlignment(Qt.AlignCenter)
        newItem2 = my_window.spinBox_TL.value()
        newItem3 = my_window.comboBox_TL.currentText()
        newTime = QTableWidgetItem(str(newItem2) + ' ' + str(newItem3))
        newTime.setTextAlignment(Qt.AlignCenter)
        # if row_click_FL == -1:
        row_count = my_window.tableWidget_SL.rowCount()
        my_window.tableWidget_SL.insertRow(row_count)
        my_window.tableWidget_SL.setItem(int(row_count), 0, newSpeed)
        my_window.tableWidget_SL.setItem(int(row_count), 1, newTime)
        # my_window.tableWidget_SL.resizeColumnsToContents()

def buttonRmSL():  # SettingList remove button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        if globals.row_click_SL == -1:
            row_count = my_window.tableWidget_SL.rowCount()
            my_window.tableWidget_SL.removeRow(row_count - 1)
        else:
            row_count = globals.row_click_SL
            my_window.tableWidget_SL.removeRow(row_count)
        globals.row_click_SL = -1

def tableSLClick(self, Item):  # SettingList click-on
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        globals.row_click_SL = Item.row()