import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time

start = time.perf_counter()

imgL = cv.imread('img/scene_l.png',0)
imgR = cv.imread('img/scene_r.png',0)
stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)

end = time.perf_counter()

print(f"Computation of disparity map took {end - start} seconds")

plt.imshow(disparity,'gray')
plt.show()