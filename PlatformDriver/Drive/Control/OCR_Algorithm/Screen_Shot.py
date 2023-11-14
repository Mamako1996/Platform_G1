import cv2
import time


class Screen_Shot:
    def __init__(self, index):
        self.index = index
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def shot(self):
        if self.index != 0:
            # open camera
            signal = self.cap.isOpened()
            n = 0
            while signal:
                if n > 2:
                    break
                time.sleep(2)
                ret, frame = self.cap.read()
                if n == 1:
                    cv2.imshow("Current", frame)
                time.sleep(1)
                cv2.waitKey(1) & 0xFF
                if n == 1:
                    cv2.imwrite("IMGS/Test" + str(self.index) + ".jpg", frame)
                n = n + 1
            print("save Test" + str(self.index) + ".jpg successfully!")

        cv2.destroyAllWindows()

    def release(self):
        self.cap.release()
