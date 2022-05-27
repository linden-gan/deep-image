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

#endif IMAGE_H