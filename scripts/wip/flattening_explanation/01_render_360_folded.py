"""Used for rendering frames as png files."""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb
from matplotlib.colors import ListedColormap

FILENAME = "/home/faruk/gdrive/paper-350_micron/paper_figures/results-patch_flatten_explain/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_masked_4visual_zoomed.nii.gz"
OUTDIR = "/home/faruk/gdrive/paper-350_micron/paper_figures/results-patch_flatten_explain/folded_curvature"

# Data range
MIN, MAX = 0, 2.1
NR_FRAMES = 24
BACKGROUND = "black"
RESOLUTION = (1920, 1920)
CMAP = "gray"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
# Get data
nii = nb.load(FILENAME)
data = nii.get_fdata()

# Mirror data
data = data[::-1, :, :]

# Normalize to 0-255
data[data > MAX] = MAX
data = (data - MIN) / (MAX - MIN)
data[data < 0] = 0
data *= 255

# Colors
cmap_custom = np.ones((256, 4))
cmap_custom[:, 0] = np.linspace(0, 1, 256)
cmap_custom[:, 1] = np.linspace(0, 1, 256)
cmap_custom[:, 2] = np.linspace(0, 1, 256)
cmap_custom[-1, :] = [1, 0, 0, 1]
cmap_custom = ListedColormap(cmap_custom)

# Prep plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0
p.add_volume(data, cmap=cmap_custom, opacity=opacity, blending="composite",
             opacity_unit_distance=0, ambient=0, shade=True,
             specular=1, specular_power=128, resolution=[1.5, 1.5, 1.5],
             culling=True)
p.set_background(BACKGROUND)
p.remove_scalar_bar()

# -----------------------------------------------------------------------------
# Manipulate camera
p.camera.elevation -= 10
p.camera.zoom(1.3)
for i in range(NR_FRAMES):
    sys.stdout.write("  Frame {}/{} \r".format(i+1, NR_FRAMES))
    sys.stdout.flush()

    p.show(auto_close=False)

    out_name = "frame-{}.png".format(str(i).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))

    # Move camera
    p.camera.azimuth += 360 / NR_FRAMES
    p.camera.azimuth %= 360

print("\nFinished.")
