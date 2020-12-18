import torchvision
import time

writer = None
import os

try:
    os.mkdir("./model")
except:
    pass


# 网络模型
def timeShow(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        ans = fn(*args, **kwargs)
        print("%s cost %s second" % (fn.__name__, time.time() - start))
        return ans

    return _wrapper


from torchvision import datasets, transforms

import torch

# 玄学加速
torch.backends.cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

import torch.nn as nn

criterion = nn.CrossEntropyLoss()
from torch.autograd import Variable


def train():
    global epoch

    model.train()

    @timeShow
    def perEpoch(epoch):
        print(f"epoch{epoch}")
        showPercent = round(len(train_loader))
        avgloss = 0
        for batch_idx, (data, target) in enumerate(train_loader):
            # gpu加速
            data, target = data.cuda(non_blocking=True), target.cuda(non_blocking=True)

            optimizer.zero_grad()
            # 前向传播
            output = model(data)
            # 计算损失函数
            loss = criterion(output, target)
            # 反向传播
            loss.backward()
            scheduler.step(loss)
            # 调参
            optimizer.step()
            avgloss += loss.item()
            if batch_idx % showPercent == 0:
                print(f'{epoch} {batch_idx}/{len(train_loader)} {loss.item()}  ')
        # torch.save(model, f'./model/resnet50{epoch}')
        # torch.save(model, f'./model/resnet50Newest')
        avgloss /= len(train_loader)
        writer.add_scalar(NetTitle+"/loss", avgloss, global_step=epoch)
        writer.flush()

        print("start save")
        try:
            os.rename(f'./model/{NetTitle}Newest',f'./model/{NetTitle}Newest.bak')
        except:
            pass
        torch.save({"model": model, "optimizer": optimizer.state_dict(), "epoch": epoch}, f'./model/{NetTitle}Newest',_use_new_zipfile_serialization=False)
        print("save success")

    # 跑n遍训练集
    for i in range(1):
        perEpoch(epoch)
        epoch += 1


import math

import numpy as np
import matplotlib.pyplot as plt


def test():
    def dotest(title, loader):
        with torch.no_grad():
            model.eval()  # 设置为test模式
            correct = 0  # 初始化预测正确的数据个数为0
            total = len(loader)
            # 打log的概率
            showPercent = round(total)
            totalImg = 0
            for index, (data, target) in enumerate(loader):
                # arrayImg = data.numpy()  # transfer tensor to array
                # arrayShow = np.squeeze(arrayImg[0], 0)  # extract the image being showed
                # plt.imshow(arrayShow)  # show image
                # plt.show()
                # exit(0)
                data, target = data.cuda(non_blocking=True), target.cuda(non_blocking=True)
                # data, target = Variable(data), Variable(target)
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                correct += (predicted == target).sum().item()
                totalImg += target.size(0)
                if index % showPercent == 0:
                    pass
                    # print(f"{title}进度 {math.floor(index / total * 100)}%")
            print(f"{title}正确率 {correct}/{totalImg} = {round(correct / totalImg * 1000) / 10}%")
            return correct / totalImg

    rate1 = dotest("测试集", test_loader)
    rate2 = dotest("训练集", test_train_loader)
    return rate1, rate2


if __name__ == "__main__":
    NetTitle = "mobileNet-large-datafix"

    try:
        from tensorboardX import SummaryWriter

        writer = SummaryWriter(comment=NetTitle)
    except:
        pass

    # from alexnet import alexnet
    # modelNet = alexnet(fcoutput=1024)
    from model_class.mobilenet_v3 import MobileNetV3_Large

    modelNet = MobileNetV3_Large(num_classes=8)
    # 存档名字
    # 爆显存了就缩一缩

    lr = 0.001
    testrate = 0

    # 训练数据
    import gta_data_set

    train_loader = gta_data_set.train_loader
    # 测试数据
    test_loader = gta_data_set.test_loader
    # 训练集测试
    test_train_loader = gta_data_set.train_loader


    def changegrad(net):
        try:
            fclayer = net.classifier
        except:
            try:
                fclayer = net.fc
            except:
                try:
                    fclayer = net.linear
                except:
                    fclayer=net.linear4
        ignored_params = list(map(id, fclayer.parameters()))
        base_params = filter(lambda p: id(p) not in ignored_params, net.parameters())
        # 对不同参数设置不同的学习率
        params_list = [{'params': base_params, 'lr': 0.005}, ]
        params_list.append({'params': fclayer.parameters(), 'lr': 0.01})
        for k, v in net.named_parameters():
            v.requires_grad = True
        return params_list


    if os.path.exists(f'./model/{NetTitle}Newest'):

        save = torch.load(f'./model/{NetTitle}Newest')
        # save = torch.load(f'./model/{NetTitle}Best')
        model = save["model"]
        params_list = changegrad(model)
        model.cuda()
        optimizer = torch.optim.Adam(params_list, lr=lr,
                                     weight_decay=0.00008)
        try:
            optimizer.load_state_dict(save["optimizer"])
        except:
            pass
        epoch = save["epoch"]
        print(f"load from './model/{NetTitle}Newest'")
    else:
        print("全新训练")
        params_list = changegrad(modelNet)
        optimizer = torch.optim.Adam(params_list, lr=lr,
                                     weight_decay=0.00008)
        epoch = 0
        writer.add_graph(modelNet,(torch.rand([1,1,224,224])))
        model = modelNet.cuda()


    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.96,
                                                           patience=2 * len(train_loader), verbose=True,
                                                           threshold=0.0001, threshold_mode='rel', cooldown=1,
                                                           min_lr=0, eps=1e-08)

    rate1, rate2 = test()
    testCorrectMax = rate1
    conf=True
    conf_times=0
    while conf or conf_times<10:
        # 给👴训练到合格为止

        train()
        rate1, rate2 = test()
        writer.add_scalar(NetTitle+"/训练集", rate2, global_step=epoch)
        writer.add_scalar(NetTitle+"/测试集", rate1, global_step=epoch)

        if rate1 > testCorrectMax:
            testCorrectMax = rate1
            print("新的正确率")

            torch.save({"model": model, "optimizer": optimizer.state_dict(), "epoch": epoch},
                       f'./model/{NetTitle}Best', _use_new_zipfile_serialization=False)
        conf=rate1 < 1 or rate2 < 1
        if not conf:
            conf_times+=1
        else:
            conf_times=0
    torch.save({"model": model, "optimizer": optimizer.state_dict(), "epoch": epoch},
               f'./model/{NetTitle}BestEnd', _use_new_zipfile_serialization=False)
    pass
