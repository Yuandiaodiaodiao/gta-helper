import cv2
import numpy as np


def get_img_fingerprints(gray_dct_ul64_list, gray_dct_ul64_avg):
    """
    获取图片指纹：遍历灰度图左上8*8的所有像素，比平均值大则记录为1，否则记录为0。
    :param gray_dct_ul64_list: 灰度图左上8*8的所有像素
    :param gray_dct_ul64_avg: 灰度图左上8*8的所有像素平均值
    :return: 图片指纹
    """
    img_fingerprints = ''
    avg = gray_dct_ul64_avg[0]
    for i in range(8):
        for j in range(8):
            if gray_dct_ul64_list[i][j] > avg:
                img_fingerprints += '1'
            else:
                img_fingerprints += '0'
    return img_fingerprints

def get_img_gray_bit(img, resize=(32, 32)):
    """
    获取图片指纹
    :param img: 图片
    :param resize: Resize的图片大小
    :return: 图片指纹
    """
    # 修改图片大小
    image_resize = cv2.resize(img, resize, interpolation=cv2.INTER_BITS)

    # 转换灰度图成浮点型
    image_gray_f = np.float32(image_resize)
    # 获取灰度图的DCT集合
    image_gray_dct = cv2.dct(image_gray_f)
    # 获取灰度图DCT集合的左上角8*8
    # gray_dct_ul64_list = get_gray_dct_ul64_list(image_gray_dct)
    gray_dct_ul64_list = image_gray_dct[0:8, 0:8]
    # 获取灰度图DCT集合的左上角8*8对应的平均值
    # gray_dct_ul64_avg = get_gray_dct_ul64_avg(gray_dct_ul64_list)
    gray_dct_ul64_avg = cv2.mean(gray_dct_ul64_list)
    # 获取图片指纹
    img_fingerprints = get_img_fingerprints(gray_dct_ul64_list, gray_dct_ul64_avg)
    return img_fingerprints


def get_mh(img_fingerprints1, img_fingerprints2):
    """
    获取汉明距离
    :param img_fingerprints1: 比较对象1的指纹
    :param img_fingerprints2: 比较对象2的指纹
    :return: 汉明距离
    """
    hm = 0
    for i in range(0, len(img_fingerprints1)):
        if img_fingerprints1[i] != img_fingerprints2[i]:
            hm += 1
    return hm