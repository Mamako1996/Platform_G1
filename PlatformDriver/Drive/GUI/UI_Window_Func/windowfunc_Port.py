from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QDateTime
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

from io import StringIO

from PlatformDriver.Drive.GUI.UI_Data import globals

def serialPortSetting():
    # check the port name
    print(globals.selected_port)

def serialOpen():
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        if not my_window.serial_test.isOpen():
            my_window.serial_test.open(QSerialPort.ReadWrite)
            my_window.pushButton_Serial_Open.setEnabled(False)
            my_window.pushButton_Serial_Close.setEnabled(True)
            my_window.pushButton_Serial_Send.setEnabled(True)

def serialClose():
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        if my_window.serial_test.isOpen():
            my_window.serial_test.close()
            my_window.pushButton_Serial_Open.setEnabled(True)
            my_window.pushButton_Serial_Close.setEnabled(False)
            my_window.pushButton_Serial_Send.setEnabled(False)

def serialSendData():
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow
    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        data_send = my_window.textEdit_Serial.toPlainText()
        if data_send:
            my_window.serial_test.write(data_send.encode())