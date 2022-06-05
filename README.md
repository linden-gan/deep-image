# Deep image
Extract depth information from a pair of stereo images. \
Our final product is an executable that could calculate and display depth information at clicked position using two webcams in realtime.

## Problem Setup
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

#### Challenges we ran into


### Neural Network (utilized [MobileStereoNet](https://github.com/cogsys-tuebingen/mobilestereonet))

#### The experiment

#### Challenges we ran into

## What we've learned & other thoughts

## Citation & Credits

