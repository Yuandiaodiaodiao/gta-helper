import time
import win32gui, win32ui, win32con, win32api
import ctypes.wintypes
import numpy as np


def get_current_size(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        size = (rect.right - rect.left, rect.bottom - rect.top)
        return size


def gethwnd(hwname):
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        # if t is not "":
        #     print(h, t)
        if t == hwname:
            return h
    print(f"{hwname} 未找到")
    return 0


def window_capture(hw, mode='window', FULLRES=[1920, 1080]):
    hwnd = hw  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    if (mode == "window" or mode == "borderless") and hw > 0:
        sizeobj = get_current_size(hwnd)
    else:
        hwnd = 0
        sizeobj = FULLRES

    w = sizeobj[0]
    h = sizeobj[1]
    # print(w,h)
    startw = 0
    starth = 0

    if mode == 'window':
        # if (w > 1920 and w < 1940) and (h > 1080 and h < 1180):
        #     startw = (w - 1920) // 2
        #     starth = h - 1080
        #     w = 1920
        #     h = 1080
        # else:
        startw = (w - FULLRES[0]) // 2
        starth = h - FULLRES[1]
        w = FULLRES[0]
        h = FULLRES[1]

    # gta5用默认截取的就行
    # if mode == "window":
    #     dimensions = win32gui.GetWindowRect(hwnd)
    #     dimensions = list(dimensions)
    #     dimensions[0] += startw
    #     dimensions[1] += starth
    #     dimensions[2] = dimensions[0] + w
    #     dimensions[3] = dimensions[1] + h
    #     win32gui.SetForegroundWindow(hwnd)
    #     from PIL import ImageGrab
    #     image = ImageGrab.grab(dimensions)
    #     image=np.array(image)
    #     return image

    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()

    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (startw, starth), win32con.SRCCOPY)
    # bmbit=saveBitMap.GetBitmapBits(False)
    signedIntsArray = saveBitMap.GetBitmapBits(True)

    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img = np.reshape(img, (h, w, 4))
    img = img[..., 0:3]
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    return img


def getpicture(gamename, mode='window', FULLRES=[1920, 1080]):
    hw = gethwnd(gamename)
    return window_capture(hw, mode, FULLRES)


if __name__ == "__main__":

    def deltapress(delta, ops):
        keyop = []
        opx = ['a', 'd', 'w', 's']
        opxx = opx[ops:ops + 2]
        if delta > 0:
            for i in range(delta):
                keyop.append(opxx[1])
        elif delta < 0:
            for i in range(delta):
                keyop.append(opxx[0])
        return keyop
