#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "image.h"

// input: a disparity map, focal length, and two cameras' displacement
// output: a depth map with 2 channels, one for vertical depth z,
// the other for euclidean distance.
image compute_depth(image disparity, double f, double d) {
    image res;
    res.h = disparity.h;
    res.w = disparity.w;
    res.c = 2;
    // the coordinate of the center pixel on the image
    float cen_x = disparity.w / 2.0;
    float cen_y = disparity.h / 2.0;
    for (int y = 0; y < disparity.h; y++) {
        for (int x = 0; x < disparity.w; x++) {
            double shift = disparity.data[y * disparity.w + x];
            // TODO: possible conversion of unit of pixel shift (pixel -> millimeter)
            double vertical_depth = f * d / shift;
            res.data[y * disparity.w + x] = vertical_depth;

            // euclidean distance
            // first, we need to calculate the distance from focal point
            // to the pixel on image by Gougu Theorem
            double x_dis = x - cen_x;
            double y_dis = y - cen_y;
            // TODO: possible conversion of unit of pixel shift (pixel -> millimeter)
            double pix_dis = sqrt(x_dis * x_dis + y_dis * y_dis);
            // second, we need to scale the pixel distance by a proportion,
            // so that we can get the real distance.
            double real_dis = pix_dis * vertical_depth / f;
            // store this real euclidean distance to the second channel
            res.data[res.w * res.h + y * disparity.w + x] = real_dis;
        }
    }
    return res;
}
