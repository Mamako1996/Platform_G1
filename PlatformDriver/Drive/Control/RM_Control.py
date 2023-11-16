import warnings

import pandas as pd
import time
import serial
from PlatformDriver.Drive.Control.OCR_Algorithm.Screen_Shot import Screen_Shot
from PlatformDriver.Searching_root import Searching_root


class RM_Control:
    def __init__(self, leArm_COM):
        self.robo_arm = LeArm_Control()
        self.robo_arm.port_init(leArm_COM)

    def robo_arm_process(self, action, index):
        return self.robo_arm.begin(action, index)

    def robo_arm_finish(self):
        self.robo_arm.end()


class LeArm_Control:
    def __init__(self):
        self.port = serial.Serial()
        self.df = None

    # Initialize port and try to connect
    def port_init(self, COM):
        self.port.port = COM
        self.port.baudrate = 9600
        self.port.bytesize = serial.EIGHTBITS
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.parity = serial.PARITY_NONE
        self.port.open()
        time.sleep(5)

    def read_csv(self, action):
        root = Searching_root().print_root()
        if action == 'b':
            self.df = pd.read_csv(root + '/Platform_G1/PlatformDriver/Drive/Control/RM_Motion_files/Bottles.csv',
                                  sep=';')
        if action == 'g':
            self.df = pd.read_csv(root + '/Platform_G1/PlatformDriver/Drive/Control/RM_Motion_files/Glasses.csv',
                                  sep=';')
        print('CSV Read successfully')
        print(self.df)

    @staticmethod
    def dec_2_hex(d):
        d_msb = int(d / (16 * 16))
        d_lsb = d - (d_msb * 16 * 16)
        h = [hex(d_msb), hex(d_lsb)]
        return h

    def begin(self, action, index):
        done = False
        self.read_csv(action)
        if self.df is None:
            done = False
            print('Action not detected')
        else:
            shape = self.df.shape
            row_count = shape[0]
            print('Total number of actions：' + str(row_count))
            for i in range(row_count):
                row = self.df.loc[i]
                is_wait = int(row['Wait'])
                if is_wait:
                    wait_time = int(row['Time']) / 1000
                    print('Wait： ' + str(wait_time) + ' s')
                    if (i != 0) & (action == 'g'):
                        Screen_Shot(index).shot()
                        index = index + 1
                        Screen_Shot(index).release()
                    else:
                        time.sleep(wait_time)
                else:
                    cmd = ''
                    cmd_list = ['55', '55']
                    motor_list = []
                    count = 0
                    for j in range(1, 7):
                        warnings.filterwarnings('ignore', message='.*Series.__getitem__.*')
                        ang = row[j]
                        if not pd.isna(ang):
                            h_ang = self.dec_2_hex(int(ang))
                            id_number = '0' + str(j)
                            motor = [id_number, h_ang[1][2:], h_ang[0][2:]]
                            motor_list = motor_list + motor
                            count = count + 1
                    h_len = hex(5 + 3 * count)
                    str_h_len = h_len[2:]
                    str_h_count = '0' + str(count)
                    head_list = [str_h_len, '03', str_h_count]
                    motion_time = int(row['Time'])
                    h_motion_time = self.dec_2_hex(motion_time)
                    time_list = [h_motion_time[1][2:], h_motion_time[0][2:]]
                    cmd_list = cmd_list + head_list + time_list + motor_list
                    for hex_obj in cmd_list:
                        if len(hex_obj) == 1:
                            cmd = cmd + '0' + hex_obj + ' '
                        else:
                            cmd = cmd + hex_obj + ' '
                    cmd = cmd[:-1]
                    cmd_bytes = bytes.fromhex(cmd)
                    self.port.write(cmd_bytes)
                    time.sleep(motion_time / 1000)
            done = True
        return done

    def end(self):
        self.port.close()


if __name__ == "__main__":
    RM_Control("COM5").robo_arm_process("g", 0)

# def start_ocr(self):
#     done = False
#     self.df = pd.read_csv('Motion_files/Glasses.csv', sep=';')
#     motions = self.df.shape[0]
#     time_usage = 0
#     for i in range(1, motions):
#         if self.df.get("Wait")[i] == 1:
#             for j in range(1, i):
#                 time_usage = time_usage + int(self.df.get("Time")[j])
#                 done = True
#     time_usage = time_usage / 1000 + 1
#     time.sleep(time_usage)
#     Screen_Shot(0, 1).shot()
#     return done
