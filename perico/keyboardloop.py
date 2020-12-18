from concurrent.futures import ThreadPoolExecutor

threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")
from pynput.keyboard import Listener
from main import singlesolve, mulsolve, mulsolve2
from keyboardsim import press_str
import os
import time
from ai_solve import ai_solve
from main import get_gtav_image

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
        img = get_gtav_image()
        import cv2
        cv2.imwrite("temp.png", img)
    if t is not None and t in ["b"]:
        threadPool.submit(ai_solve)

        # ai_solve()
    if t is not None and t in ["g"]:
        threadPool.submit(afk)
    if t is not None and t in ["n"]:
        threadPool.shutdown()
        threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")

    if t is not None and t in ["m"]:
        #采样 并切割图片 写入文件夹 创建label
        from train_data_collect import collect_data
        # threadPool.submit(collect_data)
        collect_data()
    if t is not None and t in [","]:
        for i in range(8):
            for j in range(i):
                press_str("right")
            press_str("down")
if __name__ == '__main__':
    print("start!")
    with Listener(on_press=presskey) as listener:
        listener.join()
