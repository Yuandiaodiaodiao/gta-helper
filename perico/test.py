import torch
import torch.nn as nn
from prepare import get_gtav_image,prepareimage
import cv2
import win32api

img = get_gtav_image()
print(img.shape)
imgleft=prepareimage(img=img)
cv2.imwrite('temp.png',imgleft)
exit(0)
import alexnet
model=alexnet.alexnet(fcoutput=512)
from model_class.mobilenet_v3 import MobileNetV3_Large
model=MobileNetV3_Large(num_classes=8)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
# from torchsummary import summary
# summary(model, input_size=(1, 224, 224))
# summary(model, input_size=(1, 244, 244))



# m = nn.MaxPool2d(3, stride=2)
# # pool of non-square window
# m = nn.MaxPool2d((3, 2), stride=(2, 1))
# input = torch.randn(64, 16, 3)
# output = m(input)
# print(output)