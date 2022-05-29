import numpy as np
import cv2
import sys

LEFT_PATH = sys.path[0] + "\cam\cleft\{:06d}.jpg"
RIGHT_PATH = sys.path[0] + "\cam\cright\{:06d}.jpg"

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

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
    # frame = cropHorizontal(frame)

    # if frameId == 100:
    #     if not cv2.imwrite(LEFT_PATH.format(frameId), frame):
    #         raise Exception("Could not write image")
    #     print("First image took")
    # elif frameId == 200:
    #     if not cv2.imwrite(RIGHT_PATH.format(frameId), frame):
    #         raise Exception("Could not write image")
    #     print("Second image took")
    
    if frameId != 0 and frameId % 100 == 0:
        if not cv2.imwrite(LEFT_PATH.format(frameId), frame):
            raise Exception("Could not write image")
        print("image took" + str(frameId))

    cv2.imshow('cam', frame)
    if cv2.waitKey(40) & 0xFF == ord('q'):  # 25 fps
        break

    frameId += 1

cam.release()
cv2.destroyAllWindows()
