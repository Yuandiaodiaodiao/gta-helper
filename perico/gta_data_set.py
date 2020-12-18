from torch.utils.data import Dataset
from torchvision.datasets import ImageFolder
from torchvision import datasets, transforms
import torch
from PIL import Image

import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
imageTransform = transforms.Compose([
    # transforms.Resize((38, 244), Image.NEAREST),
    # transforms.RandomCrop((34, 240), padding=1),
    transforms.RandomApply(torch.nn.ModuleList([
        transforms.RandomCrop((34, 240), padding=1),
    ]), p=0.5),
    transforms.Resize((224, 224)),
    # transforms.RandomCrop((34, 240),padding=1),
    transforms.Grayscale(1),
    transforms.ToTensor(),
    transforms.Normalize((0.5), (0.5))
])

imageTransformtest = transforms.Compose([
    # transforms.Resize((36, 240),Image.NEAREST),
    # transforms.CenterCrop((34, 240)),
    transforms.Resize((224, 224)),
    transforms.Grayscale(1),
    transforms.ToTensor(),
    transforms.Normalize((0.5), (0.5))
])

trainset = ImageFolder("./train", transform=imageTransform)

train_loader = torch.utils.data.DataLoader(trainset, batch_size=64, pin_memory=True, shuffle=True,
                                           num_workers=0)
testset = ImageFolder("./train", transform=imageTransformtest)
test_loader = torch.utils.data.DataLoader(testset, batch_size=64, pin_memory=True, shuffle=False,
                                          num_workers=0)
