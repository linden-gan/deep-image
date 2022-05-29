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

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Increase the resolution
cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# The distortion in the left and right edges prevents a good calibration, so
# discard the edges
CROP_WIDTH = 1200
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]

# Try applying brightness/contrast/gamma adjustments to the images
stereoMatcher = cv2.StereoBM_create()
stereoMatcher.setMinDisparity(4)
stereoMatcher.setNumDisparities(128)
stereoMatcher.setBlockSize(21)
stereoMatcher.setROI1(leftROI)
stereoMatcher.setROI2(rightROI)
stereoMatcher.setSpeckleRange(16)
stereoMatcher.setSpeckleWindowSize(45)

frameId = 0
leftFrame = np.zeros(imageSize)
rightFrame = np.zeros(imageSize)
original_left = np.zeros(imageSize)
original_right = np.zeros(imageSize)

outputFile = sys.path[0] + "\cam\\res_disparity"

# Grab both frames first, then retrieve to minimize latency between cameras
while(True):
    if not cam.grab():
        print("No more frames")
        break

    _, frame = cam.retrieve()
    
    if frameId == 200:
        frame = cropHorizontal(frame)
        original_right = frame
        rightFrame = cv2.remap(frame, rightMapX, rightMapY, REMAP_INTERPOLATION)
        print("Second image took")
        grayLeft = cv2.cvtColor(leftFrame, cv2.COLOR_BGR2GRAY)
        grayRight = cv2.cvtColor(rightFrame, cv2.COLOR_BGR2GRAY)
        disparity = stereoMatcher.compute(grayLeft, grayRight)
        np.savez_compressed(outputFile, disparity=disparity)

        cv2.imshow('original left', original_left)
        cv2.imshow('original right', original_right)
        cv2.imshow('left', leftFrame)
        cv2.imshow('right', rightFrame)
        cv2.imshow('disparity', disparity)
        if cv2.waitKey() & 0xFF == ord('q'):
            break
    elif frameId == 100:
        frame = cropHorizontal(frame)
        original_left = frame
        leftFrame = cv2.remap(frame, leftMapX, leftMapY, REMAP_INTERPOLATION)
        print("First image took")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frameId += 1

cam.release()
cv2.destroyAllWindows()
