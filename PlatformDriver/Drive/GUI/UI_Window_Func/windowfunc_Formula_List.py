from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QDateTime
from PyQt5.QtGui import *

from PlatformDriver.Drive.GUI.UI_Data import globals

def buttonAddFL():  # FomulaList add button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        newItem = my_window.lineEdit_ChemicalReagents.text()
        newChem = QTableWidgetItem(newItem)
        newChem.setTextAlignment(Qt.AlignCenter)

        newItem2 = my_window.doubleSpinBox_Dml.value()
        newItem3 = my_window.doubleSpinBox_Duls.value()
        newDos = QTableWidgetItem(str(newItem2) + ' ml  ' + str(newItem3) + ' μl/s')
        newDos.setTextAlignment(Qt.AlignCenter)

        newItem4 = my_window.comboBox_Order.currentText()
        newOrder = QTableWidgetItem(newItem4)
        newOrder.setTextAlignment(Qt.AlignCenter)

        newItem5= my_window.comboBox_ChemicalReagents.currentText()
        newPosition = QTableWidgetItem(newItem5)
        newPosition.setTextAlignment(Qt.AlignCenter)

        # if globals.row_click_FL == -1:
        row_count = my_window.tableWidget_FL.rowCount()
        my_window.tableWidget_FL.insertRow(row_count)
        my_window.tableWidget_FL.setItem(int(row_count), 0, newPosition)
        my_window.tableWidget_FL.setItem(int(row_count), 1, newChem)
        my_window.tableWidget_FL.setItem(int(row_count), 2, newDos)
        my_window.tableWidget_FL.setItem(int(row_count), 3, newOrder)
        my_window.tableWidget_FL.resizeColumnsToContents()

def buttonRmFL(): #FomulaList remove button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        if globals.row_click_FL == -1:
            row_count = my_window.tableWidget_FL.rowCount()
            my_window.tableWidget_FL.removeRow(row_count - 1)
        else:
            row_count = globals.row_click_FL
            my_window.tableWidget_FL.removeRow(row_count)
        globals.row_click_FL = -1

def tableFLClick(self, Item): #FomulaList click-on
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        globals.row_click_FL = Item.row()
        my_window.label_ActionFeedback.setText(str(globals.row_click_FL))

def chemPositionChange():
    from PlatformDriver.Drive.MainControl import MyWindow
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        my_control = MyWindow()
        position_num = my_window.comboBox_ChemicalReagents.currentIndex()
        my_window.lineEdit_ChemicalReagents.setText(globals.chem_reagents[position_num])