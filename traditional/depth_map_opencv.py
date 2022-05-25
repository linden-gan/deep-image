import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time

start = time.perf_counter()

imgL = cv.imread('img/scene_l.png',0)
imgR = cv.imread('img/scene_r.png',0)
stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)

# tweak parameters
stereo.setMinDisparity(2)
stereo.setNumDisparities(16)
stereo.setBlockSize(19)
stereo.setSpeckleRange(16)
stereo.setSpeckleWindowSize(45)

disparity = stereo.compute(imgL,imgR)

end = time.perf_counter()

cv.imwrite('traditional_out/output.png', disparity)

print(f"Computation of disparity map took {end - start} seconds")


# Using cv to display result
# DEPTH_VISUALIZATION_SCALE = 256
# cv.imshow('depth', disparity / DEPTH_VISUALIZATION_SCALE)
# cv.waitKey(0) 
# cv.destroyAllWindows()

# use matplotlib to display result
plt.imshow(disparity,'gray')
plt.show()