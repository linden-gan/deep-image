import numpy as np
import sys

dis = np.load(sys.path[0] + "\cam\\res_disparity.npz", allow_pickle=False)
print(dis["disparity"].shape)

for i in range(300, 400):
    for j in range(600, 700):
        print(dis["disparity"][i][j])
