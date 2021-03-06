import sys
import numpy as np
import cv2

REMAP_INTERPOLATION = cv2.INTER_LINEAR

calibration = np.load(sys.path[0] + "\cam\calib.npz", allow_pickle=False)
imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

left = cv2.VideoCapture(1, cv2.CAP_DSHOW)
right = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Increase the resolution
left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# The distortion in the left and right edges prevents a good calibration, so
# discard the edges
CROP_WIDTH = 640
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]

# Try applying brightness/contrast/gamma adjustments to the images
# window_size = 5  # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely

# stereoMatcher = cv2.StereoSGBM_create(
#     minDisparity=-1,
#     numDisparities=6*16,
#     blockSize=window_size,
#     P1=8 * 3 * window_size,
#     P2=32 * 3 * window_size,
#     disp12MaxDiff=12,
#     uniquenessRatio=10,
#     speckleWindowSize=50,
#     speckleRange=32,
#     preFilterCap=63,
#     mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
# )
window_size = 13
# stereoMatcher = cv2.StereoBM_create()
# stereoMatcher.setMinDisparity(4)
# stereoMatcher.setNumDisparities(128)
# stereoMatcher.setBlockSize(window_size)
# stereoMatcher.setROI1(leftROI)
# stereoMatcher.setROI2(rightROI)
# stereoMatcher.setSpeckleRange(16)
# stereoMatcher.setSpeckleWindowSize(45)

stereoMatcher = cv2.StereoSGBM_create(
    minDisparity=-1,
    numDisparities=5*16,
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
right_matcher = cv2.ximgproc.createRightMatcher(stereoMatcher)

frameId = 0
# Grab both frames first, then retrieve to minimize latency between cameras
while(True):
    
    if not left.grab() or not right.grab():
        print("No more frames")
        break

    _, leftFrame = left.retrieve()
    leftFrame = cropHorizontal(leftFrame)
    leftHeight, leftWidth = leftFrame.shape[:2]
    _, rightFrame = right.retrieve()
    rightFrame = cropHorizontal(rightFrame)
    rightHeight, rightWidth = rightFrame.shape[:2]

    if (leftWidth, leftHeight) != imageSize:
        print("Left camera has different size than the calibration data")
        break

    if (rightWidth, rightHeight) != imageSize:
        print("Right camera has different size than the calibration data")
        break
    # if frameId == 100:
    fixedLeft = cv2.remap(leftFrame, leftMapX, leftMapY, REMAP_INTERPOLATION)
    fixedRight = cv2.remap(rightFrame, rightMapX, rightMapY, REMAP_INTERPOLATION)

    grayLeft = cv2.cvtColor(fixedLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(fixedRight, cv2.COLOR_BGR2GRAY)
    left_disp = stereoMatcher.compute(grayLeft, grayRight)
    right_disp = right_matcher.compute(grayRight,grayLeft);

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(stereoMatcher);
    wls_filter.setLambda(8000.0);
    wls_filter.setSigmaColor(1.5);
    filtered_disp = wls_filter.filter(left_disp, leftFrame, disparity_map_right=right_disp);


    cv2.imshow('left_ori', leftFrame)
    cv2.imshow('right_ori', rightFrame)
    cv2.imshow('left', fixedLeft)
    cv2.imshow('right', fixedRight)
    cv2.imshow('disparity', filtered_disp / 512)
        # if cv2.waitKey() & 0xFF == ord('q'):
        #     break
    if cv2.waitKey(40) & 0xFF == ord('q'):
        break
    
    frameId += 1

left.release()
right.release()
cv2.destroyAllWindows()