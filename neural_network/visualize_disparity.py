# mobilestereonet requires kittitest pngs to be less than 1248x384

import numpy as np
import cv2 as cv

name = 'YOUR NAME HERE'
model_num = 1

data = np.load(f'left/{name}.npz')

disp = data['disparity']

cv.imwrite(f'output_{name}_{model_num}.png', disp * 16)
