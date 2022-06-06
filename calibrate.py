import glob
import os
import random
import sys

import numpy as np
import cv2

CHESSBOARD_SIZE = (7, 5)

OBJECT_POINT_ZERO = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3),
        np.float32)
OBJECT_POINT_ZERO[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0],
        0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

TERMINATION_CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30,
        0.001)

OPTIMIZE_ALPHA = 0.25

MAX_IMAGES = 64

leftDir = sys.path[0] + "\capture\cleft_alone"
rightDir = sys.path[0] + "\capture\cright_alone"
leftImageDir = sys.path[0] + "\capture\cleft"
rightImageDir = sys.path[0] + "\capture\cright"
outputFile = sys.path[0] + "\cam\calib"

CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480

def readImagesAndFindChessboards(imageDirectory):
    print("Reading images at {0}".format(imageDirectory))
    imagePaths = glob.glob("{0}/*.png".format(imageDirectory))

    filenames = []
    objectPoints = []
    imagePoints = []
    imageSize = None

    for imagePath in sorted(imagePaths):
        image = cv2.imread(imagePath)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        newSize = grayImage.shape[::-1]
        if imageSize != None and newSize != imageSize:
            raise ValueError(
                    "Calibration image at {0} is not the same size as the others"
                    .format(imagePath))
        imageSize = newSize

        hasCorners, corners = cv2.findChessboardCorners(grayImage,
                CHESSBOARD_SIZE, cv2.CALIB_CB_FAST_CHECK)

        if hasCorners:
            filenames.append(os.path.basename(imagePath))
            objectPoints.append(OBJECT_POINT_ZERO)
            cv2.cornerSubPix(grayImage, corners, (11, 11), (-1, -1),
                    TERMINATION_CRITERIA)
            imagePoints.append(corners)

        cv2.drawChessboardCorners(image, CHESSBOARD_SIZE, corners, hasCorners)
        cv2.imshow(imageDirectory, image)
        cv2.waitKey(1)

    cv2.destroyWindow(imageDirectory)

    print("Found corners in {0} out of {1} images"
            .format(len(imagePoints), len(imagePaths)))

    return filenames, objectPoints, imagePoints, imageSize

(_, leftObjectPoints, leftImagePoints, leftSize
        ) = readImagesAndFindChessboards(leftDir)
(_, rightObjectPoints, rightImagePoints, rightSize
        ) = readImagesAndFindChessboards(rightDir)

if leftSize != rightSize:
    print("Camera resolutions do not match")
    sys.exit(1)

(leftFilenames, leftObjectPoints_sync, leftImagePoints_sync, leftSize
        ) = readImagesAndFindChessboards(leftImageDir)
(rightFilenames, rightObjectPoints_sync, rightImagePoints_sync, rightSize
        ) = readImagesAndFindChessboards(rightImageDir)

if leftSize != rightSize:
    print("Camera resolutions do not match")
    sys.exit(1)
imageSize = leftSize

filenames = list(set(leftFilenames) & set(rightFilenames))
if (len(filenames) > MAX_IMAGES):
    print("Too many images to calibrate, using {0} randomly selected images"
            .format(MAX_IMAGES))
    filenames = random.sample(filenames, MAX_IMAGES)
filenames = sorted(filenames)
print("Using these images:")
print(filenames)

def getMatchingObjectAndImagePoints(requestedFilenames,
        allFilenames, objectPoints, imagePoints):
    requestedFilenameSet = set(requestedFilenames)
    requestedObjectPoints = []
    requestedImagePoints = []

    for index, filename in enumerate(allFilenames):
        if filename in requestedFilenameSet:
            requestedObjectPoints.append(objectPoints[index])
            requestedImagePoints.append(imagePoints[index])

    return requestedObjectPoints, requestedImagePoints

leftObjectPoints_sync, leftImagePoints_sync = getMatchingObjectAndImagePoints(filenames,
        leftFilenames, leftObjectPoints_sync, leftImagePoints_sync)
rightObjectPoints_sync, rightImagePoints_sync = getMatchingObjectAndImagePoints(filenames,
        rightFilenames, rightObjectPoints_sync, rightImagePoints_sync)

if not np.array_equiv(leftObjectPoints_sync, rightObjectPoints_sync):
    print("Object points do not match")
    sys.exit(1)

