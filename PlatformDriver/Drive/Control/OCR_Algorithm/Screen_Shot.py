import cv2
import time

from PlatformDriver.Searching_root import Searching_root


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
                    root = Searching_root().print_root()
                    cv2.imwrite(root + "/Platform_G1/PlatformDriver/Drive/Control/OCR_Algorithm/IMGS/Test" + str(self.index) + ".jpg", frame)
                n = n + 1
            print("save Test" + str(self.index) + ".jpg successfully!")

        cv2.destroyAllWindows()

    def release(self):
        self.cap.release()


if __name__ == "__main__":
    print(1)
    Screen_Shot(1).shot()
