"""Test Pyvista camera parameters."""

import os
import numpy as np
import pyvista as pv
import nibabel as nb

FILE = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/flattening/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi.nii.gz"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/movies/test_frames"

MIN, MAX = 20, 45
BACKGROUND = "black"
RESOLUTION = (720, 720)
CMAP = "gray"
# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

nii = nb.load(FILE)
dims = nii.shape
data = nii.get_fdata()

# Normalize
data[data > MAX] = MAX
data -= MIN
data /= MAX - MIN
data[data < 0] = 0
data *= 255

# Prep pyvista plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0
p.add_volume(data, cmap="gray", opacity=opacity)
p.set_background(BACKGROUND)

# p.camera.roll = 0
p.camera_position = 'yz'
p.camera.elevation = 15

print("Roll        : {}".format(p.camera.roll))
print("Elevation   : {}".format(p.camera.elevation))
print("Azimuth     : {}".format(p.camera.azimuth))
print("Position    : {}".format(p.camera.position))
print("Focal point : {}".format(p.camera.focal_point))
print("Clip range  : {}".format(p.camera.clipping_range))

CAMPOS_DEFAULT = p.camera_position

# Manipulate camera
# -----------------------------------------------------------------------------
p.camera_position = CAMPOS_DEFAULT
p.camera.elevation += 30
for i in range(90):
    p.show(auto_close=False)
    out_name = "03_azimuth-{}.png".format(str(i).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))
    p.camera.azimuth += 4
    p.camera.azimuth %= 360

print("Finished.")
