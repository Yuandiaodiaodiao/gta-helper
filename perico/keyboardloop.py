from concurrent.futures import ThreadPoolExecutor

threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")
from pynput.keyboard import Listener
from main import singlesolve, mulsolve, mulsolve2
from keyboardsim import press_str
import os
import time


def afk():
    while True:
        time.sleep(1)
        press_str("up")
        time.sleep(1)
        press_str('down')


def presskey(key):
    global threadPool
    t = None
    try:
        t = key.char
    except:
        pass
    if t is not None and t in ["z"]:
        singlesolve(press_str)
    if t is not None and t in ["x"]:
        os.system('cls')
        # mulsolve2(press_str)
        threadPool.submit(mulsolve2, press_str)

    if t is not None and t in ["c"]:
        from getscreennew import getpicture
        img = getpicture("Grand Theft Auto V", mode="fullscreen", FULLRES=[3840, 2160])
        import cv2
        cv2.imwrite("temp.png", img)
    if t is not None and t in ["b"]:
        os.system('cls')
        try:

            threadPool.submit(mulsolve2, press_str)
        except:
            pass
    if t is not None and t in ["g"]:
        threadPool.submit(afk)
    if t is not None and t in ["n"]:
        threadPool.shutdown()
        threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")


if __name__ == '__main__':
    print("start!")
    with Listener(on_press=presskey) as listener:
        listener.join()
