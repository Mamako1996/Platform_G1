import os
import time
from pywinauto import application
from pywinauto.application import ProcessNotFoundError
import psutil


def Plate_init(filename, check):
    pid = 0
    Name = 'ACTControllerCH'
    app = application.Application(backend="uia")
    try:
        if check == 0:
            pid = application.process_from_module(module=Name)
        if check == 1:
            raise ProcessNotFoundError
    except ProcessNotFoundError:
        os.system(
            "e: ..\\PlatformDriver\Sandboxie-Plus\SandMan.exe /box:" + filename + " E:\\MECH\Platform_G1\PlatformDriverI\ACTController\ACTControllerCH.exe")
        app.start(
            r"E:\\MECH\Platform_G1\PlatformDriver\Sandboxie-Plus\SandMan.exe /box:" + filename + " E:\\MECH\Platform_G1\PlatformDriver\ACTController\ACTControllerCH.exe")
        time.sleep(8)
        pid = application.process_from_module(module=Name)
        app.connect(process=pid)
        time.sleep(3)
        app['Dialog'].child_window(title="监视模式", control_type="Button", top_level_only=False).click()
        app['Dialog'].child_window(title="确定", control_type="Button", top_level_only=False).click()
        time.sleep(2)

    return pid


class Turntable:
    def __init__(self):
        self.b, self.g = self.Truntable_Init('ACTControllerCH.exe')

    def turntable_One_Step_Movement_b(self):
        app = application.Application(backend="uia")
        app.connect(process=self.b)
        app['Dialog'].child_window(title="实行", control_type="Button", top_level_only=False).click()

    def turntable_One_Step_Movement_g(self):
        app = application.Application(backend="uia")
        app.connect(process=self.g)
        app['Dialog'].child_window(title="实行", control_type="Button", top_level_only=False).click()

    def turntable_One_Step_Movement(self):
        appb = application.Application(backend="uia")
        appg = application.Application(backend="uia")
        appb.connect(process=self.b), appg.connect(process=self.g)
        appb['Dialog'].child_window(title="实行", control_type="Button", top_level_only=False).click()
        appg['Dialog'].child_window(title="实行", control_type="Button", top_level_only=False).click()

    def turntable_Home_Position_Movement_b(self):
        app = application.Application(backend="uia")
        app.connect(process=self.b)
        app['Dialog'].child_window(title="原点复位", control_type="Button", top_level_only=False).click()

    def turntable_Home_Position_Movement_g(self):
        app = application.Application(backend="uia")
        app.connect(process=self.g)
        app['Dialog'].child_window(title="原点复位", control_type="Button", top_level_only=False).click()

    def turntable_Home_Position_Movement(self):
        self.turntable_Home_Position_Movement_b()
        self.turntable_Home_Position_Movement_g()

    def turntable_Windows_Close(self):
        appb = application.Application(backend="uia")
        appg = application.Application(backend="uia")
        appb.connect(process=self.b)
        appg.connect(process=self.g)

        appb['Dialog']['TitleBar2'].child_window(title="关闭", control_type="Button", top_level_only=False).click()
        appb['Dialog'].child_window(title="确定", control_type="Button", top_level_only=False).click()
        appg['Dialog']['TitleBar2'].child_window(title="关闭", control_type="Button", top_level_only=False).click()
        appg['Dialog'].child_window(title="确定", control_type="Button", top_level_only=False).click()

    @staticmethod
    def Truntable_Init(name):
        count = 0
        bottles = 0
        glasses = 0

        for process in psutil.process_iter(['name']):
            if process.name() == name:
                count = count + 1
                if count == 1:
                    bottles = process.pid
                if count == 2:
                    glasses = process.pid
                    if int(glasses) < int(bottles):
                        temp = bottles
                        bottles = glasses
                        glasses = temp
                    print("Two Turntables Are Already Activated")
                    break

        if count < 2:
            bottles = Plate_init("Plate_with_bottles", 0)
            glasses = Plate_init("Plate_with_glasses", 0)
            if bottles == glasses:
                glasses = Plate_init("Plate_with_glasses", 1)

        return bottles, glasses
