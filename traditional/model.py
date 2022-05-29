import numpy as np
import sys
from ctypes import *

from cutil import *

disp_nparry = np.load(sys.path[0] + "/../cam/res_disparity.npz", allow_pickle=False)["disparity"]
# disparity = load_image(sys.path[0] + "/../cam/res_disparity.jpg", 1)
disparity = IMAGE()
disparity.w = 1200
disparity.h = 720
disparity.c = 1
parr = disp_nparry.reshape((1, 1200 * 720)).tolist()[0]
# print(parr)
# parr = [1.0, 2.0]
# disparity.data = 
carr = (c_float * len(parr))(*parr)
print(type(carr))
disparity.data = carr
print(f'HHHHHHHHHHHHHHHHHHHHHHH 0th element is {disparity.data[0]}')
deep_image = compute_depth(disparity, 150.0, 1.0)
for num in deep_image.data:
    print(num)
# print(deep_image.data)
