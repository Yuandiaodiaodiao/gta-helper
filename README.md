# looking for english version?
[english-version](https://github.com/Yuandiaodiaodiao/gta-helper/tree/englist-version)
# gta-helper v1.0 is coming!  
## gta新dlc 佩里克岛劲爆来袭 挑战指纹最速传说  
- UI-> Vue3.0 + vite + elementui-plus +electron  
- 后端使用mobilenetv3作为核心模型0.05秒识别一个指纹区域  
- 全屏 无边框 窗口化 全面适配  
### 使用方法  
    1.前往https://github.com/Yuandiaodiaodiao/gta-helper/releases 下载最新版本  
2.百度云下载  
3.clone项目 本地构建 详细构建方法可见.github/workflows  
### 核心思路
首先 这次的每个小格子都是有顺序的 也就是说如果当前格子里是第一个  
你想要他是第四个 那直接往右4个就好了
但是如何识别呢 这就是难点了 左侧的指纹相比右侧有轻微的缩放位移  
通过传统方法 比如cv的模板匹配等,很难直接从左侧找到是右边的第几个
所以我们直接使用暴力方式 把一共7组指纹的 8*8*7一共448张小图直接喂给神经网络  
然后摁学习出这个小图是第几个  由于cnn具有平移,缩放的一致性  
这么点缩放根本不在话下,很快啊 就识别出来了.
然后就是根据位置进行向左或者向右的调整
前后端通信使用的是前端给后端传main函数参数的形式
这样重载起来方便 js读取和保存json也十分方便

## 对于非16:9屏幕的兼容
每次f9玩指纹游戏之后 程序会在安装目录下生成temp.png
开启主菜单中的高级选项后有4个裁切比例可以选 分别对应上下侧高度百分比 和左右侧宽度百分比  
四个参数框住的就是temp.png 
你需要将其调整到合适的比例使得截出来的图和16:9截出来的图相似  
重点是上下的外框要截到
图中的是1080p下的 4k分辨率下会宽一些 
![temp.png](README.assets/temp.png)



## LICENSE
    gta-helper
    Copyright (C) 2020  yuandiaodiaodiao

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# gta-helper-old
gtaV 名钻 dc 破解
## 部署  
python 3.6+ (本人py37)  
- pip install -r requirements.txt  
启动gta-finger.py
## 配置文件 config.json  
  ```json
 {"resolution":"1920x1080", //全屏化分辨率
            "screenmode":"window", //window/fullscreen 无边框窗口化/全屏
            "keycooldown":0.01, //按键抬起之间的冷却(默认10ms)觉得自己电脑可以的可以调成0
            "pointcooldown":2.5 //点点点两次选位置之间的冷却
}
  ```

## 打包
pack.py
## 预打包
链接: https://pan.baidu.com/s/1pHOQDSd0R0YwmiohUyoFGA   
提取码: 6y4z 复制这段内容后打开百度网盘手机App，操作更方便哦

   
