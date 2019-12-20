import cv2
import math
import numpy as np

def rgb2hsv(rgb):
    b,g,r=rgb
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/m)*60
        else:
            h = ((g-b)/m)*60 + 360
    elif mx == g:
        h = ((b-r)/m)*60 + 120
    elif mx == b:
        h = ((r-g)/m)*60 + 240
    if mx == 0:
        s = 0
    else:
        s = m/mx
    v = mx
    h/=360
    return h, s, v

def solvepoint(img):
    height = img.shape[0]
    weight = img.shape[1]
    L = weight * 0.25
    T = height * 0.3
    picture = [0] * 6
    for i in range(6):
        picture[i] = []
        for j in range(5):
            BL = L + i * weight * 0.055
            BT = T + j * height * 0.1
            BR = BL + weight * 0.005
            BB = BT + height * 0.005
            picture[i].append([int(BT), int(BB), int(BL), int(BR)])

    return picture


def showpic(img):
    pic = solvepoint(img)
    for i in pic:
        for img in i:
            cv2.imshow("i", img)
            cv2.waitKey()


def checkimg(pos,imgo, h2=0.5178, s2=0.7004, v2=0.8902):
    # imgo=cv2.cvtColor(imgo, cv2.COLOR_BGR2HSV)
    R = 100.0
    angle = 30.0
    h = R * math.cos(angle / 180 * math.pi)
    r = R * math.sin(angle / 180 * math.pi)

    sum = 0.0
    x2 = r * v2 * s2 * math.cos(h2 / 180.0 * math.pi)
    y2 = r * v2 * s2 * math.sin(h2 / 180.0 * math.pi)
    z2 = h * (1 - v2)
    num=0
    for i in range(pos[0],pos[1]):
        for j in range(pos[2],pos[3]):
            col=imgo[i,j]
            # print(col)
            h1,s1,v1=rgb2hsv(col)
            # print(h1,s1,v1)
            x1 = r * v1 * s1 * math.cos(h1 / 180.0 * math.pi)
            y1 = r * v1 * s1 * math.sin(h1 / 180.0 * math.pi)
            z1 = h * (1 - v1)
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            sum = sum + dx * dx + dy * dy + dz * dz
            num+=1
    sum/=num
    eucli_dean = math.sqrt(sum)
    # print("eucli=",eucli_dean)
    # print(eucli_dean)
    return eucli_dean


def checkready(img):
    height = img.shape[0]
    weight = img.shape[1]
    L = weight * 0.542
    T = height * 0.126
    R = weight * 0.55
    B = weight * 0.136
    imgcheck = [int(T),int(B), int(L),int(R)]
    ans1=checkimg(imgcheck,img, 0.0196, 0.6838, 0.4588)
    # print("ans1=",ans1)
    return  ans1<40


def checkready2(img):
    height = img.shape[0]
    weight = img.shape[1]
    L = weight * 0.02
    T = height * 0.31
    R = weight * 0.03
    B = weight * 0.32
    imgcheck = [int(T),int(B), int(L),int(R)]
    ans2 = checkimg(imgcheck,img, 0.0, 0.0, 0.0)
    # print("ans2=", ans2)
    return ans2 < 20


def solvenum(img):
    if checkready(img) == False:
        return [-1] * 6
    if checkready2(img) == False:
        return [-1] * 6
    pic = solvepoint(img)
    ans = [-1] * 6
    for index1, i in enumerate(pic):
        for index, item in enumerate(i):
            if checkimg(item,img) <40:
                ans[index1] = index
                # cv2.imshow("i", item)
                # cv2.waitKey()
        if ans[index1] == -1:
            break
    return ans


if __name__ == "__main__":
    img = cv2.imread("./temp/screen1.bmp")
    ans = solvenum(img)
    print(ans)
