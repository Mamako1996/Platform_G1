import time

from PlatformDriver.Drive.Control.Data_Trans import Data_Trans
from PlatformDriver.Drive.Control.OCR_Algorithm.Checker_Images import Quick_OCR_Test
from PlatformDriver.Drive.Control.RM_Control import RM_Control
from PlatformDriver.Drive.Control.Turntable_Control import Turntable


# from PlatformDriver.Drive.Control.OCR_Algorithm.Checker_Images import Quick_OCR_Test


def Serial_Ports_tuple_Generate(serial_ports):
    COM_original = {}
    for i in range(0, len(serial_ports)):
        com = f'COM_{i + 1}'
        text = 'COM_original[\'' + com + '\']' + '= \'%s\'' % (serial_ports[i])
        exec(text)
    return COM_original


def DS_Process_Start(sd, COM):
    done = False
    count = 0
    temp_list = []
    if len(COM) != 1:
        for i in range(0, len(sd[0])):
            for j in range(0, len(sd)):
                temp_list.append(sd[j][i])

            stop = Data_Trans(1, 9600, *temp_list, **COM).data_sending()

            if not stop:
                print("error occurred!!!")
                return done
            else:
                count = count + 1
                temp_list.clear()

            time.sleep(1)
        if count == len(sd[0]):
            print("All process done!!")
            done = True
        else:
            print("%s processes missing" % (len(sd[0]) - count))
            done = False
    else:
        stop = Data_Trans(1, 9600, *sd, **COM).data_sending()
        if not stop:
            print("error occurred!!!")
            return done
        else:
            count = count + 1
            temp_list.clear()
        if count == len(sd):
            print("All process done!!")
            done = True
        else:
            print("processes missing")
            done = False
    return done


def Synthesise(data, Ports):
    COM_All = Serial_Ports_tuple_Generate(Ports)
    nextStep = DS_Process_Start(data, COM_All)
    return nextStep


def Dispensing(data, Ports):
    COM_All = Serial_Ports_tuple_Generate(Ports)
    disp_finished = False
    nextStep = False
    turntable_Home_Position_Movement(1, True)
    for i in range(len(data)):
        disp_finished = DS_Process_Start([data[i]], COM_All)
        time.sleep(1)
        print(disp_finished)
        if disp_finished:
            if i == len(data) - 1:
                break
            nextStep = turntable_One_Step_Movement_b(disp_finished)
            time.sleep(1)
        if not nextStep:
            print("turntable error occur")
            break
    time.sleep(2)
    turntable_Home_Position_Movement(len(data), True)
    return disp_finished


def SC_Process_Start(num, RM_Port):
    action = 'b'
    SC_finish = False
    for times in range(3):
        turntable_One_Step_Movement_b(True)
        time.sleep(2)
    control = RM_Control(RM_Port)
    for sets in range(num):
        finished = control.robo_arm_process(action, 0)
        if finished:
            if sets == num - 1:
                control.robo_arm_finish()
                break
            g = turntable_One_Step_Movement_g(True)
            b = turntable_One_Step_Movement_b(True)
            SC_finish = b & g
        else:
            print("An error occur in ArmControl.py")
            break
    turntable_Home_Position_Movement(num, True)
    return SC_finish


def CD_Process_Start(num, RM_Port):
    action = 'g'
    CD_finish = False
    control = RM_Control(RM_Port)
    index = 1
    for sets in range(num):
        finished = control.robo_arm_process(action, index)
        index = index + 1
        if finished:
            if sets == num - 1:
                control.robo_arm_finish()
                break
            CD_finish = turntable_One_Step_Movement_g(True)
        else:
            print("An error occur in ArmControl.py")
            break
    turntable_Home_Position_Movement(num, True)
    return CD_finish


def turntable_One_Step_Movement_b(movement):
    nextStep = False
    if movement:
        # pyautogui.click(225, 365)
        TB.turntable_One_Step_Movement_b()
        time.sleep(1)
        nextStep = True
    return nextStep


def turntable_One_Step_Movement_g(movement):
    nextStep = False
    if movement:
        # pyautogui.click(225, 823)
        TB.turntable_One_Step_Movement_g()
        time.sleep(1)
        nextStep = True
    return nextStep


