from PyQt5.QtWidgets import *

from PlatformDriver.Drive.GUI.UI_Data import globals

def buttonUpload():
    from PlatformDriver.Drive.GUI.UITest import Ui_MainWindow

    app = QApplication.instance()
    my_window = app.activeWindow()

    if isinstance(my_window, Ui_MainWindow):
        stir_list_1 = [''] * 4
        stir_list_2 = [''] * 4
        stir_list_3 = [''] * 4
        for i1 in range(4): #i1 from 0 to 3
            if globals.group_current[i1] and globals.group_current[i1] != 'empty':
                group_arranged = []
                for item in globals.group_current[i1]:
                    split_item = item.split('  ')
                    group_arranged.extend(split_item)
                count_Stir_1 = int(group_arranged[-1])
                count_Disp_1 = int(group_arranged[-2])
                stir_sublist_1 = []
                for j in range(count_Stir_1):
                    index1 = ((5 * count_Disp_1) - 1) + ((2 * j) + 1)
                    index2 = ((5 * count_Disp_1) - 1) + ((2 * j) + 2)
                    new_stir_data = ','.join([str(i1), \
                                              str(group_arranged[index1]), \
                                              str(group_arranged[index2]), \
                                              'true'])
                    stir_sublist_1.append(new_stir_data)
                stir_list_1[i1] = stir_sublist_1

            i2 = 4 + i1
            if globals.group_current[i2] and globals.group_current[i2] != 'empty':
                group_arranged = []
                for item in globals.group_current[i2]:
                    split_item = item.split('  ')
                    group_arranged.extend(split_item)
                count_Stir_2 = int(group_arranged[-1])
                count_Disp_2 = int(group_arranged[-2])
                stir_sublist_2 = []
                for j in range(count_Stir_2):
                    index1 = ((5 * count_Disp_2) - 1) + ((2 * j) + 1)
                    index2 = ((5 * count_Disp_2) - 1) + ((2 * j) + 2)
                    new_stir_data = ','.join([str(i1), \
                                              str(group_arranged[index1]), \
                                              str(group_arranged[index2]), \
                                              'true'])
                    stir_sublist_2.append(new_stir_data)
                stir_list_2[i1] = stir_sublist_2

            i3 = 8 + i1
            if globals.group_current[i3] and globals.group_current[i3] != 'empty':
                group_arranged = []
                for item in globals.group_current[i3]:
                    split_item = item.split('  ')
                    group_arranged.extend(split_item)
                count_Stir_3 = int(group_arranged[-1])
                count_Disp_3 = int(group_arranged[-2])
                stir_sublist_3 = []
                for j in range(count_Stir_3):
                    index1 = ((5 * count_Disp_3) - 1) + ((2 * j) + 1)
                    index2 = ((5 * count_Disp_3) - 1) + ((2 * j) + 2)
                    new_stir_data = ','.join([str(i1), \
                                              str(group_arranged[index1]), \
                                              str(group_arranged[index2]), \
                                              'true'])
                    stir_sublist_3.append(new_stir_data)
                stir_list_3[i1] = stir_sublist_3

        disp_list = [''] * 12
        for k in range(12):# k from 0 to 11
            if globals.group_current[k] and globals.group_current[k] != 'empty':
                group_arranged = []
                for item in globals.group_current[k]:
                    split_item = item.split('  ')
                    group_arranged.extend(split_item)
                count_Disp = int(group_arranged[-2])
                disp_data_1 = []
                for l in range(count_Disp):
                    disp_sublist = ','.join([str(group_arranged[5 * l + 0]), \
                                              str(group_arranged[5 * l + 3]), \
                                              str(group_arranged[5 * l + 2]), \
                                              str(group_arranged[5 * l + 4]), \
                                              'true'])
                    disp_data_1.append(disp_sublist)
                disp_list[k] = disp_data_1

        print("stir_list_1 is: ", stir_list_1)
        print("stir_list_2 is: ", stir_list_2)
        print("stir_list_3 is: ", stir_list_3)
        print("disp_list is: ", disp_list)

        globals.stir_data_1 = ""

        for i in range(len(stir_list_1)):
            if stir_list_1[i] != '':
                print("stir_data_1[i] is:", stir_list_1[i])
                # 分割字符串并转换为整数
                temp = stir_list_1[i][0].split(',')
                temp[1] = int(temp[1].split(' ')[0])
                temp[2] = int(temp[2].split(' ')[0]) * 1000
                # 将结果添加到字符串中
                globals.stir_data_1 += f"{temp[0]},{temp[1]},{temp[2]},{temp[3]},"
            else:
                # 处理空字符串
                globals.stir_data_1 += f"{i},0,0,false,"

        # 移除最后一个逗号
        globals.stir_data_1 = globals.stir_data_1[:-1]

        print("stir_data_1 is: ", globals.stir_data_1)

        globals.disp_dict = {}

        # 遍历列表
        for i in range(len(disp_list)):
            # 初始化空字符串
            disp_data = ""

            if isinstance(disp_list[i], list):
                for j in range(len(disp_list[i])):
                    # 分割字符串并转换为浮点数
                    temp = disp_list[i][j].split(',')
                    temp[1] = float(temp[1].split(' ')[0])
                    temp[2] = float(temp[2].split(' ')[0])
                    # 将结果添加到字符串中
                    disp_data += f"{temp[0]},{temp[1]},{temp[2]},{temp[3]},true,"
                for _ in range(4 - len(disp_list[i])):
                    # 处理空字符串
                    disp_data += f"{chr(65 + len(disp_list[i]) + _)},0.0,0,1,false,"
            else:
                for _ in range(4):
                    # 处理空字符串
                    disp_data += f"{chr(65 + _)},0.0,0,1,false,"

            # 移除最后一个逗号
            disp_data = disp_data[:-1]

            globals.disp_dict[f"disp_data_{i + 1}"] = disp_data

        for key in globals.disp_dict:
            print(f"{key} is: ", globals.disp_dict[key])

        print("dispdata111111 = ", str(globals.disp_dict['disp_data_1']))
