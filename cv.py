import cv2
import aircv as ac
import numpy as np
import getPicture
# print circle_center_pos
def draw_circle(img, pos, color, line_width):
    # cv2.rectangle(img, pos[0], pos[3],color, line_width)
    cv2.imshow('objDetect', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def threshold_demo(image):
    frame=image
    print(frame.shape)  #shape内包含三个元素：按顺序为高、宽、通道数
    height = frame.shape[0]
    weight = frame.shape[1]
    channels = frame.shape[2]
    # print("weight : %s, height : %s, channel : %s" %(weight, height, channels))
    for row in range(height):            #遍历高
        for col in range(weight):         #遍历宽
            color=frame[row,col]
            # print(color)
            if color[2]>150 and color[1]<80 and color[0]<80 :
                color[0]=0
                frame[row,col]=[0,0,0]
            # for c in range(channels):     #便利通道
            #     pv = frame[row, col, c]
            #     print(pv)     
                # frame[row, col, c] = 255 - pv
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    h, w =gray.shape[:2]
    m = np.reshape(gray, [1,w*h])
    mean = m.sum()/(w*h)
    mean=15

    ret, binary =  cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)
    binary=cv2.medianBlur(binary,3)
    binary = cv2.GaussianBlur(binary, (3, 3), 1)
    return binary

def findresult(temp,target,thor=0.3):
  
    # cv2.imshow('objDetect1', target)

    # find the match position
    pos = ac.find_template(temp, target,threshold=thor)
    if pos is None:
        print("no find")
        # cv2.imshow('objDetect', temp)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return False
    circle_center_pos = pos['rectangle']
    print("result=",circle_center_pos)
    print("confidenc=",pos["confidence"])
    color = (0, 255, 0)
    line_width = 5

    # draw circle
    # draw_circle(temp, circle_center_pos , color, line_width)
    return True
def solvepicture(img):
    img= threshold_demo(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img
def cvpic():
    target,imsrc=getPicture.getpic()
    imsrc=solvepicture(imsrc)
    ans=[]
    for imobj in target:
        x, y = imobj.shape[0:2]
        bigval = 1.31
        imobj = cv2.resize(imobj, (int(y * bigval), int(x * bigval)))
        imobj=solvepicture(imobj)
        thor=0.6
        ans.append(findresult(imsrc,imobj,thor))
    return ans
def solveonepicture(temp,imobj):
    x, y = imobj.shape[0:2]
    bigval = 1.31
    imobj = cv2.resize(imobj, (int(y * bigval), int(x * bigval)))
    imobj = solvepicture(imobj)
    thor = 0.6
    return findresult(temp,imobj,thor)
if __name__ == "__main__":
    
    for i in range(2,8):
        imsrc=cv2.imread('D:/PIC.bmp')
        imsrc=threshold_demo(imsrc)
        imsrc=cv2.cvtColor(imsrc,cv2.COLOR_GRAY2BGR)
        targetimg=f"D:/PIC{i}.bmp"
        imobj = cv2.imread(targetimg)

        x, y = imobj.shape[0:2]
        bigval=1.31
        imobj = cv2.resize(imobj, (int(y*bigval), int(x *bigval)))
        thor=0.4
        # 缩放到原来的二分之一，输出尺寸格式为（宽，高）

        imobj=threshold_demo(imobj)
        imobj=cv2.cvtColor(imobj,cv2.COLOR_GRAY2BGR)

        findresult(imsrc,imobj,thor)

    
