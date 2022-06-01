#ifndef IMAGE_H
#define IMAGE_H

// an image
// slice each row of an image out and put them one by one to data array
typedef struct{
    int w,h,c;
    float *data;
} image;

// A 2d point.
// float x, y: the coordinates of the point.
typedef struct{
    float x, y;
} point;

// input: a disparity map, focal length, and two cameras' displacement
// output: a depth map with 2 channels, one for vertical depth z,
// the other for euclidean distance.
image compute_depth(image disparity, float f, float d);

image make_image(int w, int h, int c);

#endif IMAGE_H