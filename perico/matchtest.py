import cv2
import matplotlib.pyplot as plt

l, r = list(map(cv2.imread, ["left.png", "right.png"]))
from main import findresult

conf = findresult(l, r, 0, bgremove=True)
print(conf)
conf2 = findresult(r, l, 0)
print(conf2)
l, r = cv2.erode(l, None, iterations=1), cv2.erode(r, None, iterations=1)
plt.subplot(121)
plt.imshow(l)
plt.subplot(122)
plt.imshow(r)
plt.show()
conf = findresult(l, r, 0)
print(conf)
l,r=cv2.cvtColor(l,cv2.COLOR_BGR2GRAY),cv2.cvtColor(r,cv2.COLOR_BGR2GRAY)
import skimage
from skimage.metrics import structural_similarity as ssim
def ssim_match(imfil1, imfil2):
    res = ssim(imfil1, imfil2)
    return res
res=ssim_match(l,r)
print(res)