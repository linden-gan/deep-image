import numpy as np
import sys
from ctypes import *

from cutil import *


def main():
    disp_arr = np.load(sys.path[0] + "/../cam/disparity.npz", allow_pickle=False)["disparity"]
    disp_arr = disp_arr.reshape((1, 110592)).tolist()[0]
    carr = (c_float * len(disp_arr))(*disp_arr)
    disparity = make_image(110592, 1, 1, carr)
    deep_image = compute_depth(disparity, 150.0, 1.0)
    for i in range(110592):
        print(deep_image.data[i])
    # print(deep_image.data)


def make_image(w, h, c, data=None):
    im = IMAGE()
    im.w = w
    im.h = h
    im.c = c
    im.data = data
    return im


if __name__ == "__main__":
    main()
