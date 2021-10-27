"""Used for rendering frames as png files."""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb

FILENAME = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/cakeplots/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi_curv_icing.nii.gz"
OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/cakeplots/01_cakeplot_360"

# Data range
MIN, MAX = 20, 45
NR_FRAMES = 24 * 8
BACKGROUND = "black"
RESOLUTION = (720, 720)
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

# Prep plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0
p.add_volume(data, cmap="gray", opacity=opacity, blending="composite",
             opacity_unit_distance=0)
p.set_background(BACKGROUND)
p.remove_scalar_bar()
p.add_text("Cakeplot", font="courier")

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

print("Finished.")
