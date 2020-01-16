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
            print("Reading points")
            picname = "screen.bmp"
            w, h = getscreen.getpicture(picname, mode, fullres)
            img = cv2.imread(picname)
            ans = gtapoint.solvenum(img)
            booltrue = all(map(lambda x: x >= 0, ans))
            if booltrue and piclock == False:
                # print("Delay", time.time() - beg)
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
                print("Start hacking the door")
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
    print("Hacking done")


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
            print("Please enter full screen resolution, example : 1920x1080")
            w, h = map(int, input().strip().split("x"))
            FULLRES = [w, h]
        else:
            MODE = "window"
        # win32api.MessageBox(0, f"切换模式为 {MODE}", "提醒", win32con.MB_OK)
        print(f"switch to {MODE}")
    else:
        return


if __name__ == "__main__":
    print("""
    Tutorial-----
    16:9 best
    f7 switch to fullscreen mode 
    Defaults to borderless windows and is compatible with most resolutions
    Press f7 once to switch to full screen mode !![[after press F7, needs enter full screen resolution manually]]!! 
    Press again to switch back to borderless window mode
    Bordered windows only support 1920x1080 at 200% zoom
    f8 start/restart point point point hacking twice
    f9 start/restart point point point hacking once
    f10 finger print hacking once, needs press afrer the big finger print picture shows on
    f6 shut down all the point point point hacking
    f11 start/restart point point point hacking three times
    Notice:!!! Point Hacking and Finger print hacking are the default option boxes in the upper left corner, If the option box is not in the upper left corner (the first one) before hacking, please return it manually
    About point point point hacking:
    Please press the key after plug in the USB flash drive. Or start to press when 5 points start to flash. Don't wait for the last five points to flash before pressing the crack button.
    After point point point hacking, the screenshot will continue to be taken. The performance is relatively high. If the computer is too stuck, the cracking may fail.
    config file :
     "resolution":"1920x1080", Full screen resolution
            "screenmode":"window", window/fullscreen Borderless windowing / full screen
            "keycooldown":0.01, CD time between key presses (default 10ms), If you think your computer is good, you set it to 0
            "pointcooldown":2.5 point point point hacking CD Timebetween selected positions
    """)

    with Listener(on_press=presskey) as listener:
        listener.join()
