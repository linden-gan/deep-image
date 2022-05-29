import numpy as np
import sys
from ctypes import *

from cutil import *

disp_nparry = np.load(sys.path[0] + "/../cam/res_disparity.npz", allow_pickle=False)["disparity"]
disparity = IMAGE()
disparity.w = 1200
disparity.h = 720
disparity.c = 1
disparity.data = disp_nparry.tolist()
compute_depth()