def turntable_Home_Position_Movement(rel_position, movement):
    nextStep = False
    rel = 1.5
    if movement:
        # pyautogui.doubleClick(226, 314)
        # pyautogui.doubleClick(226, 772)
        TB.turntable_Home_Position_Movement()
        time.sleep(rel_position * rel + rel)
        nextStep = True
    return nextStep


#
# def buttonStart():
#     # set ports
#     stirring_ports = [globals.selected_port[0], globals.selected_port[1],
#                       globals.selected_port[2]]
#     dispensing_ports = [globals.selected_port[3]]
#     RM_port = "COM5"
#     # stirring_ports = ["COM7", "COM4", "COM6"]
#     # dispensing_ports = ["COM5"]
#
#     stir_data_1 = globals.stir_data_1
#
#     disp_data_1 = globals.disp_dict['disp_data_1']
#     disp_data_2 = globals.disp_dict['disp_data_2']
#     disp_data_3 = globals.disp_dict['disp_data_3']
#     disp_data_4 = globals.disp_dict['disp_data_4']
#     disp_data_5 = globals.disp_dict['disp_data_5']
#     disp_data_6 = globals.disp_dict['disp_data_6']
#     disp_data_7 = globals.disp_dict['disp_data_7']
#     disp_data_8 = globals.disp_dict['disp_data_8']
#     disp_data_9 = globals.disp_dict['disp_data_9']
#     disp_data_10 = globals.disp_dict['disp_data_10']
#     disp_data_11 = globals.disp_dict['disp_data_11']
#     disp_data_12 = globals.disp_dict['disp_data_12']
#
#     stir_data_01 = [stir_data_1]
#     stir_data_02 = [stir_data_1]
#     stir_data_03 = [stir_data_1]
#     disp_data_00 = [disp_data_1, disp_data_2]
#
#     stir_data_total = [stir_data_01, stir_data_02, stir_data_03]
#     disp_data_total = [disp_data_1, disp_data_2, disp_data_3, disp_data_4, disp_data_5, disp_data_6, disp_data_7,
#                        disp_data_8, disp_data_9, disp_data_10, disp_data_11, disp_data_12]
#
# # Test:
#
#     Dts = disp_data_00
#     Sts = stir_data_total
#
#     length = len(Dts)
#     Disp_finished = Dispensing(Dts, dispensing_ports)
#     if Disp_finished:
#         print("Dispensing finish")
#         stir_finished = Synthesise(Sts, stirring_ports)
#         if stir_finished:
#             print("Stirring finish")
#             char_finished = SC_Process_Start(length, RM_port)
#             time.sleep(2)
#             if char_finished:
#                 print("Coating finish")
#                 dc_finished = CD_Process_Start(length, RM_port)
#                 if dc_finished:
#                     print("Data Collection finish")
#                     All_finished = Quick_OCR_Test(length).Test_beign()
#                     if All_finished:
#                         print("Experiment Finished!!!")


