


from pynput.keyboard import Listener
from main import singlesolve,mulsolve
from keyboardsim import press_str
from main import get_gtav_image
def presskey(key):
   t=None
   try:
      t=key.char
   except:
      pass
   if t is not None and t in ["c"]:
       from getscreen import getpicture
       img = get_gtav_image()
       import cv2
       cv2.imwrite("temp.png", img)

if __name__ == '__main__':
   print("start!")
   with Listener(on_press=presskey) as listener:
      listener.join()