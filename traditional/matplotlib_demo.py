from cv2 import IMREAD_UNCHANGED
import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

data = np.load('traditional_out/disparity.npz')

disparity = data['disparity']

def onClick(e):
    global disparity
    if e.xdata is not None and e.ydata is not None:
        x, y = round(e.xdata), round(e.ydata)
        print(f"x = {x}, y = {y}")
        plt.title(f'disparity is: {disparity[y][x]}')
        plt.show()
    else:
        print("out of bounds")

left_img = cv.imread('img/scene_l.png', IMREAD_UNCHANGED)

img = plt.imshow(cv.cvtColor(left_img, cv.COLOR_BGR2RGB))

cid = img.figure.canvas.mpl_connect('button_press_event', onClick)
plt.show()
