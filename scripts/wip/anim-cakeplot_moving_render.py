"""Used in thingsonthings.org LN2_MULTILATERATE blog post."""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb

# Scalar file (e.g. activtion map or anatomical image)
FILE1 = "/home/faruk/data2/DATA_MRI_NIFTI/derived/movies/test_cakeplot/test-cakeplot_moving.nii.gz"
OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/movies/test_cakeplot/frames"

MIN, MAX = 20, 45
BACKGROUND = "black"
RESOLUTION = (720, 720)
CMAP = "gray"

# -----------------------------------------------------------------------------
# Load data
data = nb.load(FILE1).get_fdata()
nr_frames = data.shape[-1]

frame_order = np.arange(nr_frames)
frame_order = np.hstack([frame_order, frame_order[::-1]])

# -----------------------------------------------------------------------------
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0

# Adjust elevation
for i, j in enumerate(frame_order):
    sys.stdout.write("  Frame {}/{} \r".format(i+1, frame_order.size))
    sys.stdout.flush()

    # Get data and clip it
    temp = np.copy(data[..., j])
    # Normalize, because CLIM does not seem to work while rendering
    temp[temp > MAX] = MAX
    temp -= MIN
    temp /= MAX - MIN
    temp[temp < 0] = 0
    temp *= 255

    # Render
    p.add_volume(temp, cmap=CMAP, opacity=opacity)
    p.remove_scalar_bar()
    p.set_background(BACKGROUND)
    p.add_text("Cakeplot", font="courier", font_size=18)

    out_name = "frame-{}.png".format(str(i).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))
    p.clear()

p.close()

print("Finished.")