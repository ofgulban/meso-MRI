"""Generate halfway phase shifted ring."""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "/home/faruk/gdrive/paper-350_micron/paper_figures/revision-distortions"

DIMS = 900, 900

RADIUS_OUTER = 450
RADIUS_INNER = 150

NR_LAYERS = 7

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

# -----------------------------------------------------------------------------
# Compute circumference ratio of equal line segments
circum_ratio = (2 * np.pi * RADIUS_OUTER) / (2 * np.pi * RADIUS_INNER)
SEGMENTS_INNER = 30
SEGMENTS_OUTER = int(SEGMENTS_INNER / circum_ratio)

circum_ratio2 = (2 * np.pi * ((RADIUS_OUTER+RADIUS_INNER)/2)) / (2 * np.pi * RADIUS_INNER)
SEGMENTS_MIDDLE = int((SEGMENTS_INNER + circum_ratio) // 2)

nr_segments_outer = 360 // SEGMENTS_OUTER
nr_segments_inner = 360 // SEGMENTS_INNER
nr_segments_middle = 360 // SEGMENTS_MIDDLE

rhos = np.linspace(RADIUS_INNER, RADIUS_OUTER, NR_LAYERS)


# =============================================================================
# Generate points
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


# =============================================================================
# Deep surface mesh
# =============================================================================
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
plt.style.use('dark_background')

DPI = 192
fig = plt.figure(figsize=(1920/DPI, 1080/DPI), dpi=DPI)

plt.imshow(data2, cmap="gray", origin="lower")
for i in range(NR_LAYERS):
    if i == NR_LAYERS-1:
        plt.plot(points_d[i, :, 0], points_d[i, :, 1], marker="o",
                 markersize=5,
                 color=[1, 0, 0])
    else:
        plt.plot(points_d[i, :, 0], points_d[i, :, 1], marker="o",
                 markersize=5, color=[0.5, 0.5, 0.5])

plt.xlim([0, DIMS2[1]])
plt.ylim([0, DIMS2[0]])
plt.axis('off')
plt.savefig(os.path.join(OUTDIR, "1_deep_mesh.png"), bbox_inches='tight')

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
fig = plt.figure(figsize=(1920/DPI, 1080/DPI), dpi=DPI)

plt.imshow(data2, cmap="gray", origin="lower")
for i in range(NR_LAYERS):
    if i == 0:
        plt.plot(points_s[i, :, 0], points_s[i, :, 1], marker="o",
                 markersize=5, color=[0, 0.5, 1])
    else:
        plt.plot(points_s[i, :, 0], points_s[i, :, 1], marker="o",
                 markersize=5, color=[0.5, 0.5, 0.5])

plt.xlim([0, DIMS2[1]])
plt.ylim([0, DIMS2[0]])
plt.axis('off')
plt.savefig(os.path.join(OUTDIR, "2_sup_mesh.png"), bbox_inches='tight')

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

# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(1920/DPI, 1080/DPI), dpi=DPI)
plt.imshow(data2, cmap="gray", origin="lower")
for i in range(NR_LAYERS):
    if i == NR_LAYERS//2:
        plt.plot(points_m[i, :, 0], points_m[i, :, 1], marker="o",
                 markersize=5, color=[0, 1, 0])
    else:
        plt.plot(points_m[i, :, 0], points_m[i, :, 1], marker="o",
                 markersize=5, color=[0.5, 0.5, 0.5])

plt.xlim([0, DIMS2[1]])
plt.ylim([0, DIMS2[0]])
plt.axis('off')
plt.savefig(os.path.join(OUTDIR, "3_middle_mesh.png"), bbox_inches='tight')

print("Finished.")
