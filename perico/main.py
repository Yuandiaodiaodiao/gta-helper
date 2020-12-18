from getscreennew import castimg, getpicture
import cv2
import matplotlib.pyplot as plt
import numpy as np
import aircv as ac
import time
import phash
from functools import reduce
import math
from img_trim import trim_iterative

def findresult_phash(temp,target):
    l=reduce(phash.get_mh,map(phash.get_img_gray_bit,[temp,target]))
    return l
from skimage.metrics import structural_similarity as ssim
def ssim_match(imfil1, imfil2):
    res = ssim(imfil1, imfil2)
    return res
def findresult(temp, target, thor=0.3,bgremove=False):

    # cv2.imshow('objDetect1', target)

    # find the match position
    pos = ac.find_template(temp, target, threshold=thor,bgremove=bgremove)
    if pos is None:
        # print("no find")
        return False
    circle_center_pos = pos['rectangle']
    # print("result=", circle_center_pos)
    # print("confidenc=", pos["confidence"])
    return circle_center_pos, pos["confidence"]

def cutblack(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = img[y:y + h, x:x + w]
    return crop

def prepareimage(cast1=None,
          cast2=None, img=None,
          resize_interpolation=cv2.INTER_BITS,show=False):
    hd2 = 0.003
    if cast1 is None:
        # cast1 = [0.346, 0.870+hd2, 0.226, 0.4165]
        cast1 = [0.332 + 0.006, 0.872 + hd2, 0.226, 0.4165]
    if cast2 is None:
        # cast2 = [0.329+0.006, 0.866+hd2, 0.538542, 0.75]
        # cast2 = [0.329+0.006, 0.871+hd2, 0.538542, 0.7467]
        cast2 = [0.329 + 0.006, 0.871 + hd2, 0.538542, 0.75]
    if img is None:
        img = cv2.imread("temp.png")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img720p = img
    img720p = cv2.resize(img720p, (1280, 720), interpolation=resize_interpolation)
    # plt.imshow(img720p)
    # plt.show()
    h, w = img720p.shape
    imgleft = castimg(img720p, cast1, h, w)

    _, imgleft = cv2.threshold(imgleft, 60, 255, cv2.THRESH_BINARY)
    # plt.subplot(121)
    # plt.imshow(imgleft,cmap="gray")

    imgright = castimg(img720p, cast2, h, w)
    imgright = trim_iterative(imgright)
    imgright_bgr = cv2.cvtColor(imgright, cv2.COLOR_GRAY2BGR)
    imgright = cv2.resize(imgright, (imgleft.shape[1], imgleft.shape[0]), interpolation=resize_interpolation)
    _, imgright = cv2.threshold(imgright, 60, 255, cv2.THRESH_BINARY)

    return imgleft,imgright,imgright_bgr


def splitline(imgleft):
    lh, lw = imgleft.shape
    lineinfo = [0]
    maxline = lw * 255
    for i in range(lh):
        linesum = np.sum(imgleft[i])
        if linesum >= maxline * 0.99:
            lineinfo.append(i)
    lineinfo.append(lh)
    # print(lineinfo)
    lineinfo_unique = []
    last = 0
    for i in lineinfo:
        if i != last + 1:
            lineinfo_unique.append(i)
        last = i
    return lineinfo_unique


def hsplit(image):
    lineinfo_unique=splitline(image)
    for i in range(0, len(lineinfo_unique), 2):
        start = lineinfo_unique[i]
        end = lineinfo_unique[i + 1]
        cast = [start + 5, end - 3, 0, lw]
        ileft = castimg(imgleft, cast)
        iright = castimg(imgright, cast)

def solve(cast1=None,
          cast2=None, img=None,
          resize_interpolation=cv2.INTER_BITS,show=False,save_cpu=None):
    if save_cpu is None:
        save_cpu=set()
    imgleft,imgright,imgright_bgr=prepareimage(cast1,cast2,img,resize_interpolation,show)

    lh, lw = imgleft.shape
    lineinfo_unique=splitline(imgleft)
    # print(lineinfo_unique)
    # plt.show()

    leftimgs = []
    imgs = []

    realconf = []
    bingdingls=[]
    for i in range(0, len(lineinfo_unique), 2):
        if i//2 in save_cpu:
            imgs.append(None)
            leftimgs.append(None)
            bingdingls.append(None)
            realconf.append(None)
            continue

        start = lineinfo_unique[i]
        end = lineinfo_unique[i + 1]
        cast = [start+5, end-3, 0, lw]
        ileft = castimg(imgleft, cast)
        iright = castimg(imgright, cast)

        # res = findresult(cv2.cvtColor(ileft, cv2.COLOR_GRAY2BGR),
        #                  cv2.cvtColor(iright, cv2.COLOR_GRAY2BGR),
        #                  0.01)
        res=False
        from img_trim import trim_iterative

        # ileft,iright=trim_iterative(ileft),trim_iterative(iright)
        # iright = cv2.resize(iright, (ileft.shape[1], ileft.shape[0]), interpolation=resize_interpolation)
        # _, iright = cv2.threshold(iright, 60, 255, cv2.THRESH_BINARY)

        imgs.append(iright)
        leftimgs.append(ileft)

        bigres=findresult(imgright_bgr,cv2.cvtColor(ileft, cv2.COLOR_GRAY2BGR),0.35)
        index="?"
        if bigres!=False:
            poscenter=(bigres[0][0][1]+bigres[0][1][1])/2
            percentage=poscenter/imgright_bgr.shape[0]
            index=math.floor(8*percentage)
        else:
            percentage=0
        print(f"{i // 2}位置 对应{bigres} percentage={percentage*8} index={index}")
        bingdingls.append(index)

        # res2=ssim_match(ileft,iright)
        # res=[_,res2]
        # cv2.imwrite("left.png",ileft)
        # cv2.imwrite("right.png",iright)
        # res2=findresult_phash(ileft,iright)
        # res2ls.append(res2)
        if res is not False:
            realconf.append(res[1])
        else:
            realconf.append(0)

    if show:
        submum = 1
        col=3
        for index,(l,r) in enumerate(zip(leftimgs,imgs)):
            conf = realconf[index]
            plt.subplot(len(leftimgs), col, submum)
            plt.imshow(l, cmap="gray")
            submum += 1

            plt.subplot(len(leftimgs), col, submum)
            plt.imshow(r, cmap="gray")
            submum += 1

            plt.subplot(len(leftimgs), col, submum)
            plt.text(0.5, 0, f"{int(conf * 100)}%")
            submum += 1
            # res2=res2ls[index]
            # plt.subplot(len(leftimgs), col, submum)
            # plt.text(0.5, 0, f"{int(res2 * 100)}%")
            # submum += 1
        plt.show()

    return bingdingls,realconf

def from_to(nowpos,selfid):
    if nowpos<selfid:
        # 往右直接走就行
        return selfid-nowpos
    elif nowpos==selfid:
        return 0
    else:
        # 小于 要往左走 换算成先走到0 然后再走到对应位置
        return 8-nowpos+selfid
def mulsolve2(press_str):
    ready=set()
    res_all=[]
    res_sum=[]
    for i in range(8):
        img = getpicture("Grand Theft Auto V", mode="fullscreen", FULLRES=[3840, 2160])
        res,res2 = solve(None, None, img,show=False)
        # res_sum.append(res2)
        res_all.append(res)
        for i in range(8):
            press_str("right")
            press_str("down")
    possible_ans=[]
    for i in range(8):
        possible_ans.append([])
    for i in range(8):
        for j in range(8):
            x=res_all[j][i]
            if x!='?' and x is not None:
                #表示第j轮的时候 显示的是位置x 期望的位置是i
                possible_ans[i].append((j,x))

    print(possible_ans)
    for id,indexitem in enumerate(possible_ans):
        ss=set()
        newans=[]
        for item in indexitem:
            phase = 0
            j, x = item
            delta1 = j
            phase += delta1
            # 然后看到自己在x的位置上 反推出x应该走n步right到达deep
            phase %= 8
            delta2 = from_to(x, id)
            phase += delta2
            phase %= 8
            if phase not in ss:
                ss.add(phase)
                newans.append(item)
        possible_ans[id]=newans

    print(possible_ans)
    def try_all_ans(ans,deep):
        if deep>=8:return
        # 设当前相位是0
        phase=0
        for item in possible_ans[deep]:
            #第j轮的时候 自己的位置在x的位置上
            lastphase=phase
            j,x=item
            # 那首先要phase go right j 达到第j轮的位置
            delta1=from_to(lastphase,j)
            phase+=delta1
            # 然后看到自己在x的位置上 反推出x应该走n步right到达deep
            phase%=8
            delta2=from_to(x,deep)
            phase+=delta2
            phase%=8
            # 这个位置进行操作
            delta3=from_to(lastphase,phase)
            print(f"deep={deep} delta3={delta3} delta1={delta1} delta2={delta2}")
            for i in range(delta3):
                press_str("right")

            if deep+1<8:
                press_str('down')
                try_all_ans(ans,deep+1)
                press_str('up')
    try_all_ans(possible_ans,0)
        # for index,item in enumerate(res):
        #     print(f'index={index} item={item}')
        #     if index==item or index in ready:
        #         # 当前就位的
        #         ready.add(index)
        #         press_str("down")
        #     elif item!='?':
        #         #已经定位到了 直接算出位移
        #         delta=index-item
        #         if delta<0:
        #             delta=8+delta
        #             for i in range(abs(delta)):
        #                 print("right")
        #                 press_str("right")
        #         elif delta>0:
        #
        #             for i in range(abs(delta)):
        #                 print("right")
        #                 press_str("right")
        #         ready.add(index)
        #         press_str("down")
        #     else:
        #         # 找不到  下一个
        #         print("right")
        #         press_str("right")
        #         press_str("down")
        #         pass
        #
        # if len(ready)==8:
        #     break
    print(possible_ans)
    # for i in res_sum:
    #     print(i)
def mulsolve(press_str):
    res_all=[]
    for i in range(8):
        time.sleep(0.1)
        res=singlesolve(press_str,show=False)

        # print(list(map(lambda x:int(x*100),res)))
        res_all.append(res)
    print("the ans is!")

    plt.show()
    for i in res_all:
        print(i)
    bestans=[]
    for i in range(8):
        maxnum=0
        maxid=None
        for j in range(8):
            # if res_all[j][i]>maxnum:
            #     maxnum=res_all[j][i]
            #     maxid=j
            if res_all[j][i]==i:
                bestans.append([j,0])
        # bestans.append([maxid,int(maxnum*100)])

    print(bestans)
    # for i in bestans:
    #     for j in range(i[0]):
    #         press_str("right")
    #     press_str("down")


def singlesolve2(press_str,show=False):
    img = getpicture("Grand Theft Auto V",mode="fullscreen",FULLRES=[3840,2160])
    res = solve(None, None, img,show=show)
    # print(res)
    keylist = []
    for i in res:
        keylist.append("right")
        keylist.append("down")

        # 至少有一个 没有匹配

            # if i != 0:
            #     keylist.append("down")
            # else:
            #     keylist.append("right")
            #     keylist.append("down")
    # print(keylist)
    for i in keylist:
        press_str(i)
    return res

def singlesolve(press_str,show=False):
    img = getpicture("Grand Theft Auto V",mode="fullscreen",FULLRES=[3840,2160])
    # plt.imshow(img)
    # plt.show()
    res = solve(None, None, img,show=show)
    plt.show()
    # print(res)
    keylist = []
    for i in res:
        keylist.append("right")
        keylist.append("down")

        # 至少有一个 没有匹配

            # if i != 0:
            #     keylist.append("down")
            # else:
            #     keylist.append("right")
            #     keylist.append("down")
    # print(keylist)
    for i in keylist:
        press_str(i)
    return res

def train():
    import copy
    cast2_template = [0.332, 0.873, 0.226, 0.417]
    rightans_num = 6
    img = cv2.imread("img1.png")
    img = cv2.resize(img, (1920, 1080))
    maxconfs = sum(solve(None, None, img))
    # for i in range(10):
    #     for i in range(0, 4):
    #         maxans = None
    #         for delta in range(-100, 100, 1):
    #             # print(f"delta={delta}")
    #             cast2 = copy.deepcopy(cast2_template)
    #             cast2[i] = cast2_template[i] + delta / 100 / 10000
    #             confs = solve(cast2_template, None, img)
    #             if len(confs) == rightans_num and sum(confs) > maxconfs:
    #                 maxconfs = sum(confs)
    #                 maxans = cast2
    #         if maxans is not None:
    #             cast2_template = maxans
    #             print(f"conf={maxconfs},args={maxans}")
    methods = [cv2.INTER_AREA,
               cv2.INTER_BITS,
               cv2.INTER_BITS2,
               cv2.INTER_CUBIC,
               cv2.INTER_LANCZOS4,
               cv2.INTER_LINEAR]
    maxconfs = 0
    maxans = 0
    for m in methods:
        # print(f"delta={delta}")
        confs = solve(None, None, img, m)
        print(f"m={m} conf={sum(confs)}")
        if len(confs) == rightans_num and sum(confs) > maxconfs:
            maxconfs = sum(confs)
            maxans = m
    print(f"conf={maxconfs},methods={maxans}")


# 右边大图973
# 左边958

if __name__ == "__main__":
    # train()
    solve(show=True)
    plt.show()
