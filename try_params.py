import sys
import numpy as np
import cv2

# imgL = cv2.imread(sys.path[0] + '\scene_l.png')
# imgR = cv2.imread(sys.path[0] + '\scene_r.png')

# imgL = cv2.imread(sys.path[0] + '\left.png')
# imgR = cv2.imread(sys.path[0] + '\mright.png')

# resizedLeft = cv2.resize(imgL, (640, 480), interpolation = cv2.INTER_LINEAR)
# resizedRight = cv2.resize(imgR, (640, 480), interpolation = cv2.INTER_LINEAR)

imgL = cv2.imread(sys.path[0] + '\cmleft.png')
imgR = cv2.imread(sys.path[0] + '\cmright.png')

calibration = np.load(sys.path[0] + "\cam\calib.npz", allow_pickle=False)
imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])

window_size = 5

stereoMatcher = cv2.StereoSGBM_create(
    minDisparity=-1,
    numDisparities=3*16,
    blockSize=window_size,
    P1=8 * 3 * window_size,
    P2=32 * 3 * window_size,
    disp12MaxDiff=12,
    uniquenessRatio=10,
    speckleWindowSize=50,
    speckleRange=32,
    preFilterCap=63,
    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)
right_matcher = cv2.ximgproc.createRightMatcher(stereoMatcher);

# stereoMatcher = cv2.StereoBM_create()
# stereoMatcher.setMinDisparity(4)
# stereoMatcher.setNumDisparities(128)
# stereoMatcher.setBlockSize(9)
# stereoMatcher.setROI1(leftROI)
# stereoMatcher.setROI2(rightROI)
# stereoMatcher.setSpeckleRange(16)
# stereoMatcher.setSpeckleWindowSize(45)
# right_matcher = cv2.ximgproc.createRightMatcher(stereoMatcher)

grayLeft = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
grayRight = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
left_disp = stereoMatcher.compute(grayLeft, grayRight)
right_disp = right_matcher.compute(grayRight,grayLeft);

wls_filter = cv2.ximgproc.createDisparityWLSFilter(stereoMatcher);
wls_filter.setLambda(8000.0);
wls_filter.setSigmaColor(1.5);
filtered_disp = wls_filter.filter(left_disp, imgL, disparity_map_right=right_disp);

out = filtered_disp / 512

cv2.imshow("out", out)
cv2.imwrite(sys.path[0] + "/disp.png", out * 512 / 16)

while True:
	key = cv2.waitKey()
	if key == -1:
		break