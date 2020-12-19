from torch import device, load, no_grad, unsqueeze
import torch
from torchvision import transforms
from PIL import Image
from timeshow import timeShow
import cv2
import numpy as np
from model_class.mobilenet_v3 import MobileNetV3_Large
from argsolver import  args
class TestCore():
    def __init__(self, net_title=""):
        d = device('cpu')
        self.gpu=False
        try:
            save = load(f'{args.modelpath}/{net_title}', map_location=d)
            self.model = save["model"]
            self.model.eval()
            self.minisave()
        except:
            # print("加载debug模型失败")
            pass
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.Grayscale(1),
            transforms.ToTensor(),
            transforms.Normalize((0.5), (0.5))
        ])

    @timeShow
    def testimg(self, img):
        with no_grad():
            # img = Image.open(imgpath)
            # img = cv2.imread(imgpath)
            img = Image.fromarray(img,mode="RGB")
            img = self.transform(img)
            tensor = unsqueeze(img, 0)
            output = self.model(tensor)
            _, ans = torch.max(output.data, 1)
            ans = ans.numpy()[0]
            return ans

    def minisave(self):
        torch.save(self.model, f"{args.modelpath}/modelall.pkl")

    def miniload(self):
        d = device('cpu')
        self.model = load(f'{args.modelpath}/modelall.pkl', map_location=d)
        self.model.eval()


if __name__ == "__main__":
    NetTitle = "mobileNet-large-datafixBestEnd"
    core = TestCore(NetTitle)
    core.miniload()

    img=cv2.imread('train/4/1608310350497-3.png')
    res = core.testimg(img)
    print(res)
