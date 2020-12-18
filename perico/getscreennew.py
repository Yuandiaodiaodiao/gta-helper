import time
import win32gui, win32ui, win32con, win32api
import ctypes.wintypes
import numpy as np
import cv2


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
    if mode == "window" and hw > 0:
        sizeobj = get_current_size(hwnd)
    else:
        hwnd = 0
        hw = 0
        sizeobj = FULLRES

    w = sizeobj[0]
    h = sizeobj[1]
    # print(w,h)

    startw = 0
    starth = 0
    if (w > 1920 and w < 2000) and (h > 1080 and h < 1200):
        startw = (w - 1920) // 2
        starth = h - 1080
        w = 1920
        h = 1080

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
    img=img[...,0:3]
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    return img


def getpicture(gamename, mode='window', FULLRES=[1920, 1080]):
    hw = gethwnd(gamename)
    return window_capture(hw, mode, FULLRES)



def castimg(src, args,h=1,w=1):
    args=[args[0]*h,args[1]*h,args[2]*w,args[3]*w]
    args = list(map(int, args))
    return src[args[0]:args[1], args[2]:args[3],...]

if __name__ == "__main__":


    import time

    time.sleep(1)
    # img = getpicture("Cyberpunk 2077 (C) 2020 by CD Projekt RED",mode="fullscreen")
    # img = getpicture("UU加速器")
    # img=cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
    import matplotlib.pyplot as plt
    import cv2

    img = cv2.imread("img1.png")
    img720p = cv2.resize(img, (1280, 720))
    # img=cv2.cvtColor(img,cv2.COLOR_BGRA2RGB)
    imggray = cv2.cvtColor(img720p, cv2.COLOR_BGR2GRAY)
    plt.subplot(231)
    plt.imshow(imggray)

    h, w = imggray.shape
    argmap = [h * 0.31, h * 0.61, w * 0.15, w * 0.35]
    img_code_matrix = castimg(imggray, argmap)
    plt.subplot(232)
    plt.imshow(img_code_matrix)

    argmap2 = [h * 0.31, h * 0.5, w * 0.42, w * 0.6]
    img_code_needed = castimg(imggray, argmap2)
    plt.subplot(233)
    plt.imshow(img_code_needed)

    from cnocr import CnOcr
    from cnocr import consts

    ocr = CnOcr(cand_alphabet=consts.ENG_LETTERS)
    res = ocr.ocr(cv2.cvtColor(img_code_matrix, cv2.COLOR_GRAY2BGR))
    # print("Predicted Chars:", res)
    code_matrix = []
    for line in res:
        line_matrix = []
        for i in range(0, len(res) * 2, 2):
            line_matrix.append(line[i] + line[i + 1])
        code_matrix.append(line_matrix)
    print(code_matrix)
    import numpy

    code_matrix = numpy.array(code_matrix)

    res_needed = ocr.ocr(cv2.cvtColor(img_code_needed, cv2.COLOR_GRAY2BGR))
    # print(res_needed)
    res_needed = res_needed[0]
    code_needed = []
    for i in range(0, len(res_needed), 2):
        code_needed.append(res_needed[i] + res_needed[i + 1])
    print(code_needed)

    id_use = np.zeros(shape=(len(code_matrix), len(code_matrix)))

    plt.show()

    ansused = None


    def dfs(needed_index, status, lineid, used, selected, deep):
        global ansused
        if needed_index >= len(code_needed):
            ansused = used
            return True
        if deep >= 4:
            return False
        if status == 0:
            line = code_matrix[lineid]
        else:
            line = code_matrix[..., lineid]
        search_item = code_needed[needed_index]

        def isused(index):
            if status == 0:
                return used[lineid][index]
            else:
                return used[index][lineid]

        def setused(index):
            usedc = np.copy(used)
            if status == 0:
                usedc[lineid][index] = 1
            else:
                usedc[index][lineid] = 1
            return usedc

        for index, item in enumerate(line):
            # 如果是选过的 就不能选了
            if isused(index) == 1:
                continue
            if item == search_item:
                usedc = setused(index)

                res = dfs(needed_index + 1, status ^ 1, index, usedc, True, deep + 1)
                if res == True:
                    return True
        # 如果已经开始选了 还选不到就无了
        if selected == True:
            return False
        # 如果这行搞不出来结果 就乱搞一波
        for index, item in enumerate(line):
            if isused(index) == 1:
                continue
            if item != search_item:
                usedc = setused(index)
                # 保持原本的index
                res = dfs(needed_index, status ^ 1, index, usedc, False, deep + 1)
                if res == True:
                    return True
        return False


    res = dfs(0, 0, 0, id_use, False, 0)
    print(res)
    print(ansused)

    op = []
    fulldeep = np.sum(ansused)


    def searchop(status, lineid, deep, used):
        if deep >= fulldeep:
            return True
        if status == 0:
            line = used[lineid]
        else:
            line = used[..., lineid]

        def clearused(index):
            usedc = np.copy(used)
            if status == 0:
                usedc[lineid][index] = 0
            else:
                usedc[index][lineid] = 0
            return usedc

        for index, item in enumerate(line):
            if item == 1:
                unused = clearused(index)
                if status == 0:
                    op.append((lineid, index))
                else:
                    op.append((index, lineid))
                res = searchop(status ^ 1, index, deep + 1, unused)

                if res:
                    return True
                op.pop()


    ans = searchop(0, 0, 0, ansused)
    print(ans)
    print(op)
    mousex, mousey = 0, 0
    status = 0
    keyop = []


    def deltapress(delta, ops):
        opx = ['a', 'd', 'w', 's']
        opxx = opx[ops:ops + 2]
        if delta > 0:
            for i in range(delta):
                keyop.append(opxx[1])
        elif delta < 0:
            for i in range(delta):
                keyop.append(opxx[0])


    for index, item in enumerate(op):
        if index == 0:
            # 第一行特殊处理
            keyop.append("d")
            y = item[1]
            delta = y - 1
            deltapress(delta, 0)
        else:
            if status == 0:
                now = item[1]
                last = op[index - 1][1]
            else:
                now = item[0]
                last = op[index - 1][0]
            delta = now - last
            deltapress(delta, status)
        status = status ^ 1
        keyop.append('enter')

    print(keyop)
    import keyboardsim
    keybind={
        "w":keyboardsim.UP,
        "a":keyboardsim.LEFT,
        "s":keyboardsim.DOWN,
        "d":keyboardsim.RIGHT,
        'enter':keyboardsim.ENTER
    }
    key_opcode=list(map(lambda x:keybind[x],keyop))
    print(key_opcode)
    # for i in key_opcode:
    #     keyboardsim.press(i)
    #     time.sleep(0.1)
