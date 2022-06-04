import numpy as np
import cv2
import sys

LEFT_PATH = sys.path[0] + "\capture\cleft\{:06d}.jpg"
RIGHT_PATH = sys.path[0] + "\capture\cright\{:06d}.jpg"

CAMERA_WIDTH = 1000
CAMERA_HEIGHT = 800

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

frameId = 0

# Grab both frames first, then retrieve to minimize latency between cameras
while(True):
    if not (left.grab() and right.grab()):
        print("No more frames")
        break

    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()

    if frameId != 0 and frameId % 200 == 0:
        if not cv2.imwrite(LEFT_PATH.format(frameId // 200), leftFrame):
            raise Exception("Could not write image")
        if not cv2.imwrite(RIGHT_PATH.format(frameId // 200), rightFrame):
            raise Exception("Could not write image")
        print("images took" + str(frameId // 200))

    cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    if cv2.waitKey(40) & 0xFF == ord('q'):  # 25 fps
        break

    frameId += 1

left.release()
right.release()
cv2.destroyAllWindows()
