from keyboardsim import press_str
from main import get_gtav_image,prepareimage,splitline,hsplit
import matplotlib.pyplot as plt
import cv2
import os
import time

def collect_single_data():
    img=get_gtav_image()
    imgleft,_,_=prepareimage(img=img)
    lineinfo=splitline(imgleft)
    leftimgs=hsplit(imgleft,lineinfo)
    return leftimgs
def collect_data():
    print("collect data")
    for i in range(8):
        #收集数据
        imgs=collect_single_data()
        try:
            os.mkdir(f"./train/{i}")
        except:
            pass
        for index,img in enumerate(imgs):

            cv2.imwrite(f"./train/{i}/{str(int(time.time()*1000))}-{index}.png",img)
        for i in range(8):
            press_str("right")
            press_str("down")
        time.sleep(0.1)


if __name__=="__main__":
    collect_single_data()