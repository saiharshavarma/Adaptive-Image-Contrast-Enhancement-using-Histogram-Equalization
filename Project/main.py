import cv2
import time
import sys

from wthe import WTHE

def my_time_output(string, start_time, end_time):
    print(f"{string}{(end_time - start_time) * 1000.0:.2f}ms")

if __name__ == '__main__':
    src = cv2.imread("data/cloudy.jpg", 1)

    if src is None:
        print("Can't read image file.")
        sys.exit()

    start_time = time.time()
    WTHE_dst = WTHE(src)
    end_time = time.time()
    my_time_output("WTHE处理时间: ", start_time, end_time)

    cv2.imshow("src", src)
    cv2.imshow("WTHE_dst", WTHE_dst)