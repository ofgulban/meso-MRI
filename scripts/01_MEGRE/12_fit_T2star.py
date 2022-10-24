"""Monoexponential decay (T2star) fitting."""

import os
import nibabel as nb
import numpy as np
# from scipy.linalg import lstsq

# Parameters
NII_NAME = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/11_decayfix/sub-23_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed.nii.gz"

TEs = np.array([3.83, 8.20, 12.57, 16.94, 21.31, 25.68])

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/12_T2star"

# =============================================================================
print("Step_12: Fit T2*.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# =============================================================================
nii = nb.load(NII_NAME)
dims = nii.shape
nr_voxels = dims[0]*dims[1]*dims[2]

data = nii.get_fdata()
data = data.reshape((nr_voxels, dims[3]))

# Take logarithm
data = np.log(data, where=data > 0)

design = np.ones((dims[3], 2))
design[:, 0] *= -TEs

betas = np.linalg.lstsq(design, data.T, rcond=None)[0]
data = None

T2_star = np.reciprocal(betas[0], where=betas[0] != 0)

T2_star = np.abs(T2_star)
T2_star[T2_star > 100] = 100  # Max clipping

S0 = np.exp(betas[1])

# Reshape to image space
T2_star = T2_star.reshape((dims[0], dims[1], dims[2]))
S0 = S0.reshape((dims[0], dims[1], dims[2]))

# Save
basename, ext = NII_NAME.split(os.extsep, 1)
basename = os.path.basename(basename)
img = nb.Nifti1Image(T2_star, affine=nii.affine)
nb.save(img, os.path.join(OUTDIR, "{}_T2s.nii.gz".format(basename)))
img = nb.Nifti1Image(S0, affine=nii.affine)
nb.save(img, os.path.join(OUTDIR, "{}_S0.nii.gz".format(basename)))

print('Finished.')
