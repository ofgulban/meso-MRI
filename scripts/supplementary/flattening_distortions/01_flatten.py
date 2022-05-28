"""Generate halfway phase shifted ring."""

import os
import cv2
import numpy as np
from scipy import ndimage


OUTDIR = "/home/faruk/gdrive/paper-350_micron/paper_figures/revision-distortions"

DIMS = 900, 900

RADIUS_OUTER = 450
RADIUS_INNER = 150

SEGMENTS_INNER = 5  # Default 30, high res 5
NR_LAYERS = 121  # Default 21, high red 121

FLAT_DIMS = 320, 960

KAYCUBE_FACTOR = 32

# -----------------------------------------------------------------------------
# Compute circumference ratio of equal line segments
circum_ratio = (2 * np.pi * RADIUS_OUTER) / (2 * np.pi * RADIUS_INNER)
SEGMENTS_OUTER = int(SEGMENTS_INNER / circum_ratio)

circum_ratio2 = (2 * np.pi * ((RADIUS_OUTER+RADIUS_INNER)/2)) / (2 * np.pi * RADIUS_INNER)
SEGMENTS_MIDDLE = int((SEGMENTS_INNER + circum_ratio) // 2)

nr_segments_outer = 360 // SEGMENTS_OUTER
nr_segments_inner = 360 // SEGMENTS_INNER
nr_segments_middle = 360 // SEGMENTS_MIDDLE

rhos = np.linspace(RADIUS_INNER, RADIUS_OUTER, NR_LAYERS)

# =============================================================================
# Generate coordinates
# =============================================================================
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

# -----------------------------------------------------------------------------
# Create checkerboard pattern
data3 = np.zeros((DIMS[0], DIMS[1]+DIMS[1]*2//3))
for i in range(DIMS2[0]):
    for j in range(DIMS2[1]):
        x, y = i // KAYCUBE_FACTOR, j // KAYCUBE_FACTOR

        if (x % 2 == 0) and (y % 2 == 0):
            data3[i, j] = 50
        elif (x % 2 == 0) and (y % 2 != 0):
            data3[i, j] = 100
        elif (x % 2 != 0) and (y % 2 == 0):
            data3[i, j] = 150
        else:
            data3[i, j] = 250

data3[data2 == 0] = 0
cv2.imwrite(os.path.join(OUTDIR, "kaycubes.png"), data3)

# =============================================================================
# Ideal coordinates
# =============================================================================
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
# Deep surface mesh
# =============================================================================
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


# Part 1
points1 = np.zeros((NR_LAYERS, nr_segments_outer, 2))
phis = np.linspace(np.pi, 2*np.pi, nr_segments_outer)
for k, r in enumerate(rhos):
    for i, j in enumerate(phis):
        points1[k, i, :] = pol2cart(r, j)
    # Adjust point coordinates to array grid coordinates
    points1[k, :, :] += center

# Part 2
points2 = np.zeros((NR_LAYERS, nr_segments_inner, 2))
phis = np.linspace(0, np.pi, nr_segments_inner)
for k, r in enumerate(rhos):
    for i, j in enumerate(phis):
        points2[k, i, :] = pol2cart(r, j)
    # Adjust point coordinates to array grid coordinates
    points2[k, :, :] += center
    points2[k, :, 0] += RADIUS_OUTER + RADIUS_INNER

points_d = np.zeros((NR_LAYERS, nr_segments_outer + nr_segments_inner, 2))
points_d[:, :nr_segments_outer, :] = points1
points_d[:, nr_segments_outer:, :] = points2[::-1, ::-1, :]

# =============================================================================
# Superficial surface mesh
# =============================================================================
points1 = np.zeros((NR_LAYERS, nr_segments_inner, 2))

phis = np.linspace(np.pi, 2*np.pi, nr_segments_inner)
for k, r in enumerate(rhos):
    for i, j in enumerate(phis):
        points1[k, i, :] = pol2cart(r, j)
    # Adjust point coordinates to array grid coordinates
    points1[k, :, :] += center

# -----------------------------------------------------------------------------
points2 = np.zeros((NR_LAYERS, nr_segments_outer, 2))

phis = np.linspace(0, np.pi, nr_segments_outer)
for k, r in enumerate(rhos):
    for i, j in enumerate(phis):
        points2[k, i, :] = pol2cart(r, j)
    # Adjust point coordinates to array grid coordinates
    points2[k, :, :] += center
    points2[k, :, 0] += RADIUS_OUTER + RADIUS_INNER

points_s = np.zeros((NR_LAYERS, nr_segments_outer + nr_segments_inner, 2))
points_s[:, :nr_segments_inner, :] = points1
points_s[:, nr_segments_inner:, :] = points2[::-1, ::-1, :]

# =============================================================================
# Middle surface mesh
# =============================================================================
points_m = np.zeros((NR_LAYERS, nr_segments_middle*2, 2))

phis = np.linspace(-np.pi, np.pi, nr_segments_middle*2)
for k, r in enumerate(rhos):
    for i, j in enumerate(phis):
        points_m[k, i, :] = pol2cart(r, j)
    # Adjust point coordinates to array grid coordinates
    points_m[k, :, :] += center

points_m[:, nr_segments_middle:, 0] *= -1
points_m[:, nr_segments_middle:, 0] += RADIUS_OUTER*3 + RADIUS_INNER
points_m[:, nr_segments_middle:, :] = points_m[::-1, nr_segments_middle:, :]

# =============================================================================
# Flatten
# =============================================================================
# Ideal case (voxel-based)
flat_i = np.zeros(FLAT_DIMS)
r_min, r_max = ideal_radii[ideal_radii > 0].min(), ideal_radii.max()
for i in range(DIMS2[0]):
    for j in range(DIMS2[1]):
        if data2[i, j] > 0:
            x = (ideal_radii[i, j]-r_min) / (r_max-r_min) * (flat_i.shape[0]-1)
            y = ideal_angles[i, j] / (2*np.pi) * (flat_i.shape[1]-1)
            flat_i[int(x), int(y)] = data3[i, j]

cv2.imwrite(os.path.join(OUTDIR, "flat-0_ideal1.png"), flat_i)

# Quick fill in with median
img = ndimage.median_filter(flat_i, size=5)
flat_i[~(flat_i != 0)] = img[~(flat_i != 0)]
cv2.imwrite(os.path.join(OUTDIR, "flat-0_ideal2.png"), flat_i)

# (Optional) Emulate voxel based subsampling
flat_v = ndimage.zoom(flat_i, 1./(KAYCUBE_FACTOR/24), mode="reflect",
                      order=0, prefilter=False)
flat_v = ndimage.zoom(flat_v, KAYCUBE_FACTOR/4, mode="reflect",
                      order=0, prefilter=False)
cv2.imwrite(os.path.join(OUTDIR, "flat-4_voxel.png"), flat_v)

# -----------------------------------------------------------------------------
# Deep mesh
# -----------------------------------------------------------------------------
flat_d = np.zeros(FLAT_DIMS)
dims = flat_d.shape
r_min, r_max = ideal_radii[ideal_radii > 0].min(), ideal_radii.max()

nr_depths = points_d.shape[0]
nr_points = points_d.shape[1]
points_uv = np.zeros((nr_depths, nr_points, 2))
for d in range(nr_depths):
    for p in range(nr_points):
        j, i = points_d[d, p, :].astype("int")

        # Handle edge cases
        if i >= DIMS2[0]:
            i -= 1
        if j >= DIMS2[1]:
            j -= 1

        # Transform the point coordinates form folded to flat
        x = (ideal_radii[i, j]-r_min) / (r_max-r_min) * (flat_d.shape[0]-1)
        y = ideal_angles[i, j] / (2*np.pi) * (flat_d.shape[1]-1)

        # Adjust for flattening mesh geodesics
        g = circum_ratio + 1
        f = dims[1]//2
        if y < dims[1]//2:
            f = dims[1]//2
            z = int((y / f) * dims[1]/g*(g-1))
        else:
            f = dims[1]//2
            z = ((y - f) / f) * (dims[1]/g)
            z = int(z + dims[1]/g*(g-1))

        points_uv[d, p, :] = x, z  # Useful for filling in later
        flat_d[int(x), int(z)] = data3[i, j]

cv2.imwrite(os.path.join(OUTDIR, "flat-1_deep1.png"), flat_d)

# -----------------------------------------------------------------------------
# Fill-in
new = np.zeros(flat_d.shape)

for i in range(dims[0]):
    for j in range(dims[1]):
        # Access to point coordinates in folded
        a = np.copy(points_uv.reshape(nr_depths*nr_points, 2))
        b = np.copy(points_d.reshape(nr_depths*nr_points, 2))

        # Evaluate distances
        dists = (a[:, 0]-i)**2 + (a[:, 1]-j)**2  # skip sqrt
        idx = np.argmin(dists)
        y, x = b[idx, :]

        # Handle edge cases
        if x >= DIMS2[0]:
            x -= 1
        if y >= DIMS2[1]:
            y -= 1

        new[i, j] = data3[int(x), int(y)]

cv2.imwrite(os.path.join(OUTDIR, "flat-1_deep2.png"), new)

# -----------------------------------------------------------------------------
# Superficial mesh
# -----------------------------------------------------------------------------
flat_s = np.zeros(FLAT_DIMS)
r_min, r_max = ideal_radii[ideal_radii > 0].min(), ideal_radii.max()

nr_depths = points_s.shape[0]
nr_points = points_s.shape[1]
points_uv = np.zeros((nr_depths, nr_points, 2))
for d in range(nr_depths):
    for p in range(nr_points):
        j, i = points_s[d, p, :].astype("int")

        # Handle edge cases
        if i >= DIMS2[0]:
            i -= 1
        if j >= DIMS2[1]:
            j -= 1

        # Transform the point coordinates form folded to flat
        x = (ideal_radii[i, j]-r_min) / (r_max-r_min) * (flat_s.shape[0]-1)
        y = ideal_angles[i, j] / (2*np.pi) * (flat_s.shape[1]-1)

        # ---------------------------------------------------------------------
        # Adjust for flattening mesh geodesics
        g = circum_ratio + 1
        f = dims[1]//2
        if y < dims[1]//2:
            z = int((y / f) * (dims[1]/g))
        else:
            z = ((y - f) / f) * (dims[1]/g*(g-1))
            z = int(z + dims[1]/g)
        # ---------------------------------------------------------------------

        points_uv[d, p, :] = x, z  # Useful for filling in later
        flat_s[int(x), int(z)] = data3[i, j]

cv2.imwrite(os.path.join(OUTDIR, "flat-2_superficial1.png"), flat_s)

# -----------------------------------------------------------------------------
# Fill-in
for i in range(dims[0]):
    for j in range(dims[1]):
        # Access to point coordinates in folded
        a = np.copy(points_uv.reshape(nr_depths*nr_points, 2))
        b = np.copy(points_s.reshape(nr_depths*nr_points, 2))

        # Evaluate distances
        dists = (a[:, 0]-i)**2 + (a[:, 1]-j)**2  # skip sqrt
        idx = np.argmin(dists)
        y, x = b[idx, :]

        # Handle edge cases
        if x >= DIMS2[0]:
            x -= 1
        if y >= DIMS2[1]:
            y -= 1

        new[i, j] = data3[int(x), int(y)]

cv2.imwrite(os.path.join(OUTDIR, "flat-2_superficial2.png"), new)

# -----------------------------------------------------------------------------
# Middle mesh
# -----------------------------------------------------------------------------
flat_m = np.zeros(FLAT_DIMS)
r_min, r_max = ideal_radii[ideal_radii > 0].min(), ideal_radii.max()

nr_depths = points_m.shape[0]
nr_points = points_m.shape[1]
points_uv = np.zeros((nr_depths, nr_points, 2))
for d in range(nr_depths):
    for p in range(nr_points):
        j, i = points_m[d, p, :].astype("int")

        # Handle edge cases
        if i >= DIMS2[0]:
            i -= 1
        if j >= DIMS2[1]:
            j -= 1

        # Transform the point coordinates form folded to flat
        x = (ideal_radii[i, j]-r_min) / (r_max-r_min) * (flat_m.shape[0]-1)
        y = ideal_angles[i, j] / (2*np.pi) * (flat_m.shape[1]-1)

        points_uv[d, p, :] = x, y  # Useful for filling in later
        flat_m[int(x), int(y)] = data3[i, j]

cv2.imwrite(os.path.join(OUTDIR, "flat-3_middle1.png"), flat_m)

# -----------------------------------------------------------------------------
# Fill-in
for i in range(dims[0]):
    for j in range(dims[1]):
        # Access to point coordinates in folded
        a = np.copy(points_uv.reshape(nr_depths*nr_points, 2))
        b = np.copy(points_m.reshape(nr_depths*nr_points, 2))

        # Evaluate distances
        dists = (a[:, 0]-i)**2 + (a[:, 1]-j)**2  # skip sqrt
        idx = np.argmin(dists)
        y, x = b[idx, :]

        # Handle edge cases
        if x >= DIMS2[0]:
            x -= 1
        if y >= DIMS2[1]:
            y -= 1

        new[i, j] = data3[int(x), int(y)]

cv2.imwrite(os.path.join(OUTDIR, "flat-3_middle2.png"), new)

print("Finished.")
