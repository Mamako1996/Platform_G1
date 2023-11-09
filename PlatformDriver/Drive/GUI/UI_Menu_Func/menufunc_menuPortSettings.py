from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import serial
import os

from PlatformDriver.Drive.GUI.UI_Data import globals

def menuPortSettings():
    from PlatformDriver.Drive.MainControl import MyWindow
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow

    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        my_control = MyWindow()

        filename = 'E:/MECH/Platform_G1/PlatformDriver/Drive/GUI/UI_Data/PortConfig.txt'
        if os.path.exists(filename):
            print("Import existing port config.")
            with open(filename,'r') as f:
                lines = f.readlines()[:4]
                lines = [line.strip() for line in lines]
            globals.selected_port = lines
        else:
            print("No existing port config, please manually select.")
        # pop up a dialog
        dialog_serial_port_settings = QDialog()
        dialog_serial_port_settings.setWindowTitle("Serial Port settings")
        layout_dialog = QVBoxLayout()
        label_port = QLabel("Choose a port to connect:")

        groupbox_port = QGroupBox()
        groupbox_port.setTitle("COM")

        layout_groupbox_V = QVBoxLayout()
        layout_groupbox_H1 = QHBoxLayout()
        layout_groupbox_H2 = QHBoxLayout()
        layout_groupbox_H3 = QHBoxLayout()
        layout_groupbox_H4 = QHBoxLayout()

        groupbox_port.setFixedSize(500, 300)

        font = QFont()
        font.setPointSize(11)

        label_1 = QLabel("Stirring Station 1:")
        label_2 = QLabel("Stirring Station 2:")
        label_3 = QLabel("Stirring Station 3:")
        label_4 = QLabel("Pump:")

        combobox_COM_1 = QComboBox()
        combobox_COM_2 = QComboBox()
        combobox_COM_3 = QComboBox()
        combobox_COM_4 = QComboBox()

        combobox_Baud_1 = QComboBox()
        combobox_Baud_2 = QComboBox()
        combobox_Baud_3 = QComboBox()
        combobox_Baud_4 = QComboBox()

        combobox_COM_1.setFont(font)
        combobox_COM_2.setFont(font)
        combobox_COM_3.setFont(font)
        combobox_COM_4.setFont(font)

        combobox_Baud_1.setFont(font)
        combobox_Baud_2.setFont(font)
        combobox_Baud_3.setFont(font)
        combobox_Baud_4.setFont(font)

        '''def adjust_combobox_COM_width(combo):
            max_length = 0
            font_metrics = combo.fontMetrics()
            for i in range(combo.count()):
                item_text = combo.itemText(i)
                text_length = font_metrics.width(item_text)
                if text_length > max_length:
                    max_length = text_length
            combo.view().setMinimumWidth(max_length)

        adjust_combobox_COM_width(combobox_COM_1)
        adjust_combobox_COM_width(combobox_COM_2)
        adjust_combobox_COM_width(combobox_COM_3)
        adjust_combobox_COM_width(combobox_COM_4)'''

        layout_groupbox_H1.addWidget(combobox_COM_1)
        layout_groupbox_H1.addWidget(combobox_Baud_1)
        layout_groupbox_H2.addWidget(combobox_COM_2)
        layout_groupbox_H2.addWidget(combobox_Baud_2)
        layout_groupbox_H3.addWidget(combobox_COM_3)
        layout_groupbox_H3.addWidget(combobox_Baud_3)
        layout_groupbox_H4.addWidget(combobox_COM_4)
        layout_groupbox_H4.addWidget(combobox_Baud_4)

        layout_groupbox_V.addWidget(label_1)
        layout_groupbox_V.addLayout(layout_groupbox_H1)
        layout_groupbox_V.addWidget(label_2)
        layout_groupbox_V.addLayout(layout_groupbox_H2)
        layout_groupbox_V.addWidget(label_3)
        layout_groupbox_V.addLayout(layout_groupbox_H3)
        layout_groupbox_V.addWidget(label_4)
        layout_groupbox_V.addLayout(layout_groupbox_H4)

        baud_rate = [9600, 14400, 19200, 38400, 57600, 115200, 128000]
        for rate in baud_rate:
            combobox_Baud_1.addItem(str(rate))
            combobox_Baud_2.addItem(str(rate))
            combobox_Baud_3.addItem(str(rate))
            combobox_Baud_4.addItem(str(rate))

        def refresh_serial_ports():
            combobox_COM_1.clear()
            combobox_COM_2.clear()
            combobox_COM_3.clear()
            combobox_COM_4.clear()
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                combobox_COM_1.addItem(port.device + ": " + port.description)
                combobox_COM_2.addItem(port.device + ": " + port.description)
                combobox_COM_3.addItem(port.device + ": " + port.description)
                combobox_COM_4.addItem(port.device + ": " + port.description)
            for i in range(combobox_COM_1.count()):
                if combobox_COM_1.itemText(i).startswith(globals.selected_port[0]):
                    combobox_COM_1.setCurrentIndex(i)
                    break
            for i in range(combobox_COM_2.count()):
                if combobox_COM_2.itemText(i).startswith(globals.selected_port[1]):
                    combobox_COM_2.setCurrentIndex(i)
                    break
            for i in range(combobox_COM_3.count()):
                if combobox_COM_3.itemText(i).startswith(globals.selected_port[2]):
                    combobox_COM_3.setCurrentIndex(i)
                    break
            for i in range(combobox_COM_4.count()):
                if combobox_COM_4.itemText(i).startswith(globals.selected_port[3]):
                    combobox_COM_4.setCurrentIndex(i)
                    break

        button_refresh = QPushButton("Rescan")
        button_refresh.clicked.connect(refresh_serial_ports)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog_serial_port_settings.accept)
        buttonBox.rejected.connect(dialog_serial_port_settings.reject)

        layout_dialog.addWidget(label_port)
        layout_dialog.addWidget(groupbox_port)
        layout_dialog.addWidget(button_refresh)
        layout_dialog.addWidget(buttonBox)
        dialog_serial_port_settings.setLayout(layout_dialog)
        groupbox_port.setLayout(layout_groupbox_V)

        combobox_COM_1.clear()
        combobox_COM_2.clear()
        combobox_COM_3.clear()
        combobox_COM_4.clear()
        refresh_serial_ports()

        if dialog_serial_port_settings.exec_() == QDialog.Accepted:
            globals.selected_port[0] = combobox_COM_1.currentText().split(":")[0].strip()
            globals.selected_port[1] = combobox_COM_2.currentText().split(":")[0].strip()
            globals.selected_port[2] = combobox_COM_3.currentText().split(":")[0].strip()
            globals.selected_port[3] = combobox_COM_4.currentText().split(":")[0].strip()

            globals.port_baud_rate[0] = combobox_Baud_1.currentText()
            globals.port_baud_rate[1] = combobox_Baud_2.currentText()
            globals.port_baud_rate[2] = combobox_Baud_3.currentText()
            globals.port_baud_rate[3] = combobox_Baud_4.currentText()
            print("Serial Port Settings:", globals.selected_port)
            print("Serial Port Baud Rate:", globals.port_baud_rate)
            #my_control.serialPortSetting()

            # save Serial Port Settings into .txt
            with open('E:/MECH/Platform_G1/PlatformDriver/Drive/GUI/UI_Data/PortConfig.txt', 'w') as f:
                for item in globals.selected_port:
                    f.write("%s\n" % item)
                for item in globals.port_baud_rate:
                    f.write("%s\n" % item)