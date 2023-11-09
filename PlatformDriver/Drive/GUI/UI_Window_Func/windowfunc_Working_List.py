import sys
import random
import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QDateTime
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment

from io import StringIO

from PlatformDriver.Drive.GUI.UI_Data import globals

def clear_table_WL():
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        # Clear the table
        columnCount_oldWL = my_window.tableWidget_WL.columnCount()
        for hr in range(0, columnCount_oldWL):
            my_window.tableWidget_WL.removeColumn(0)
        rowCount_oldWL = my_window.tableWidget_WL.rowCount()
        for hc in range(0, rowCount_oldWL):
            my_window.tableWidget_WL.removeRow(0)

def build_table_each_WL(rowCount_FL, rowCount_SL, position_data):
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        # set names of columns and rows
        rowName = []
        rowName.append("Position")
        rowName.append("Chemical")
        rowName.append("Dosage")
        rowName.append("Order")
        for i in range(1, rowCount_SL + 1):
            rowName.append("Setting" + str(i))
        my_window.tableWidget_WL.setVerticalHeaderLabels(rowName)
        # insert the items into the table
        ## insert the Chemicals and Dosages
        for kf in range(0, rowCount_FL):
            item_insert = QTableWidgetItem(position_data[4 * kf])
            item_insert.setTextAlignment(Qt.AlignCenter)
            my_window.tableWidget_WL.setItem(0, kf, item_insert)
            item_insert = QTableWidgetItem(position_data[4 * kf + 1])
            item_insert.setTextAlignment(Qt.AlignCenter)
            my_window.tableWidget_WL.setItem(1, kf, item_insert)

            item_insert = QTableWidgetItem(position_data[4 * kf + 2])
            item_insert.setTextAlignment(Qt.AlignCenter)
            my_window.tableWidget_WL.setItem(2, kf, item_insert)
            item_insert = QTableWidgetItem(position_data[4 * kf + 3])
            item_insert.setTextAlignment(Qt.AlignCenter)
            my_window.tableWidget_WL.setItem(3, kf, item_insert)
        ## insert the Settings
        for ks in range(0, rowCount_SL):
            item_insert = QTableWidgetItem(
                position_data[4 * rowCount_FL + 2 * ks] + '  ' + position_data[4 * rowCount_FL + 2 * ks + 1])
            item_insert.setTextAlignment(Qt.AlignCenter)
            my_window.tableWidget_WL.setItem(4 + ks, 0, item_insert)
            my_window.tableWidget_WL.setSpan(4 + ks, 0, 1, rowCount_FL)
        my_window.tableWidget_WL.resizeColumnsToContents()
        for column in range(my_window.tableWidget_WL.columnCount()):
            column_width = my_window.tableWidget_WL.columnWidth(column)
            my_window.tableWidget_WL.setColumnWidth(column, column_width + 15)
        for row in range(my_window.tableWidget_WL.rowCount()):
            column_width = my_window.tableWidget_WL.columnWidth(column)
            my_window.tableWidget_WL.setColumnWidth(column, column_width + 10)

def buttonAddWL():  # WorkingList add button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        # Get the quantity of Working List
        # global globals.group_current
        position_count = len(globals.group_current)
        position_number_current = int(my_window.lineEdit_WL_Position.text())
        # Clear the table
        clear_table_WL()
        # Establish new Working List
        rowCount_FL = my_window.tableWidget_FL.rowCount()  # number of chemicals
        rowCount_SL = my_window.tableWidget_SL.rowCount()  # number of settings

        my_window.tableWidget_WL.setColumnCount(rowCount_FL)  # set column of WL
        my_window.tableWidget_WL.setRowCount(4 + rowCount_SL)  # set row of WL
        # append items into the list of contents of current Working List
        position_data_current = []
        for i in range(1, rowCount_FL + 1):
            position_data_current.append(my_window.tableWidget_FL.item(i - 1, 0).text())
            position_data_current.append(my_window.tableWidget_FL.item(i - 1, 1).text())
            position_data_current.append(my_window.tableWidget_FL.item(i - 1, 2).text())
            position_data_current.append(my_window.tableWidget_FL.item(i - 1, 3).text())
        for j in range(1, rowCount_SL + 1):
            position_data_current.append(my_window.tableWidget_SL.item(j - 1, 0).text())
            position_data_current.append(my_window.tableWidget_SL.item(j - 1, 1).text())

        build_table_each_WL(rowCount_FL, rowCount_SL, position_data_current)

        # Save the established Working List
        position_data_current.append(str(rowCount_FL))
        position_data_current.append(str(rowCount_SL))
        globals.group_current[position_number_current - 1] = position_data_current
        print(globals.group_current)
        '''if position_quantity == 0:  #no Working List
            my_window.lineEdit_WL_Position.setText('1')
        else:
            my_window.lineEdit_WL_Position.setText(str(int(position_quantity) + 1))'''

def buttonRmWL():  # WorkingList remove button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        # global globals.group_current
        position_number_current = int(my_window.lineEdit_WL_Position.text()) - 1
        clear_table_WL()
        globals.group_current[position_number_current] = 'empty'
        print(globals.group_current)

def buttonPreWL():  # WorkingList previous position button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        # change the position number
        position_number_current = int(my_window.lineEdit_WL_Position.text())
        if position_number_current > 1:
            position_number_previous = position_number_current - 1
            my_window.lineEdit_WL_Position.setText(str(position_number_previous))
            # Clear the table
            clear_table_WL()
            if globals.group_current[position_number_previous - 1] != 'empty':
                # get the previous position contents
                position_data_previous = globals.group_current[position_number_previous - 1]
                itemCount = len(position_data_previous)
                rowCount_FL = int(position_data_previous[itemCount - 2])  # contents of FL
                rowCount_SL = int(position_data_previous[itemCount - 1])  # contents of SL
                # establish the previous table
                my_window.tableWidget_WL.setColumnCount(rowCount_FL)
                my_window.tableWidget_WL.setRowCount(4 + rowCount_SL)
                build_table_each_WL(rowCount_FL, rowCount_SL, position_data_previous)

def buttonNextWL(self):  # WorkingList next position button
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        # change the position number
        position_number_current = int(my_window.lineEdit_WL_Position.text())
        if position_number_current < len(globals.group_current):
            position_number_next = position_number_current + 1
            my_window.lineEdit_WL_Position.setText(str(position_number_next))
            # Clear the table
            clear_table_WL()
            if globals.group_current[position_number_next - 1] != 'empty':
                # get the next position contents
                position_data_next = globals.group_current[position_number_next - 1]
                itemNum = len(position_data_next)
                rowCount_FL = int(position_data_next[itemNum - 2])
                rowCount_SL = int(position_data_next[itemNum - 1])
                # establish the next table
                my_window.tableWidget_WL.setColumnCount(rowCount_FL)
                my_window.tableWidget_WL.setRowCount(4 + rowCount_SL)
                build_table_each_WL(rowCount_FL, rowCount_SL, position_data_next)
