"""Used for rendering frames as png files."""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb

FILENAME = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-demo_flatten/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi_median_boxv3_5-5-11.nii.gz"
OUTDIR = "/home/faruk/gdrive/paper-350_micron/paper_figures/results-patch_flatten_explain/flat_curvature"

# Mask to smooth cake sides
MASK = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/median_maps/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi_median_projection.nii.gz"

# Data range
MIN, MAX = 0, 2
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

# Smooth sides
mask = np.squeeze(nb.load(MASK).get_fdata())
idx = mask != 0
data[~(idx), :] = 0

# Mirror data
# data = data[::-1, :, :]

# Fix top layer not being rendered
data[:, :, -1] = 0

# Normalize to 0-255
data[data > MAX] = MAX
data = (data - MIN) / (MAX - MIN)
data[data < 0] = 0
data *= 255

# Prep plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0
p.add_volume(data, cmap=CMAP, opacity=opacity, blending="composite",
             opacity_unit_distance=0, ambient=0, shade=True,
             specular=0, specular_power=0)
p.set_background(BACKGROUND)
p.remove_scalar_bar()

# -----------------------------------------------------------------------------
# Manipulate camera
p.camera.elevation += 10
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
