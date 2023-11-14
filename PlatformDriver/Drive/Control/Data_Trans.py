import serial
import time


def reading_check(error):
    if error == 1:
        raise Exception("Upload failure!!", error)


class Data_Trans:
    def __init__(self, Timeout, BaudRate, *Group, **COM):
        self.Timeout = Timeout
        self.BaudRate = BaudRate
        self.Group = Group
        self.COM = COM

    def data_sending(self):
        success = False
        if not (isinstance(self.Group, tuple) & isinstance(self.COM, dict)):
            print("Please check the format about the type of parameters")
            return False

        if not (len(self.Group) == len(self.COM)):
            print("Please check the format about parameter integrity")
            return False

        if not (len(self.Group) == 0):
            serialDict = {}
            serials = list(self.Group)
            com = list(self.COM.values())
            count = 0
            for data in serials:
                serials[count] = "ser" + str(count + 1)
                serialDict.update({serials[count]: data})
                serialDict[serials[count]] = serial.Serial(com[count], self.BaudRate, timeout=self.Timeout)
                print("Parameter Settings: Serial port =%s, baud rate =%d" % (com[count], self.BaudRate))
                time.sleep(2)
                # serialDict[serials[count]].write(list(self.Group)[count].encode())
                count = count + 1
            time.sleep(1)
            for n in range(count):
                serialDict[serials[n]].write(list(self.Group)[n].encode())

            receiver = list(self.Group)
            jumper = 0

            for times in range(len(self.Group)):
                start = time.time()
                while True:
                    receiver[times] = serialDict[serials[times]].readline().decode()
                    current = time.time()

                    if "Download_Completed" in receiver[times]:
                        print("Received and completed!")
                        jumper = jumper + 1

                        break

                    if receiver[times] != '':
                        print(receiver[times])

                    if start - current >= 5:
                        reading_check(1)

                    # if receiver[times] == "Dispensing_Complete":
                    #     print("All done")
                    #     break

            if jumper == len(self.Group):
                print("Data upload successfully!")
                turn = len(self.Group)
                check = 0
                for times in range(turn):
                    while True:
                        receiver[times] = serialDict[serials[times]].readline().decode()
                        if "finished" in receiver[times]:
                            print("Processes finished")
                            success = True
                            check = check + 1
                            break
                if check == turn:
                    return success
                else:
                    print("failure")
                    return False
            else:
                print("Data upload ERROR occur!")
        return success

    def getGroup(self):
        return self.Group

    def getCOM(self):
        return self.COM

    def getTimeout(self):
        return self.Timeout

    def getBaudRate(self):
        return self.BaudRate
