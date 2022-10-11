"""Encode nifti axes to conveniently identifying flat orientations later."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

REF = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned.nii.gz"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/11_encode_directions"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# Determine output basename
filename = os.path.basename(REF)
basename, ext = filename.split(os.extsep, 1)

# Load reference
nii = nb.load(REF)
dims = nii.shape

# -----------------------------------------------------------------------------
# Encode R-L direction
data = np.zeros(dims, dtype=np.int32)
temp = np.arange(0, dims[0], dtype=np.int32)
for i in range(dims[1]):
    for j in range(dims[2]):
        data[:, i, j] = temp

# Save
outname = os.path.join(OUTDIR, "{}_RL.{}".format(basename, ext))
out = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(out, outname)

# -----------------------------------------------------------------------------
# Encode P-A direction
data = np.zeros(dims, dtype=np.int32)
temp = np.arange(0, dims[1], dtype=np.int32)
for i in range(dims[0]):
    for j in range(dims[2]):
        data[i, :, j] = temp

# Save
outname = os.path.join(OUTDIR, "{}_PA.{}".format(basename, ext))
out = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(out, outname)


# -----------------------------------------------------------------------------
# Encode I-S, direction
data = np.zeros(dims, dtype=np.int32)
temp = np.arange(0, dims[2], dtype=np.int32)
for i in range(dims[0]):
    for j in range(dims[1]):
        data[i, j, :] = temp

# Save
outname = os.path.join(OUTDIR, "{}_IS.{}".format(basename, ext))
out = nb.Nifti1Image(data, affine=np.eye(4))
nb.save(out, outname)

print('Finished.\n')
