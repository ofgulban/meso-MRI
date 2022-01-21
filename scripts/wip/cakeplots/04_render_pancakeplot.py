"""Used for rendering frames as png files."""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb

FILENAME = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/flattening/sub-04_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi.nii.gz"
OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/animations/pancakeplot_sub-04"

# Data range
MIN, MAX = 20, 60
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
data = np.asarray(nii.dataobj)

# Cleanup sides
idx = data[:, :, data.shape[2]//2] != 0
data[~idx, :] = 0

# Mirror data
data = data[::-1, :, :]

# Shave off bottom and top slices (gives weird render bug)
data[:, :, 0] = 0
data[:, :, -1] = 0

# Normalize to 0-255
idx0 = data == 0
data[data > MAX] = MAX
data = (data - MIN) / (MAX - MIN)
data *= 255
data[data < 0] = 1
data[idx0] = 0

# Prep plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0

p.set_background(BACKGROUND)
p.add_text("Pancakeplot", font="courier")

# -----------------------------------------------------------------------------
# # (Optional) Test render
# p.add_volume(data, cmap="gray", opacity=opacity, blending="composite",
#              opacity_unit_distance=0, ambient=0, shade=True,
#              specular=1, specular_power=128)
# p.set_background(BACKGROUND)
# p.show(auto_close=False)

# -----------------------------------------------------------------------------
# Manipulate camera
# p.camera.elevation += 10
# p.camera.zoom(1.3)

NR_FRAMES = data.shape[2]
frame = 0
for i in range(NR_FRAMES):
    sys.stdout.write("  Frame {}/{} \r".format(frame, NR_FRAMES))
    sys.stdout.flush()

    temp = np.copy(data)
    temp[:, :, i:] = 0

    actor = p.add_volume(temp, cmap="gray", opacity=opacity,
                         blending="composite", opacity_unit_distance=0,
                         ambient=0, shade=True,
                         specular=1, specular_power=128)
    p.remove_scalar_bar()
    p.show(auto_close=False)

    out_name = "frame-{}.png".format(str(frame).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))
    p.remove_actor(actor)
    frame += 1

# backwards
for i in range(NR_FRAMES, 0, -1):
    sys.stdout.write("  Frame {}/{} \r".format(frame, NR_FRAMES*2))
    sys.stdout.flush()

    temp = np.copy(data)
    temp[:, :, i:] = 0

    actor = p.add_volume(temp, cmap="gray", opacity=opacity,
                         blending="composite", opacity_unit_distance=0,
                         ambient=0, shade=True,
                         specular=1, specular_power=128)
    p.remove_scalar_bar()
    p.show(auto_close=False)

    out_name = "frame-{}.png".format(str(frame).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))
    p.remove_actor(actor)
    frame += 1

print("Finished.")
