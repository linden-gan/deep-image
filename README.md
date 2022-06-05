# Deep image
Extract depth information from a pair of stereo images. \
Our final product is an executable that could calculate and display depth information at clicked position using two webcams in realtime.

## Problem Setup
Depth informaton are sometime useful. We want our images tell us how far an object is instead of just some flat 2D information. This can be crucial in auto-drive, 3D environment reconstruction, and distance measurement.
We explored both the traditional (stereo box match, graph cut) and neural network solutions for calculating disparity maps, and finally choose traditional stereo box match to achieve realtime depth estimation from two webcams.

## Data used
- Photos taken by ourselves
- Kitti stereo dataset
- Middlebury stereo dataset

## Technologies & techniques used
### Traditional (based on opencv, stereo box match)
#### Prereq
- numpy (`pip install numpy`)
- opencv (cv2) (`pip install opencv-python`)
- matplotlib (`pip install matplotlib`)
- gcc compiler (already installed in Linux and Mac, please download MinGW for gcc [here](https://www.mingw-w64.org/))
- hardwares (two cameras, recommended to use two exactly same webcams so that they can be easily connected to computers and produce same-size images)

#### Pipeline & Algorithm
- First, we caliberate our webcams to get rid of distorted margin. Next, we input two stereo images to OpenCV's library function to get a disparity map, which represents shifts of each pair of pixels from left and right images. Then, we compute the depth of each pixel based on its shift. Finally, we output the depth information so that user can know each pixel's depth once they click it.
- 

#### Challenges we ran into


### Neural Network (utilized [MobileStereoNet](https://github.com/cogsys-tuebingen/mobilestereonet))

#### The experiment

#### Challenges we ran into

## What we've learned & other thoughts

## Citation & Credits

