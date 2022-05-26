"""Generate halfway phase shifted ring."""

import os
import cv2
import numpy as np

OUT = "/home/faruk/gdrive/paper-350_micron/paper_figures/revision-distortions/test.png"

DIMS = 900, 900

# =============================================================================
# Generate coordinates
coords = np.zeros((DIMS[0], DIMS[1], 2))
center = DIMS[0]/2, DIMS[1]/2
for i in range(DIMS[0]):
    for j in range(DIMS[1]):
        coords[i, j, 0] = i
        coords[i, j, 1] = j

coords[:, :, 0] -= center[0]
coords[:, :, 1] -= center[1]

# -----------------------------------------------------------------------------
# Generate ring
mag = np.linalg.norm(coords, axis=-1)
data = np.zeros(DIMS)
data[mag < 450] = 200
data[mag < 150] = 0

# Extend horizontally
DIMS2 = DIMS[0], DIMS[1]+DIMS[1]*2//3
data2 = np.zeros((DIMS2[0], DIMS2[1]))
data2[0:DIMS[0]//2, 0:DIMS[1]] = data[0:DIMS[0]//2, :]
data2[DIMS[0]//2:, DIMS[1]*2//3:] = data[DIMS[0]//2:, :]

# -----------------------------------------------------------------------------
# Create checkerboard pattern
data3 = np.zeros((DIMS[0], DIMS[1]+DIMS[1]*2//3))
FACTOR = 32
for i in range(DIMS2[0]):
    for j in range(DIMS2[1]):
        x, y = i // FACTOR, j // FACTOR

        if (x % 2 == 0) and (y % 2 == 0):
            data3[i, j] = 50
        elif (x % 2 == 0) and (y % 2 != 0):
            data3[i, j] = 100
        elif (x % 2 != 0) and (y % 2 == 0):
            data3[i, j] = 150
        else:
            data3[i, j] = 250

data3[data2 == 0] = 0
# cv2.imwrite(OUT, data3)

# -----------------------------------------------------------------------------
# Ideal flattening
a = np.arctan2(coords[..., 0], coords[..., 1]) + np.pi
angles = np.rad2deg(a)
angles = (angles // 30) * 30 * (255/360)

data4 = np.zeros((DIMS2[0], DIMS2[1]))
data4[0:DIMS[0]//2, 0:DIMS[1]] = angles[0:DIMS[0]//2:, :]
data4[DIMS[0]//2:, DIMS[1]*2//3:] = angles[DIMS[0]//2:, ::-1]


cv2.imwrite(OUT, data4)

# -----------------------------------------------------------------------------
# # Sample points along border Circumference = 2*pi*r
# circum = 2 * np.pi * 450
# circum = 2 * np.pi * 150
