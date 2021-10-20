"""Trilaterate positions."""

import os
import numpy as np
import nibabel as nb
import compoda.core as cp

DATA = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz"
COORDS = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/HG_LH/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_HG_LH_UV_coordinates.nii.gz"
MASK = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/HG_LH/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_HG_LH_perimeter_chunk.nii.gz"
DEPTH = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/HG_LH/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_HG_LH_metric_equivol.nii.gz"

OUT_NAME = "test"

XY_BINS = 20  # Determines flat image resolution
Z_LAYERS = 5  # Determine flat image layers

# =============================================================================
# Mask out voxels
mask = nb.load(MASK)
mask = np.asarray(mask.dataobj)
idx = mask != 0

# Measurement
nii0 = nb.load(DATA)
data = np.asarray(nii0.dataobj)[idx]

# Coordinates
nii1 = nb.load(COORDS)
coord_uv = np.asarray(nii1.dataobj)[idx, :]

# Depth
depth = nb.load(DEPTH)
depth = np.asarray(depth.dataobj)[idx]

dirname = os.path.dirname(COORDS)
# -----------------------------------------------------------------------------
# Iso-distance lines
img_out = np.zeros(nii0.shape)
img_out[idx] = np.abs(coord_uv[:, 0]) + 1
out_path = os.path.join(dirname, "{}_UVmagnitudeU.nii.gz".format(OUT_NAME))
out = nb.Nifti1Image(img_out, header=nii0.header, affine=nii0.affine)
nb.save(out, out_path)

img_out = np.zeros(nii0.shape)
img_out[idx] = np.abs(coord_uv[:, 1]) + 1
out_path = os.path.join(dirname, "{}_UVmagnitudeV.nii.gz".format(OUT_NAME))
out = nb.Nifti1Image(img_out, header=nii0.header, affine=nii0.affine)
nb.save(out, out_path)
# -----------------------------------------------------------------------------
# Threshold based on euclidean norm
# coord_uv[norm > 0.7] = 0

# -----------------------------------------------------------------------------
# Determine flat grid range
range_min = np.floor(np.min(coord_uv))
range_max = np.ceil(np.max(coord_uv))

idx_roi = idx[idx]
qsteps = XY_BINS
qrange = np.linspace(range_min, range_max, qsteps+1)

# Depth stuff
zsteps = Z_LAYERS
zrange = np.linspace(0, 1, zsteps+1)
# Prep 3D images
cells = np.zeros(data.shape)
cell_density = np.zeros(data.shape)
cell_quadrant = np.zeros(data.shape)
# Prep 2D images
img_2D_data = np.zeros([qsteps, qsteps, zsteps])
img_2D_density = np.zeros(img_2D_data.shape)
img_2D_quadrant = np.zeros(img_2D_data.shape)

for z in range(0, zsteps):
    print("\rDoing depth {}/{}".format(z+1, zsteps))
    for i in range(0, qsteps):
        for j in range(0, qsteps):
            # Bin cells
            idx_cell = depth > zrange[z]
            idx_cell *= depth < zrange[z+1]
            idx_cell *= coord_uv[:, 0] > qrange[i]
            idx_cell *= coord_uv[:, 0] < qrange[i+1]
            idx_cell *= coord_uv[:, 1] > qrange[j]
            idx_cell *= coord_uv[:, 1] < qrange[j+1]
            # Cell density measure
            nr_cell_voxels = np.sum(idx_cell)
            # Cell calue
            if nr_cell_voxels > 0:
                val = np.mean(data[idx_cell])
            else:
                val = 0

            # Update UV images
            img_2D_data[i, j, z] = val
            img_2D_density[i, j, z] = nr_cell_voxels

            # Update 3D images
            cells[idx_cell] = qsteps * i + j
            cell_density[idx_cell] = nr_cell_voxels

# Save
img_out = np.zeros(nii0.shape)
img_out[idx] = cells
out_path = os.path.join(dirname, "{}_cells.nii.gz".format(OUT_NAME))
out = nb.Nifti1Image(img_out, header=nii0.header, affine=nii0.affine)
nb.save(out, out_path)

img_out[idx] = cell_density
out_path = os.path.join(dirname, "{}_density.nii.gz".format(OUT_NAME))
out = nb.Nifti1Image(img_out, header=nii0.header, affine=nii0.affine)
nb.save(out, out_path)

out_path = os.path.join(dirname, "{}_flat_data.nii.gz".format(OUT_NAME))
out = nb.Nifti1Image(img_2D_data, affine=np.eye(4))
nb.save(out, out_path)

out_path = os.path.join(dirname, "{}_flat_density.nii.gz".format(OUT_NAME))
out = nb.Nifti1Image(img_2D_density, affine=np.eye(4))
nb.save(out, out_path)

print("Finished.")
