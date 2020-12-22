import cv2
import aircv as ac
import numpy as np
from logger import logger
from prepare import get_gtav_image


def getpic():
    fullimg = get_gtav_image()
    # print(fullimg.shape)
    fullimg = cv2.resize(fullimg, (1920, 1080))
    h, w = fullimg.shape[0], fullimg.shape[1]

    # print(fullimg.shape)
    # if (w/h - 16/9) > 0.01:
    #     ww = h*16//9
    #     fullimg = fullimg[:,(w - ww)//2 :w - (ww-w)//2, :]
    #     w = h*16/9
    BL = 0.49 * w
    BT = 0.115 * h
    BR = 0.71 * w
    BB = 0.64 * h
    # print(int(BT),int(BB), int(BL),int(BR))
    bigimg = fullimg[int(BT):int(BB), int(BL):int(BR)]
    # print(bigimg.shape)
    # cv2.imshow("1", bigimg)
    # cv2.waitKey()

    BBL = 0.251 * w
    BBT = 0.257 * h
    picture = []
    for j in range(0, 5, 4):
        for i in range(0, 4):
            L = BBL + j / 4 * 0.075 * w
            T = BBT + i * 0.134 * h
            R = L + 0.0545 * w
            B = T + 0.095 * h
            picture.append(fullimg[int(T):int(B), int(L):int(R)])
    # for i in range(8):
    #     cv2.imshow("1", picture[i])
    #     cv2.waitKey()
    return picture, bigimg


def threshold_demo(image):
    frame = image
    # print(frame.shape)  # shape内包含三个元素：按顺序为高、宽、通道数
    height = frame.shape[0]
    weight = frame.shape[1]
    channels = frame.shape[2]
    # print("weight : %s, height : %s, channel : %s" %(weight, height, channels))
    for row in range(height):  # 遍历高
        for col in range(weight):  # 遍历宽
            color = frame[row, col]
            # print(color)
            if color[2] > 150 and color[1] < 80 and color[0] < 80:
                color[0] = 0
                frame[row, col] = [0, 0, 0]
            # for c in range(channels):     #便利通道
            #     pv = frame[row, col, c]
            #     print(pv)
            # frame[row, col, c] = 255 - pv
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape[:2]
    m = np.reshape(gray, [1, w * h])
    mean = m.sum() / (w * h)
    mean = 15

    ret, binary = cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)
    binary = cv2.medianBlur(binary, 3)
    binary = cv2.GaussianBlur(binary, (3, 3), 1)
    return binary


def solvepicture(img):
    img = threshold_demo(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def findresult(temp, target, thor=0.3):
    # cv2.imshow('objDetect1', target)

    # find the match position
    pos = ac.find_template(temp, target, threshold=thor)
    if pos is None:
        print("no find")
        # cv2.imshow('objDetect', temp)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return False
    circle_center_pos = pos['rectangle']
    logger.info(f"result={circle_center_pos}")
    logger.info(f"confidenc={pos['confidence']}")

    return True


def solveonepicture(temp, imobj):
    x, y = imobj.shape[0:2]
    bigval = 1.31
    imobj = cv2.resize(imobj, (int(y * bigval), int(x * bigval)))
    imobj = solvepicture(imobj)
    thor = 0.6
    return findresult(temp, imobj, thor)
