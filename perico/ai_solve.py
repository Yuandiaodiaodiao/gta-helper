from keyboardsim import press_str
from main import get_gtav_image,prepareimage,splitline,hsplit
import matplotlib.pyplot as plt
import cv2
import os
import time
import find_which
from main import from_to
import numpy as np
core=find_which.TestCore("mobileNet-large-datafixBest1")
core.miniload()
def collect_single_data():
    img=get_gtav_image()
    imgleft,_,_=prepareimage(img=img)
    lineinfo=splitline(imgleft)
    leftimgs=hsplit(imgleft,lineinfo)
    return leftimgs

def rightstep_optimize(rightstep):
    rightstep%=8
    if rightstep>=5:
        leftstep=8-rightstep
        return -leftstep
    return rightstep
def ai_solve():
    print("collect data")
    imgs=collect_single_data()
    for index,img in enumerate(imgs):
        # plt.subplot(8,1,index+1)
        # plt.imshow(img)

        res=core.testimg(cv2.cvtColor(img,cv2.COLOR_GRAY2RGB))
        # res=core.testimg(np.reshape(img,(img.shape[0],img.shape[1],1)))
        rightstep=from_to(res,index)
        rightstep=rightstep_optimize(rightstep)
        print(f"{res} -> {index}  {rightstep}")

        for i in range(abs(rightstep)):
            if rightstep>0:
                press_str("right")
            else:
                press_str("left")
        press_str("down")
    # for i in range(8):
    #     press_str("right")
    #     press_str("down")
    plt.show()

if __name__=="__main__":
    collect_single_data()