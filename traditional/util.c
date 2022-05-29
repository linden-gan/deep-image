#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "image.h"
#include "stb_image.h"
#include "stb_image_write.h"

// input: a disparity map, focal length, and two cameras' displacement
// output: a depth map with 2 channels, one for vertical depth z,
// the other for euclidean distance.
image compute_depth(image disparity, float f, float d) {
    image res;
    res.h = disparity.h;
    res.w = disparity.w;
    res.c = 2;
    res.data = calloc(res.h * res.w * res.c, sizeof(float));
    // the coordinate of the center pixel on the image
    float cen_x = disparity.w / 2.0;
    float cen_y = disparity.h / 2.0;
    for (int y = 0; y < disparity.h; y++) {
        for (int x = 0; x < disparity.w; x++) {
            double shift = disparity.data[y * disparity.w + x];
            // TODO: possible conversion of unit of pixel shift (pixel -> millimeter)
            double vertical_depth = f * d / shift;
            // printf("depth is %f", vertical_depth);
            res.data[y * disparity.w + x] = vertical_depth;

            // euclidean distance
            // first, we need to calculate the distance from focal point
            // to the pixel on image by Gougu Theorem
            double x_dis = x - cen_x;
            double y_dis = y - cen_y;
            // TODO: possible conversion of unit of pixel shift (pixel -> millimeter)
            double xy_dis = sqrt(x_dis * x_dis + y_dis * y_dis);
            double pix_dis = sqrt(xy_dis * xy_dis + f * f);
            // second, we need to scale the pixel distance by a proportion,
            // so that we can get the real distance.
            double real_dis = pix_dis * vertical_depth / f;
            // store this real euclidean distance to the second channel
            res.data[res.w * res.h + y * disparity.w + x] = real_dis;
        }
    }
    return res;
}

image load_image(char *filename, int channels)
{
    // int w, h, c;
    // unsigned char *data = stbi_load(filename, &w, &h, &c, channels);
    // if (!data) {
    //     fprintf(stderr, "Cannot load image \"%s\"\nSTB Reason: %s\n",
    //         filename, stbi_failure_reason());
    //     exit(0);
    // }
    // if (channels) {
    //     c = channels;
    // }
    // int i,j,k;
    image im;
    // im.w = w;
    // im.h = h;
    // im.c = c;
    // for(k = 0; k < c; ++k){
    //     for(j = 0; j < h; ++j){
    //         for(i = 0; i < w; ++i){
    //             int dst_index = i + w*j + w*h*k;
    //             int src_index = k + c*i + c*w*j;
    //             im.data[dst_index] = (float)data[src_index];
    //         }
    //     }
    // }
    // //We don't like alpha channels, #YOLO
    // if(im.c == 4) im.c = 3;
    // free(data);
    return im;
}
