import numpy as np
import cv2
import sys

LEFT_PATH = sys.path[0] + "\capture\cleft\{:06d}.jpg"
RIGHT_PATH = sys.path[0] + "\capture\cright\{:06d}.jpg"

CAMERA_WIDTH = 720
CAMERA_HEIGHT = 480

left = cv2.VideoCapture(0, cv2.CAP_DSHOW)
right = cv2.VideoCapture(2, cv2.CAP_DSHOW)

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
CROP_WIDTH = 960
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]

frameId = 0

# Grab both frames first, then retrieve to minimize latency between cameras
while(True):
    if not (left.grab() and right.grab()):
        print("No more frames")
        break

    _, leftFrame = left.retrieve()
    # leftFrame = cropHorizontal(leftFrame)  # not sure if crop is needed
    _, rightFrame = right.retrieve()
    # rightFrame = cropHorizontal(rightFrame)

    # if not cv2.imwrite(LEFT_PATH.format(frameId), leftFrame):
    #     raise Exception("Could not write image")
    # if not cv2.imwrite(RIGHT_PATH.format(frameId), rightFrame):
    #     raise Exception("Could not write image")

    cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    if cv2.waitKey(40) & 0xFF == ord('q'):  # 25 fps
        break

    frameId += 1

left.release()
right.release()
cv2.destroyAllWindows()
