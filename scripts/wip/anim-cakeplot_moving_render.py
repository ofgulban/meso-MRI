"""Used in thingsonthings.org LN2_MULTILATERATE blog post."""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb

# Scalar file (e.g. activtion map or anatomical image)
FILE1 = "/home/faruk/data2/ISMRM-2022/anim-slice_slide/anim_prep/scene-invivo_shot-1.nii.gz"
OUTDIR = "/home/faruk/data2/ISMRM-2022/anim-slice_slide/anim_frames/scene-invivo_shot-1"

MIN, MAX = 20, 45
BACKGROUND = "black"
RESOLUTION = (720, 720)
CMAP = "gray"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# -----------------------------------------------------------------------------
# Load data
data = nb.load(FILE1).get_fdata()
nr_frames = data.shape[-1]

# Establish frame ordering
frame_order = np.arange(nr_frames)
# Freeze animation
frame_order = np.hstack([frame_order, np.repeat(frame_order[-1], 6)])
# Reverse animation
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

print("\nFinished.")
