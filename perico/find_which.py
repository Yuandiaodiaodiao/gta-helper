from torch import device, load, no_grad, unsqueeze
import torch
from torchvision import transforms
from PIL import Image
from timeshow import timeShow
import cv2
import numpy as np


class TestCore():
    def __init__(self, net_title=""):
        d = device('cpu')
        try:
            save = load(f'./model/{net_title}', map_location=d)
            self.model = save["model"]
            self.model.eval()
            self.minisave()
        except:
            print("加载debug模型失败")
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
        torch.save({"model_static": self.model.state_dict()}, './model/model.pkl', _use_new_zipfile_serialization=False)

    def miniload(self):
        import model_class.mobilenet_v3
        self.model = model_class.mobilenet_v3.MobileNetV3_Large(num_classes=8)
        d = device('cpu')
        save = load(f'./model/model.pkl', map_location=d)
        state = save["model_static"]
        self.model.load_state_dict(state)
        self.model.eval()


if __name__ == "__main__":
    NetTitle = "mobileNet-largeBest2"
    core = TestCore(NetTitle)
    core.minisave()
    core.miniload()
    img=cv2.imread('train/4/1608275723315-1.png')
    res = core.testimg(img)
    print(res)
