import sys
import numpy as np
import cv2

LEFT_PATH = sys.path[0] + "\capture\cleft\{:06d}.jpg"
RIGHT_PATH = sys.path[0] + "\capture\cright\{:06d}.jpg"
outputFile = sys.path[0] + "\cam\\res_disparity.npz"

REMAP_INTERPOLATION = cv2.INTER_LINEAR

calibration = np.load(sys.path[0] + "\cam\calib.npz", allow_pickle=False)
imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])

CAMERA_WIDTH, CAMERA_HEIGHT = 980, 576
CROP_WIDTH = 620
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]

stereoMatcher = cv2.StereoBM_create()
stereoMatcher.setMinDisparity(4)
stereoMatcher.setNumDisparities(128)
stereoMatcher.setBlockSize(21)
stereoMatcher.setROI1(leftROI)
stereoMatcher.setROI2(rightROI)
stereoMatcher.setSpeckleRange(16)
stereoMatcher.setSpeckleWindowSize(45)
right_matcher = cv2.ximgproc.createRightMatcher(stereoMatcher);

def compute_disparity(leftFrame, rightFrame):
    # leftFrame = cropHorizontal(leftFrame)
    # leftHeight, leftWidth = leftFrame.shape[:2]
    # rightFrame = cropHorizontal(rightFrame)
    # rightHeight, rightWidth = rightFrame.shape[:2]

    # print(imageSize)
    # if (leftWidth, leftHeight) != imageSize:
    #     print("Left camera has different size than the calibration data")
    #     return

    # if (rightWidth, rightHeight) != imageSize:
    #     print("Right camera has different size than the calibration data")
    #     return
    
    # fixedLeft = cv2.remap(leftFrame, leftMapX, leftMapY, REMAP_INTERPOLATION)
    # fixedRight = cv2.remap(rightFrame, rightMapX, rightMapY, REMAP_INTERPOLATION)
    fixedLeft = leftFrame
    fixedRight = rightFrame

    grayLeft = cv2.cvtColor(fixedLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(fixedRight, cv2.COLOR_BGR2GRAY)

    left_disp = stereoMatcher.compute(grayLeft, grayRight)
    right_disp = right_matcher.compute(grayRight,grayLeft);

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(stereoMatcher);
    wls_filter.setLambda(8000.0);
    wls_filter.setSigmaColor(1.5);
    filtered_disp = wls_filter.filter(left_disp, leftFrame, disparity_map_right=right_disp);

    np.savez_compressed(outputFile, disparity = filtered_disp)

    return filtered_disp

    # cv2.imshow('original left', original_left)
    # cv2.imshow('original right', original_right)
    # cv2.imshow('left', leftFrame)
    # cv2.imshow('right', rightFrame)
    # cv2.imshow('disparity', filtered_disp / 1024)
    # if cv2.waitKey() & 0xFF == ord('q'):
    #     return
