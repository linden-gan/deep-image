import sys, os
from ctypes import *
import math
import random

lib = CDLL(os.path.join(os.path.dirname(__file__), "util_linux.so"), RTLD_GLOBAL)

# objects
class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]
    def __add__(self, other):
        return add_image(self, other)
    def __sub__(self, other):
        return sub_image(self, other)


class POINT(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float)]


# functions
compute_depth = lib.compute_depth
compute_depth.argtypes = [IMAGE, c_float]
compute_depth.restype = IMAGE

def compute_depth(disparity, f):
    return compute_depth(disparity, f)

