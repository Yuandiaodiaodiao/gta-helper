from concurrent.futures import ThreadPoolExecutor, wait
RESOLUTION_PERSETS={
    "1080p":[1920,1080],
    "2k":[2560,1440],
    "4k":[3840,2160]
}
RESOLUTION=RESOLUTION_PERSETS["4k"]
from argsolver import args
from logger import logger

threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")
from pynput.keyboard import Listener
from keyboardsim import press_str
import os
import time
from ai_solve import ai_solve

import threading

def get_key_name(key):
    t=None
    try:
        t = key.char
    except:
        try:
            t = key.name
        except:
            return ""
    return t

def get_thread_id(thread):
    for id, t in threading._active.items():
        if t is thread:
            return id


def raise_exception(thread_id):
    import ctypes
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                     ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')


def whilet():
    while True:
        time.sleep(1)
        print("running")


def afk():
    while True:
        time.sleep(1)
        press_str("up")
        time.sleep(1)
        press_str('down')


def tp_hack():
    # 提高产量
    downlist = [
        1,
        3,
        9,
        26
    ]
    time.sleep(0.1)
    press_str("right")
    time.sleep(0.5)
    press_str("enter")
    time.sleep(0.5)
    for item in downlist:
        press_str("enter")
        time.sleep(1)
        for i in range(item):
            press_str("down")
        time.sleep(0.5)
    # press_str("enter")


def stop():
    global threadPool
    for thread in threadPool._threads:
        id = get_thread_id(thread)
        raise_exception(id)

    threadPool.shutdown(wait=False)


def restart():
    global threadPool
    stop()
    threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")


def presskey(key):
    global threadPool
    t = get_key_name(key)



    if t == args.tp:
        #一键提高产量
        threadPool.submit(tp_hack)

        #截图
    # if t is not None and t in ["c"]:
    #     img = get_gtav_image()
    #     import cv2
    #     cv2.imwrite("temp.png", img)
    if t == args.perico:
        # 指纹破解
        # logging.warning("submit perico")
        logger.info('perico start')
        threadPool.submit(ai_solve)
        # ai_solve()
    if t == args.afk:
        #自动挂机
        logger.info("afk start")
        threadPool.submit(afk)
    if t ==args.stop:
        #停止当前的动作
        logger.info("stop")
        restart()
    if t  =="eeeee":
        #给深度学习构建数据集
        # 采样 并切割图片 写入文件夹 创建label
        from train_data_collect import collect_data
        # threadPool.submit(collect_data)
        collect_data()
    if t == "eeeeeee":
        #调到都是0号指纹后自动破解
        for i in range(8):
            for j in range(i):
                press_str("right")
            press_str("down")
    if t == args.allstop:
        #停止进程
        stop()
        exit(0)
        raise Exception


if __name__ == '__main__':
    logger.info("start!")
    with Listener(on_press=presskey) as listener:
        listener.join()
