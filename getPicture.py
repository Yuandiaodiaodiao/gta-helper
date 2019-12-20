import getscreen
import cv2

def getpic(mode,FULLRES):
    picname = "screen.bmp"
    w,h = getscreen.getpicture(picname,mode,FULLRES)
    # w, h = 1920, 1080
    fullimg = cv2.imread(picname)
    BL = 0.49 * w
    BT = 0.115 * h
    BR = 0.71 * w
    BB = 0.64 * h
    bigimg = fullimg[int(BT):int(BB), int(BL):int(BR)]
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
    return picture,bigimg
if __name__ == "__main__":

    getpic()