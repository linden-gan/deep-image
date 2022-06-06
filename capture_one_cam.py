import numpy as np
import cv2
import sys

LEFT_PATH = sys.path[0] + "\capture\cleft_alone\{:06d}.png"
RIGHT_PATH = sys.path[0] + "\capture\cright_alone\{:06d}.png"

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Increase the resolution
cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

frameId = 0

# Grab both frames first, then retrieve to minimize latency between cameras
while(True):
    if not cam.grab():
        print("No more frames")
        break

    _, frame = cam.retrieve()
    
    if frameId != 0 and frameId % 80 == 0:
        if not cv2.imwrite(LEFT_PATH.format(frameId // 80), frame):
            raise Exception("Could not write image")
        print("left image took " + str(frameId // 80))

    cv2.imshow('cam', frame)
    if cv2.waitKey(40) & 0xFF == ord('q'):  # 25 fps
        break

    frameId += 1

cam.release()
cv2.destroyAllWindows()