print("Calibrating left camera...")
_, leftCameraMatrix, leftDistortionCoefficients, _, _ = cv2.calibrateCamera(
        leftObjectPoints, leftImagePoints, imageSize, None, None)

print("Calibrating right camera...")
_, rightCameraMatrix, rightDistortionCoefficients, _, _ = cv2.calibrateCamera(
        rightObjectPoints, rightImagePoints, imageSize, None, None)

leftCameraMatrix, roi=cv2.getOptimalNewCameraMatrix(leftCameraMatrix, 
                                                    leftDistortionCoefficients,
                                                    (CAMERA_WIDTH,CAMERA_HEIGHT),
                                                    1,
                                                    (CAMERA_WIDTH,CAMERA_HEIGHT))

rightCameraMatrix, roi=cv2.getOptimalNewCameraMatrix(rightCameraMatrix,
                                                     rightDistortionCoefficients,
                                                     (CAMERA_WIDTH,CAMERA_HEIGHT),
                                                     1,
                                                     (CAMERA_WIDTH,CAMERA_HEIGHT))

print("Calibrating cameras together...")
(_, _, _, _, _, rotationMatrix, translationVector, _, _) = cv2.stereoCalibrate(
        leftObjectPoints_sync, leftImagePoints_sync, rightImagePoints_sync,
        leftCameraMatrix, leftDistortionCoefficients,
        rightCameraMatrix, rightDistortionCoefficients,
        imageSize, None, None, None, None,
        cv2.CALIB_FIX_INTRINSIC, TERMINATION_CRITERIA)

print("Rectifying cameras...")
(leftRectification, rightRectification, leftProjection, rightProjection,
        dispartityToDepthMap, leftROI, rightROI) = cv2.stereoRectify(
                leftCameraMatrix, leftDistortionCoefficients,
                rightCameraMatrix, rightDistortionCoefficients,
                imageSize, rotationMatrix, translationVector,
                None, None, None, None, None,
                cv2.CALIB_ZERO_DISPARITY, OPTIMIZE_ALPHA)

print("Saving calibration...")
leftMapX, leftMapY = cv2.initUndistortRectifyMap(
        leftCameraMatrix, leftDistortionCoefficients, leftRectification,
        leftProjection, imageSize, cv2.CV_32FC1)
rightMapX, rightMapY = cv2.initUndistortRectifyMap(
        rightCameraMatrix, rightDistortionCoefficients, rightRectification,
        rightProjection, imageSize, cv2.CV_32FC1)

np.savez_compressed(outputFile, imageSize=imageSize,
        leftMapX=leftMapX, leftMapY=leftMapY, leftROI=leftROI,
        rightMapX=rightMapX, rightMapY=rightMapY, rightROI=rightROI)


# Code to test the calibration

# REMAP_INTERPOLATION = cv2.INTER_LINEAR

# calibration = np.load(sys.path[0] + "\cam\calib.npz", allow_pickle=False)
# imageSize = tuple(calibration["imageSize"])
# leftMapX = calibration["leftMapX"]
# leftMapY = calibration["leftMapY"]
# leftROI = tuple(calibration["leftROI"])
# rightMapX = calibration["rightMapX"]
# rightMapY = calibration["rightMapY"]
# rightROI = tuple(calibration["rightROI"])

# LEFT_PATH = sys.path[0] + "\mleft.png"
# im = cv2.imread(LEFT_PATH.format(10))
# im = cv2.resize(im, (640, 480), interpolation = cv2.INTER_LINEAR)
# cv2.imshow('left', im)
# fixedLeft = cv2.remap(im, leftMapX, leftMapY, REMAP_INTERPOLATION)
# cv2.imshow('left_calib', fixedLeft)
# cv2.imwrite(sys.path[0] + "\cmleft.png", fixedLeft)

# RIGHT_PATH = sys.path[0] + "\mright.png"
# im = cv2.imread(RIGHT_PATH.format(10))
# im = cv2.resize(im, (640, 480), interpolation = cv2.INTER_LINEAR)
# cv2.imshow('right', im)
# fixedRight = cv2.remap(im, rightMapX, rightMapY, REMAP_INTERPOLATION)
# cv2.imshow('right_calib', fixedRight)
# cv2.imwrite(sys.path[0] + "\cmright.png", fixedRight)

# cv2.waitKey()

# cv2.destroyAllWindows()