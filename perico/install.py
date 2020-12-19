import os
#装的慢可以换源
# pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple
os.system("pip install -r requirements.txt")
os.system("pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html")
