import time
import cv2
import pytesseract
import openpyxl
import re

from PlatformDriver.Searching_root import Searching_root


def create_workBook(name):
    wb_b = openpyxl.Workbook()
    file = wb_b.active
    file.title = name
    file.append(['Number', 'UV Transmission', 'IR Transmission', 'VL Transmission', 'Time Usage', 'Threshold'])
    return wb_b, file


class Quick_OCR_Test:
    def __init__(self, num):
        self.num = num

    def Test_beign(self):
        wb, sheet = create_workBook("Testing")
        done = False
        root = Searching_root().print_root()
        # Tesseract-OCR path
        pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd = r"" + root + "\Platform_G1\PlatformDriver\Drive\Control\OCR_Algorithm\Tesseract-OCR\\tesseract.exe"
        index = 0
        for i in range(1, self.num + 1):
            index = index + 1
            # Image open
            img = cv2.imread(
                root + '/Platform_G1/PlatformDriver/Drive/Control/OCR_Algorithm/IMGS/Test' + str(i) + '.jpg')
            img = img[80:610, 250:470]

            # Resizing for scan
            img = cv2.resize(img, None, fx=0.645, fy=0.645)
            # threshold method for dividing the clearer color block
            tn = 0
            ti = 110
            threshold = 0
            start = time.perf_counter()
            print(i)

            while True:
                ret, r1 = cv2.threshold(img, ti + tn, 255, cv2.THRESH_BINARY)
                rz = cv2.cvtColor(r1, cv2.COLOR_BGR2GRAY)
                rez, rr = cv2.threshold(rz, 127, 255, cv2.THRESH_BINARY)

                # extract the text from image
                text = pytesseract.image_to_string(rr)
                text = text.replace(" ", "")
                text = text.replace(",", ".")

                testchar = 0

                # make a cell to hold the data
                a = re.findall(r'\d+\.?\d*', text)
                if len(a) == 3:
                    for n in range(3):
                        if a[n].find("100") != -1:
                            a[n] = '100'
                        if len(a[n]) > 4:
                            a[n] = a[n][0:4]
                        a[n] = str(round(float(a[n]), 1))
                    for line in text.splitlines():
                        b = re.findall(r'\d+', line)
                        if len(b) != 0:
                            if float(b[0]) > 100:
                                testchar = 1
                            else:
                                if line.find("%") != -1:
                                    for c in line:
                                        if c.isalpha():
                                            testchar = 1
                                    if (line.find(".") == -1) & (line.find("100") == -1):  # & (line.find("100") == -1)
                                        testchar = 1
                                else:
                                    if line.find("100") == -1:
                                        testchar = 1
                        else:
                            if line.find("%") != -1:
                                testchar = 1
                    if testchar == 0:
                        # print it out for checking
                        # print(text + "\n")
                        threshold = tn + ti
                        print("threshold value is " + str(tn + ti))
                        break
                    else:
                        tn += 1
                else:
                    tn += 1
                if (ti + tn) >= 255:
                    break
            a.insert(0, index)
            end = time.perf_counter()
            timing = round(end - start, 2)
            a.append(timing)
            a.append(threshold)
            print(a)
            sheet.append(a)
            print("time consuming : {:.2f}s".format(end - start))
            wb.save(root + '/Platform_G1/PlatformDriver/Drive/Control/OCR_Algorithm/Result/Testing.xlsx')
            done = True
        return done


if __name__ == "__main__":
    Quick_OCR_Test(1).Test_beign()
