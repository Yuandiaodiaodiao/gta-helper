from keyboardsim import press_str
from dc.dc_cv import getpic,solvepicture,solveonepicture
from logger import logger
def breakonce():
    targets, imsrc = getpic()
    imsrc = solvepicture(imsrc)
    # logger.info(f"")
    num = 0
    for index, imgobj in enumerate(targets):
        if solveonepicture(imsrc, imgobj):
            num += 1
            press_str("enter")
        if index != 7:
            press_str("down")
        if index == 3:
            press_str("right")
        if num >= 4:
            break
    press_str('tab')
