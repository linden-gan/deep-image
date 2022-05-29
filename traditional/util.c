#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "util.h"

// input: a disparity map, focal length, and two cameras' displacement
// output: a depth map with 2 channels, one for vertical depth z,
// the other for euclidean distance.
image compute_depth(image disparity, float f, float d) {
    int w = disparity.w;
    int h = disparity.h;
    image res = make_image(w, h, 2);
    // the coordinate of the center pixel on the image
    float cen_x = w / 2.0;
    float cen_y = h / 2.0;
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            float shift = disparity.data[y * w + x];
            // TODO: possible conversion of unit of pixel shift (pixel -> millimeter)
            float vertical_depth = f * d / shift;
            // printf("depth is %f", vertical_depth);
            res.data[y * w + x] = vertical_depth;

            // euclidean distance
            // first, we need to calculate the distance from focal point
            // to the pixel on image by Gougu Theorem
            float x_dis = x - cen_x;
            float y_dis = y - cen_y;
            // TODO: possible conversion of unit of pixel shift (pixel -> millimeter)
            float xy_dis = sqrt(x_dis * x_dis + y_dis * y_dis);
            float pix_dis = sqrt(xy_dis * xy_dis + f * f);
            // second, we need to scale the pixel distance by a proportion,
            // so that we can get the real distance.
            float real_dis = pix_dis * vertical_depth / f;
            // store this real euclidean distance to the second channel
            res.data[w * h + y * w + x] = real_dis;
        }
    }
    return res;
}

image make_image(int w, int h, int c) {
    image im;
    im.w = w;
    im.h = h;
    im.c = c;
    im.data = calloc(im.h * im.w * im.c, sizeof(float));
    return im;
}
