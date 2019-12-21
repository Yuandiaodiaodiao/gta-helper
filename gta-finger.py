import cv
import win32api
import win32con
import time
import getscreen
import getPicture
import ctypes
import multiprocessing
import os
import json
if not os.path.exists("config.json"):
    with open("config.json",'w')as f:
        json.dump({
            "resolution":"1920x1080",
            "screenmode":"window",
            "keycooldown":0.01,
            "pointcooldown":2.5
        },f)

# MODE = "window"
# FULLRES = [1920, 1080]
LEFT = 65
DOWN = 83
UP = 87
RIGHT = 68
# keycooldown = 0.01
# pointcooldown = 2.5
with open("config.json","r")as f:

    js=json.load(f)
    MODE=js["screenmode"]
    x,y=map(int,js["resolution"].strip().split("x"))
    FULLRES=[x,y]
    keycooldown=js["keycooldown"]
    pointcooldown=js["pointcooldown"]
import cv2

import threading


def press(key):
    MapKey = ctypes.windll.user32.MapVirtualKeyA
    win32api.keybd_event(key, MapKey(key, 0), 0, 0)
    time.sleep(keycooldown)
    win32api.keybd_event(key, MapKey(key, 0), win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(keycooldown)


from pynput.keyboard import Listener


def breakonce():
    global MODE
    targets, imsrc = getPicture.getpic(MODE, FULLRES)
    imsrc = cv.solvepicture(imsrc)
    num = 0
    for index, imgobj in enumerate(targets):
        if cv.solveonepicture(imsrc, imgobj):
            num += 1
            press(13)
        if index != 7:
            press(DOWN)
        if index == 3:
            press(RIGHT)
        if num >= 4:
            break
    press(9)


def f11func(mode, fullres, cntnum=2,pointcd=2.5):
    cnt = 0
    pos = 0
    while cnt <= cntnum:
        cnt += 1
        picans = []
        piclock = False
        num = 0
        beg = time.time()
        while True:
            print("正在读取点")
            picname = "screen.bmp"
            w, h = getscreen.getpicture(picname, mode, fullres)
            img = cv2.imread(picname)
            ans = gtapoint.solvenum(img)
            booltrue = all(map(lambda x: x >= 0, ans))
            if booltrue and piclock == False:
                # print("间隔", time.time() - beg)
                beg = time.time()
                piclock = True
                if picans == ans:
                    num += 1
                else:
                    picans = ans
                    num = 0

            elif booltrue and piclock == True:
                piclock = False
                beg = time.time()
            if num > 0 and time.time() - beg > 1:
                print("开始破解")
                break

        # print("picans=", picans)
        for i in picans:
            while True:
                move = i - pos
                if move > 0:
                    press(DOWN)
                    pos += 1
                elif move < 0:
                    press(UP)
                    pos -= 1
                else:
                    break
            press(13)
            time.sleep(pointcd)
            # print("continue")
            # print(end - beg)
    time.sleep(2)
    print("破解结束")


import gtapoint

f11thread = None


def presskey(key):
    global FULLRES
    global MODE
    global f11thread
    global pointcooldown
    if not hasattr(key, "name"):
        return
    if key.name == "f11":
        print("restart")
        if f11thread is not None and f11thread.is_alive():
            f11thread.terminate()
        f11thread = multiprocessing.Process(target=f11func, args=(MODE, FULLRES,2,pointcooldown))
        f11thread.start()
    if key.name == "f6":
        if f11thread is None:
            pass
        elif f11thread.is_alive():
            f11thread.terminate()
        f11thread = None
        print("stop")
    if key.name == "f10":
        breakonce()
    elif key.name == "f9":
        print("restart")
        if f11thread is not None and f11thread.is_alive():
            f11thread.terminate()
        f11thread = multiprocessing.Process(target=f11func, args=(MODE, FULLRES, 0,pointcooldown))
        f11thread.start()
    elif key.name == "f8":
        print("restart")
        if f11thread is not None and f11thread.is_alive():
            f11thread.terminate()
        f11thread = multiprocessing.Process(target=f11func, args=(MODE, FULLRES, 1,pointcooldown))
        f11thread.start()
    elif key.name == "f7":
        if MODE == "window":
            MODE = "fullscreen"
            print("请输入全屏分辨率 如 1920x1080")
            w, h = map(int, input().strip().split("x"))
            FULLRES = [w, h]
        else:
            MODE = "window"
        # win32api.MessageBox(0, f"切换模式为 {MODE}", "提醒", win32con.MB_OK)
        print(f"切换为 {MODE}")
    else:
        return


if __name__ == "__main__":
    print("""
    使用教程-----
    游戏模式最好为16:9
    f7 切换全屏模式 
    默认为无边框窗口并且兼容大部分分辨率
    按一次f7切换到全屏模式 !![[需要f7后手动输入全屏分辨率]]!! 
    再按一次切回无边框窗口模式
    有边框窗口仅支持200%缩放下的1920x1080
    f8 开始/重新开始点点破解2次
    f9 开始/重新开始点点破解1次
    f10 指纹破解一次 需要在大指纹显示出来之后再按!!!!
    f6 结束所有点点破解
    f11 开始/重新开始点点破解3次
    注意:!!! 点点点和指纹 都是默认选项框在左上角的 如果破解之前选项框不在左上角(第一个)请手动归位
    关于点点点破解:
    请在插入u盘之后开始按键 或者在5个点开始闪烁的时候开始按键 不要等五个点最后一次闪完了再按破解键
    点点点破解开始后会持续进行屏幕截图 比较吃性能 如果电脑太卡可能会导致破解失败
    配置文件说明:
     "resolution":"1920x1080", 全屏化分辨率
            "screenmode":"window", window/fullscreen 无边框窗口化/全屏
            "keycooldown":0.01, 按键抬起之间的冷却(默认10ms)觉得自己电脑可以的可以调成0
            "pointcooldown":2.5 点点点两次选位置之间的冷却
    """)

    with Listener(on_press=presskey) as listener:
        listener.join()
