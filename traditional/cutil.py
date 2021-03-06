import  os
from ctypes import *

# Change to the following line if you are on linux 
# You can generate the .so file by gcc -o util_linux.so -shared -fPIC -O2 util.c
# lib = CDLL(os.path.join(os.path.dirname(__file__), "util_linux.so"), RTLD_GLOBAL)
lib = CDLL(os.path.join(os.path.dirname(__file__), "util_win32.so"), RTLD_GLOBAL)

# objects
class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class POINT(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float)]


# functions
compute_depth_lib = lib.compute_depth
compute_depth_lib.argtypes = [IMAGE, c_float, c_float]
compute_depth_lib.restype = IMAGE

def make_image(w, h, c, data=None):
    im = IMAGE()
    im.w = w
    im.h = h
    im.c = c
    im.data = data
    return im

def compute_depth(disparity_raw, f, d, x, y):
    disparity_raw = disparity_raw.reshape((1, 307200)).tolist()[0]
    carr = (c_float * len(disparity_raw))(*disparity_raw)
    disparity = make_image(640, 480, 1, carr)
    deep_image = compute_depth_helper(disparity, f, d)
    return deep_image.data[x + y * 640]

def compute_depth_helper(disparity, f, d):
    return compute_depth_lib(disparity, f, d)

