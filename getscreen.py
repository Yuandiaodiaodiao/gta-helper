import time
import win32gui, win32ui, win32con, win32api
import ctypes.wintypes


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




def window_capture(hw, filename, mode,FULLRES):
    hwnd = hw  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    if mode == "window":
        sizeobj = get_current_size(hwnd)

    else:
        hwnd=0
        hw=0
        sizeobj = FULLRES
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()

    w = sizeobj[0]
    h = sizeobj[1]
    # print(w,h)
    catchw = w
    catchh = h
    startw=0
    starth=0
    if w==1924 and h==1130:
        startw=2
        starth=1130-1080
        catchw=1922
        catchh=1130
        w=1920
        h=1080

    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (startw, starth), win32con.SRCCOPY)
    # bmbit=saveBitMap.GetBitmapBits(False)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    return w, h


def getpicture(imgname, mode,FULLRES):
    hw = gethwnd("Grand Theft Auto V")
    return window_capture(hw, imgname, mode,FULLRES)


if __name__ == "__main__":
    beg = time.time()
    hw = gethwnd("Grand Theft Auto V")
    window_capture(hw, "screen.bmp")
    end = time.time()
    print(end - beg)
