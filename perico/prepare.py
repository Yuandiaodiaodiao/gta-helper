
from argsolver import  args
import cv2
import numpy as np
from getscreennew import getpicture
from logger import logger


def get_gtav_image(FULLRES=[1920,1080]):
    FULLRES=[args.width,args.height]
    logger.info(FULLRES)
    # img = getpicture("Grand Theft Auto V", mode="fullscreen", FULLRES=[3840, 2160])
    if args.mode=="fullscreen":
        img = getpicture("Grand Theft Auto V",
                         mode="fullscreen",
                         FULLRES=FULLRES)
    else:
        img=getpicture("Grand Theft Auto V",mode=args.mode,FULLRES=FULLRES)
    return img

def castimg(src, args,h=1,w=1):
    args=[args[0]*h,args[1]*h,args[2]*w,args[3]*w]
    args = list(map(int, args))
    return src[args[0]:args[1], args[2]:args[3],...]


def prepareimage(cast1=None,
                 cast2=None, img=None,
                 resize_interpolation=cv2.INTER_BITS, show=False, resize=(1280, 720)):
    hd2 = 0.003
    if cast1 is None:

        # cast1 = [0.332 - 0.015, 0.872 + 0.003+0.01, 0.226, 0.4165]
        cast1 = args.cast
    if cast2 is None:
        cast2 = [0.329 + 0.006, 0.871 + hd2, 0.538542, 0.75]
    if img is None:
        img = cv2.imread("temp.png")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img720p = img
    img720p = cv2.resize(img720p, resize, interpolation=resize_interpolation)

    h, w = img720p.shape
    imgleft = castimg(img720p, cast1, h, w)
    _, imgleft = cv2.threshold(imgleft, 60, 255, cv2.THRESH_BINARY)
    return imgleft

def splitline(imgleft):
    lh, lw = imgleft.shape
    lineinfo = []
    maxline = lw * 255
    for i in range(lh):
        linesum = np.sum(imgleft[i])
        if linesum >= maxline * 0.95:
            lineinfo.append(i)
    # print(lineinfo)
    lineinfo_unique = []
    last = -1
    temp = []
    temp2 = []
    for i in lineinfo:
        if i == last + 1:
            temp.append(i)
        else:
            if temp is not None and len(temp) > 0:
                temp2.append(temp)
            temp = [i]
        last = i
    if temp is not None and len(temp) > 0:
        temp2.append(temp)
    # print(temp2)
    # 第一个进入的线是 第一个框的上粗线
    flip = -1
    for i in temp2:
        # flip==0 取上边缘-1
        # flip==-1 取下边缘+1
        if flip == 0:
            i[flip] -= 3
        elif flip == -1:
            i[flip] += 3
        lineinfo_unique.append(i[flip])
        flip ^= -1


    if len(lineinfo_unique) % 2 != 0:
        logger.warning("警告 lineinfo不是2的倍数")
    logger.info(f"拆分为{len(lineinfo_unique)/2}份")
    return lineinfo_unique

def hsplit(image, lineinfo):
    h, w = image.shape[0], image.shape[1]
    res = []
    for start, end in zip(*([iter(lineinfo)] * 2)):
        cast = [start, end, 0, w]
        print(cast)
        ileft = castimg(image, cast)
        res.append(ileft)
    return res

def from_to(nowpos, selfid):
    if nowpos < selfid:
        # 往右直接走就行
        return selfid - nowpos
    elif nowpos == selfid:
        return 0
    else:
        # 小于 要往左走 换算成先走到0 然后再走到对应位置
        return 8 - nowpos + selfid

def rightstep_optimize(rightstep):
    rightstep %= 8
    if rightstep >= 5:
        leftstep = 8 - rightstep
        return -leftstep
    return rightstep