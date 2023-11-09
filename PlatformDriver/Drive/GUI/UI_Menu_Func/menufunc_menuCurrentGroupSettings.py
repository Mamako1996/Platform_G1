from PyQt5.QtWidgets import *

from PlatformDriver.Drive.GUI.UI_Data import globals
from PlatformDriver.Drive.GUI.UI_Window_Func import windowfunc_Working_List

def menuCurrentGroupSettings():
    from PlatformDriver.Drive.MainControl import group_all

    from PlatformDriver.Drive.MainControl import MyWindow
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow

    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        print("1")
        my_control = MyWindow()
        # save current group
        my_control.save_current_group()
        # pop up a dialog
        dialog_current_group_settings = QDialog()
        dialog_current_group_settings.resize(300, 300)
        dialog_current_group_settings.setWindowTitle("Current group settings")
        layout = QVBoxLayout()
        # add settings of GROUP NAME and NUMBER OF POSITIONS
        label_name = QLabel("Name of current group:")
        lineEdit_name = QLineEdit()
        group_name_current = my_window.comboBox_Group.currentText()
        lineEdit_name.setText(group_name_current)
        label_count = QLabel("Total number of positions:")
        spinBox_count = QSpinBox()
        spinBox_count.setValue(len(globals.group_current))
        spinBox_count.setMinimum(1)
        spinBox_count.setMaximum(999)
        # add the settings of CHEMICAL REAGENTS
        label_chems = QLabel("Set Chemical Reagents:")
        label_position_A = QLabel("Position A:")
        label_position_B = QLabel("Position B:")
        label_position_C = QLabel("Position C:")
        label_position_D = QLabel("Position D:")
        lineEdit_chem_A = QLineEdit()
        lineEdit_chem_B = QLineEdit()
        lineEdit_chem_C = QLineEdit()
        lineEdit_chem_D = QLineEdit()
        # check existing REAGENTS and substitute into
        lineEdit_chem_A.setText(globals.chem_reagents[0])
        lineEdit_chem_B.setText(globals.chem_reagents[1])
        lineEdit_chem_C.setText(globals.chem_reagents[2])
        lineEdit_chem_D.setText(globals.chem_reagents[3])

        # add LAYOUT
        layoutA = QHBoxLayout()
        layoutB = QHBoxLayout()
        layoutC = QHBoxLayout()
        layoutD = QHBoxLayout()

        layoutA.addWidget(label_position_A)
        layoutA.addWidget(lineEdit_chem_A)
        layoutB.addWidget(label_position_B)
        layoutB.addWidget(lineEdit_chem_B)
        layoutC.addWidget(label_position_C)
        layoutC.addWidget(lineEdit_chem_C)
        layoutD.addWidget(label_position_D)
        layoutD.addWidget(lineEdit_chem_D)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog_current_group_settings.accept)
        buttonBox.rejected.connect(dialog_current_group_settings.reject)

        layout.addWidget(label_name)
        layout.addWidget(lineEdit_name)
        layout.addWidget(label_count)
        layout.addWidget(spinBox_count)

        layout.addWidget(label_chems)
        layout.addLayout(layoutA)
        layout.addLayout(layoutB)
        layout.addLayout(layoutC)
        layout.addLayout(layoutD)

        layout.addWidget(buttonBox)
        dialog_current_group_settings.setLayout(layout)

        if dialog_current_group_settings.exec() == QDialog.Accepted:
            index = my_window.comboBox_Group.currentIndex()
            group_name_new = lineEdit_name.text()
            my_window.comboBox_Group.setItemText(index, group_name_new)
            index_in_all = group_all.index(group_name_current)
            group_all[index_in_all] = group_name_new
            position_count_new = spinBox_count.value()
            my_window.label_Total_Positions.setText("/" + str(position_count_new))
            if position_count_new > len(globals.group_current):
                globals.group_current.extend(['empty'] * (position_count_new - len(globals.group_current)))
            elif position_count_new < len(globals.group_current):
                del globals.group_current[position_count_new:]

            globals.chem_reagents[0] = lineEdit_chem_A.text()
            globals.chem_reagents[1] = lineEdit_chem_B.text()
            globals.chem_reagents[2] = lineEdit_chem_C.text()
            globals.chem_reagents[3] = lineEdit_chem_D.text()

            windowfunc_Working_List.clear_table_WL()
            my_window.build_table_overall_WL(globals.group_current)

            fixed_word = 'Set chemical reagnents: '
            full_text = fixed_word + ', '.join(globals.chem_reagents)
            my_window.label_ActionFeedback.setText(full_text)

            my_window.comboBox_ChemicalReagents.setCurrentIndex(0)
            my_window.lineEdit_ChemicalReagents.setText(globals.chem_reagents[0])

            # print(full_text)
            print(my_window.label_ActionFeedback.text())
    else:
        print("2")