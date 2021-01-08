"""Detect voxels that does not decay over time."""

import os
import nibabel as nb
import numpy as np

# Parameters
NII_NAME = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/10_composite/sub-23_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite.nii.gz"

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/11_decayfix"

# =============================================================================
print("Step_11: Detect and fix non-decaying timepoints.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# =============================================================================

nii = nb.load(NII_NAME)
dims = nii.shape
data = nii.get_fdata()

data = np.abs(data)
idx = data != 0
data[idx] = np.log(data[idx])

# 1-neighbour fix
temp1 = np.zeros(dims[:-1])
for i in range(dims[3] - 1):
    temp2 = data[..., i] - data[..., i+1]
    idx = temp2 < 0
    if (i > 0) and (i < dims[3] - 1):
        data[idx, i] = (data[idx, i-1] + data[idx, i+1]) / 2
    else:
        temp1[idx] = 1

# Save
basename, ext = NII_NAME.split(os.extsep, 1)
basename = os.path.basename(basename)
img = nb.Nifti1Image(temp1, affine=nii.affine)
nb.save(img, os.path.join(OUTDIR, "{}_decaymask.nii.gz".format(basename)))
data = np.exp(data)
img = nb.Nifti1Image(data, affine=nii.affine)
nb.save(img, os.path.join(OUTDIR, "{}_decayfixed.nii.gz".format(basename)))

print('Finished.')
