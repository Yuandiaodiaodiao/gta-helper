import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--height', type=int, help='屏幕高度',default=1080)
parser.add_argument('--width', type=int, help='屏幕宽度',default=1920)
parser.add_argument('--tp', type=str, help='一键提高产量',default="f8")
parser.add_argument('--perico', type=str, help='佩里克指纹',default="f9")
parser.add_argument('--afk', type=str, help='自动挂机',default="")
parser.add_argument('--stop', type=str, help='急停',default="backspace")
parser.add_argument('--mode', type=str, help='显示模式 全屏 无边框 窗口',default="window")
parser.add_argument('--cast',  help='左侧指纹的切片选项',nargs="+",type=float,default=[0.317, 0.885, 0.226, 0.4165])
parser.add_argument('--modelpath',  help='模型路径',type=str,default="./model")
parser.add_argument('--keydelay',  help='按键延迟',type=float,default="0")
args = parser.parse_args()
