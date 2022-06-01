import numpy as np
import sys

dis = np.load(sys.path[0] + "\cam\\res_disparity.jpg.npz", allow_pickle=False)
print(dis["disparity"].shape)

for i in range(720):
    for j in range(1200):
        if (i + j) % 13 == 0:
            print(dis["disparity"][i][j])
