"""Used for rendering frames as png files."""

import os
import numpy as np
import pyvista as pv
import nibabel as nb

FILENAME = "/home/faruk/data2/DATA_MRI_NIFTI/derived/movies/test_cakeplot/test-cakeplot.nii.gz"
OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/movies/scene-02"

# Data range
MIN, MAX = 20, 45
NR_FRAMES = 48
BACKGROUND = "black"
RESOLUTION = (720, 720)
CMAP = "gray"

# =============================================================================
# Get data
nii = nb.load(FILENAME)
data = nii.get_fdata()

# Normalize
data[data > MAX] = MAX
data -= MIN
data /= MAX - MIN
data[data < 0] = 0
data *= 255

# Prep plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0
p.add_volume(data, cmap="gray", opacity=opacity)
p.set_background(BACKGROUND)
p.remove_scalar_bar()
p.add_text("Cakeplot", font="courier", font_size=18)

# -----------------------------------------------------------------------------
# Manipulate camera
# -----------------------------------------------------------------------------
for i in range(NR_FRAMES):
    p.show(auto_close=False)

    out_name = "03_azimuth-{}.png".format(str(i).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))

    # Move camera
    p.camera.azimuth += 360 / NR_FRAMES
    p.camera.azimuth %= 360

print("Finished.")
