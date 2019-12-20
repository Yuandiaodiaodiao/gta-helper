import cv
import win32api
import win32con
import time
import getscreen
import getPicture
import ctypes
import multiprocessing

MODE = "window"
FULLRES = [1920, 1080]
LEFT = 65
DOWN = 83
UP = 87
RIGHT = 68
keycooldown = 0.00
cooldown = 4.4
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


def f11func(mode, fullres):
    cnt = 0
    pos = 0
    while cnt <= 2:
        cnt += 1
        picans = []
        piclock = False
        num = 0
        beg = time.time()
        while True:

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
                # print("getans=", ans)
                # picname = f"./temp/screen{num}.bmp"
                # w, h = getscreen.getpicture(picname, MODE, FULLRES)
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
            time.sleep(2.5)
            # print("continue")
            # print(end - beg)
    print("破解结束")


import gtapoint

f11thread = None


def presskey(key):
    global FULLRES
    global MODE

    if not hasattr(key, "name"):
        return
    if key.name == "f11":
        global f11thread
        if f11thread is None:
            f11thread = multiprocessing.Process(target=f11func, args=(MODE, FULLRES))
            f11thread.start()
        else:
            if f11thread.is_alive():
                f11thread.terminate()
            f11thread = None
            print("restart")
            f11thread = multiprocessing.Process(target=f11func, args=(MODE, FULLRES))
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
        for i in range(3):
            breakonce()
            time.sleep(cooldown)
    elif key.name == "f8":
        for i in range(4):
            breakonce()
            time.sleep(cooldown)
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
    elif key.name == 'ctrl_l':
        exit(0)
    else:
        return


if __name__ == "__main__":
    print("""
    使用教程-----
    f7 切换全屏模式 默认为无边框窗口
    按一次f7切换到全屏模式 需要f7后手动输入全屏分辨率 再按一次切回无边框窗口模式
    有边框窗口仅支持200%缩放下的1920x1080
    f8 指纹连续4次破解
    f9 指纹连续3次破解
    f10 指纹破解一次
    f6 结束所有点点破解
    f11 开始/重新开始点点破解3次
    
    """)
    with Listener(on_press=presskey) as listener:
        listener.join()
