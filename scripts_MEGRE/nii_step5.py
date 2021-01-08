"""Monoexponential decay (T2star) fitting."""

import os
import nibabel as nb
import numpy as np
# from scipy.linalg import lstsq

# Parameters
NII_NAME = "/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/05_fit_t2star/sub-03_ses-01_RL_LR_flow_artifact_mitigated_avg.nii.gz"

TEs = np.array([3.83, 8.20, 12.57, 16.94, 21.31, 25.68])

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

np.max(betas[0])
np.min(betas[0])

np.max(betas[1])
np.min(betas[1])

T2_star = np.reciprocal(betas[0], where=betas[0] != 0)

T2_star = np.abs(T2_star)
T2_star[T2_star > 1000] = 1000

S0 = np.exp(betas[1])

# Reshape to image space
T2_star = T2_star.reshape((dims[0], dims[1], dims[2]))
S0 = S0.reshape((dims[0], dims[1], dims[2]))

# Save
basename = NII_NAME.split(os.extsep, 1)[0]
img = nb.Nifti1Image(T2_star, affine=nii.affine)
nb.save(img, "{}_T2star.nii.gz".format(basename))
img = nb.Nifti1Image(S0, affine=nii.affine)
nb.save(img, "{}_S0.nii.gz".format(basename))

print('Finished.')
