"""Generate halfway phase shifted ring."""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "/home/faruk/gdrive/paper-350_micron/paper_figures/revision-distortions"

DIMS = 900, 900

RADIUS_OUTER = 450
RADIUS_INNER = 150

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
data[mag < RADIUS_OUTER] = 200
data[mag < RADIUS_INNER] = 0

# Extend horizontally
DIMS2 = DIMS[0], DIMS[1]+DIMS[1]*2//3
data2 = np.zeros((DIMS2[0], DIMS2[1]))
data2[0:DIMS[0]//2, 0:DIMS[1]] = data[0:DIMS[0]//2, :]
data2[DIMS[0]//2:, DIMS[1]*2//3:] = data[DIMS[0]//2:, :]

cv2.imwrite(os.path.join(OUTDIR, "step1.png"), data2)

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
cv2.imwrite(os.path.join(OUTDIR, "step2.png"), data3)

# -----------------------------------------------------------------------------
# Compute circumference ratio of equal line segments
circum_ratio = (2 * np.pi * RADIUS_OUTER) / (2 * np.pi * RADIUS_INNER)
SEGMENTS_INNER = 30
SEGMENTS_OUTER = int(SEGMENTS_INNER / circum_ratio)

# Inner angular segments
angles = np.arctan2(coords[..., 0], coords[..., 1]) + np.pi
angles = np.rad2deg(angles)
angles = (angles // SEGMENTS_INNER) * SEGMENTS_INNER * (255/360)

data4 = np.zeros((DIMS2[0], DIMS2[1]))
data4[0:DIMS[0]//2, 0:DIMS[1]] = angles[0:DIMS[0]//2:, :]
data4[DIMS[0]//2:, DIMS[1]*2//3:] = angles[DIMS[0]//2:, ::-1]

data4[data2 == 0] = 0
cv2.imwrite(os.path.join(OUTDIR, "step3.png"), data4)

# Outer angular segments
angles = np.arctan2(coords[..., 0], coords[..., 1]) + np.pi
angles = np.rad2deg(angles)
angles = (angles // SEGMENTS_OUTER) * SEGMENTS_OUTER * (255/360)

data5 = np.zeros((DIMS2[0], DIMS2[1]))
data5[0:DIMS[0]//2, 0:DIMS[1]] = angles[0:DIMS[0]//2:, :]
data5[DIMS[0]//2:, DIMS[1]*2//3:] = angles[DIMS[0]//2:, ::-1]

data5[data2 == 0] = 0
cv2.imwrite(os.path.join(OUTDIR, "step4.png"), data5)

data6 = np.copy(data4)
data6[0:DIMS[0]//2, 0:DIMS[1]] = data5[0:DIMS[0]//2, 0:DIMS[1]]
cv2.imwrite(os.path.join(OUTDIR, "step5.png"), data6)

data7 = np.copy(data5)
data7[0:DIMS[0]//2, 0:DIMS[1]] = data4[0:DIMS[0]//2, 0:DIMS[1]]
cv2.imwrite(os.path.join(OUTDIR, "step6.png"), data7)

# =============================================================================
# Ideal coordinates
angles = np.arctan2(coords[..., 0], coords[..., 1]) + np.pi
ideal_angles = np.zeros((DIMS2[0], DIMS2[1]))
ideal_angles[0:DIMS[0]//2, 0:DIMS[1]] = angles[0:DIMS[0]//2:, :]
ideal_angles[DIMS[0]//2:, DIMS[1]*2//3:] = angles[DIMS[0]//2:, ::-1]

ideal_angles[data2 == 0] = 0
img = ideal_angles / (2*np.pi) * 255
cv2.imwrite(os.path.join(OUTDIR, "ideal_angles.png"), img)

radii = np.linalg.norm(coords, axis=-1)
ideal_radii = np.zeros((DIMS2[0], DIMS2[1]))
ideal_radii[0:DIMS[0]//2, 0:DIMS[1]] = radii[0:DIMS[0]//2:, :]
ideal_radii[DIMS[0]//2:, DIMS[1]*2//3:] = np.abs(radii[DIMS[0]//2:, ::-1] -
                                                 (RADIUS_OUTER + RADIUS_INNER))

ideal_radii[data2 == 0] = 0

img = ideal_radii / ideal_radii.max() * 255
cv2.imwrite(os.path.join(OUTDIR, "ideal_radii.png"), img)

# =============================================================================
# Flatten
flat = np.zeros((400, 1200))
r_min, r_max = ideal_radii[ideal_radii > 0].min(), ideal_radii.max()
for i in range(DIMS2[0]):
    for j in range(DIMS2[1]):
        if data2[i, j] > 0:
            x = (ideal_radii[i, j]-r_min) / (r_max-r_min) * (flat.shape[0]-1)
            y = ideal_angles[i, j] / (2*np.pi) * (flat.shape[1]-1)
            flat[int(x), int(y)] = data3[i, j]

cv2.imwrite(os.path.join(OUTDIR, "ideal_flat.png"), flat)

# =============================================================================
# Generate points
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

NR_LAYERS = 11
rhos = np.linspace(RADIUS_INNER, RADIUS_OUTER, NR_LAYERS)

nr_segments_outer = 360 // SEGMENTS_OUTER
nr_segments_inner = 360 // SEGMENTS_INNER
# -----------------------------------------------------------------------------
phis = np.linspace(np.pi, 2*np.pi, nr_segments_outer)
POINTS1 = []
for r in rhos:
    points = np.zeros((nr_segments_outer, 2))
    for i, j in enumerate(phis):
        points[i, :] = pol2cart(r, j)
    # Adjust point coordinates to array grid coordinates
    points += center
    POINTS1.append(points)

# -----------------------------------------------------------------------------
phis = np.linspace(0, np.pi, nr_segments_inner)
POINTS2 = []
for r in rhos:
    points = np.zeros((nr_segments_inner, 2))
    for i, j in enumerate(phis):
        points[i, :] = pol2cart(r, j)
    # Adjust point coordinates to array grid coordinates
    points += center
    points[:, 0] += RADIUS_OUTER + RADIUS_INNER
    POINTS2.append(points)

# =============================================================================
DPI = 96
fig = plt.figure(figsize=(1000/DPI, 1000/DPI), dpi=DPI)

plt.imshow(data2, cmap="gray", origin="lower")
for i in range(NR_LAYERS):
    plt.plot(POINTS1[i][:, 0], POINTS1[i][:, 1], marker="o", markersize=5)
    plt.plot(POINTS2[i][:, 0], POINTS2[i][:, 1], marker="o", markersize=5)

plt.xlim([0, DIMS2[1]])
plt.ylim([0, DIMS2[0]])
plt.show()

print("Finished.")
