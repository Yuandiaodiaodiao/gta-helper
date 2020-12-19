dellist = ["caffe2_detectron_ops.dll", 'opencv_videoio_ffmpeg440_64.dll']

import shutil

import os
os.system("pyinstaller ./keyboardloop.py -y")


try:
    try:
        os.mkdir("./dist/keyboardloop/model")
    except:
        pass
    shutil.copy("./model/modelall.pkl","./dist/keyboardloop/model/modelall.pkl")

    for root, dirs, files in os.walk("./dist/keyboardloop/torch/lib", topdown=False):
        for name in files:
            if ".lib" in name or name in dellist:
                try:
                    os.remove(os.path.join(root, name))
                except:
                    pass
    for root, dirs, files in os.walk("./dist/keyboardloop/cv2", topdown=False):
        for name in files:
            if ".lib" in name or name in dellist:
                try:
                    os.remove(os.path.join(root, name))
                except:
                    pass

    try:
        shutil.rmtree("../ui/keyboardloop")
    except:
        pass
    shutil.move("./dist/keyboardloop","../ui/keyboardloop")
except:
    pass
print("pack success")
