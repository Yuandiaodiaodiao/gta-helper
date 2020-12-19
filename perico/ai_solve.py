from keyboardsim import press_str

# import matplotlib.pyplot as plt
import cv2
import os
import time
import find_which
from prepare import *
import numpy as np
core=find_which.TestCore("mobileNet-large-datafixBestEnd")
core.miniload()

def collect_single_data():
    img=get_gtav_image()
    imgleft=prepareimage(img=img)
    lineinfo=splitline(imgleft)
    leftimgs=hsplit(imgleft,lineinfo)
    return leftimgs,imgleft


def ai_solve():
    print("collect data")
    imgs,imgleft=collect_single_data()
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
    cv2.imwrite("temp.png",imgleft)
    # for i in range(8):
    #     press_str("right")
    #     press_str("down")
    # plt.show()

if __name__=="__main__":
    collect_single_data()