# Test:
def Demo():
    RM_port = "COM5"
    stirring_ports = ["COM6", "COM8", "COM7"]
    dispensing_ports = ["COM13"]

    stir_data_1 = "0,1000,5000,true,1,1000,6000,true,2,1000,7000,true,3,1000,8000,true"
    stir_data_2 = "0,6500,4000,true,1,6500,3000,true,2,6500,2000,true,3,6500,1000,true"
    stir_data_3 = "0,6500,3000,true,1,6500,3000,true,2,6500,3000,true,3,6500,3000,true"
    stir_data_4 = "1,6500,3000,true,3,6500,1000,true,0,6500,2000,true,2,6500,4000,true"
    stir_data_5 = "1,6500,3000,true,2,6500,1000,true,3,6500,2000,true,0,6500,4000,true"
    stir_data_6 = "1,6000,3000,true,0,6500,1000,true,3,6500,2000,true,2,6500,4000,true"
    stir_data_7 = "0,6500,1000,false,1,6500,2000,false,2,6500,3000,true,3,6500,4000,true"
    stir_data_8 = "0,6500,1000,false,1,6500,2000,false,2,6500,3000,false,3,6500,4000,false"

    stir_data_9 = "0,500,6000,true,1,550,6500,true,2,600,7000,true,3,650,7500,true"
    stir_data_10 = "0,700,8000,true,1,750,8500,true,2,800,9000,true,3,850,9500,true"
    stir_data_11 = "0,900,10000,true,1,950,10500,true,2,1000,11500,true,3,1050,12000,true"
    stir_data_12 = "0,1100,12500,true,1,1150,13000,true,2,1200,13500,true,3,1250,14000,true"

    stir_data_demo = "0,700,8000,true,1,700,8000,true,2,700,8000,true,3,700,8000,true"

    disp_data_1 = "A,50.0,3,1,true,B,50.0,3,1,true,C,50.0,3,1,true,D,50.0,2,1,true"
    disp_data_2 = "A,50.0,3,1,true,B,50.0,3,2,true,C,50.0,3,3,true,D,50.0,1,4,true"
    disp_data_3 = "A,50.0,3,1,true,B,50.0,3,2,true,C,50.0,3,2,true,D,50.0,1,3,true"
    disp_data_4 = "A,50.0,1,1,true,B,50.0,1,1,true,C,50.0,1,2,true,D,50.0,1,3,true"
    disp_data_5 = "A,50.0,1,1,true,B,50.0,1,2,true,C,50.0,1,3,true,D,50.0,1,3,true"
    disp_data_6 = "A,50.0,1,1,true,B,50.0,1,2,true,C,50.0,1,1,true,D,50.0,1,2,true"
    disp_data_7 = "A,50.0,1,2,true,B,50.0,1,1,true,C,50.0,1,3,true,D,50.0,1,1,true"
    disp_data_8 = "A,50.0,1,3,true,B,50.0,1,1,true,C,50.0,1,2,true,D,50.0,1,1,true"
    disp_data_9 = "A,50.0,1,1,true,B,50.0,1,2,true,C,50.0,1,2,true,D,50.0,1,3,true"
    disp_data_10 = "A,50.0,1,1,true,B,50.0,1,1,true,C,50.0,1,2,true,D,50.0,1,3,true"
    disp_data_11 = "A,50.0,1,1,true,B,50.0,1,2,true,C,50.0,1,3,true,D,50.0,1,3,true"
    disp_data_12 = "A,50.0,2,1,true,B,50.0,2,1,true,C,50.0,2,1,true,D,50.0,2,1,true"

    stir_data_01 = [stir_data_demo]
    stir_data_02 = [stir_data_demo]
    stir_data_03 = [stir_data_demo]
    disp_data_00 = [disp_data_1, disp_data_2]

    stir_data_total = [stir_data_01, stir_data_01, stir_data_01]
    disp_data_total = [disp_data_1, disp_data_2, disp_data_3, disp_data_4, disp_data_5, disp_data_6, disp_data_7,
                       disp_data_8, disp_data_9, disp_data_10, disp_data_11, disp_data_12]

    Dts = disp_data_00
    Sts = stir_data_total

    length = len(Dts)
    Disp_finished = Dispensing(Dts, dispensing_ports)

    if Disp_finished:
        print("Dispensing finish")
        stir_finished = Synthesise(Sts, stirring_ports)
        if stir_finished:
            print("Stirring finish")
            char_finished = SC_Process_Start(length, RM_port)
            time.sleep(2)
            if char_finished:
                print("Coating finish")
                dc_finished = CD_Process_Start(length, RM_port)
                if dc_finished:
                    print("Data Collection finish")
                    All_finished = Quick_OCR_Test(length).Test_beign()
                    if All_finished:
                        TB.turntable_Windows_Close()
                    print("Experiment Finished!!!")


# # length = 3
# dc_finished = CD_Process_Start(1, RM_port)
# # if dc_finished:
# #     print("Data Collection finish")
# #     All_finished = Quick_OCR_Test(length).Test_beign()
# #     if All_finished:
# #         print("Experiment Finished!!!")

if __name__ == "__main__":
    TB = Turntable()
    Demo()
