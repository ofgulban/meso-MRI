"""B0 angle related stuff"""

import os
import numpy as np
import nibabel as nb

# Scalar file
FILE1 = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/99_B0_angles/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim.nii.gz"

# Vector file
FILE2 = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/99_B0_angles/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_streamline_vectors.nii.gz"

# =============================================================================
# Load nifti
nii1 = nb.load(FILE1)
data = np.asarray(nii1.dataobj)
idx = data != 0
dims = nii1.shape

# Affine
aff = nii1.affine
aff = np.linalg.inv(aff)

ref = np.array([[0, 0, 0], [0, 0, 1]])
new = nb.affines.apply_affine(aff, ref)
new = new[1, :] - new[0, :]
new /= np.linalg.norm(new)

# Prepare 4D nifti
vec_B0 = np.zeros(dims + (3,))
vec_B0[..., 0] = new[0]
vec_B0[..., 1] = new[1]
vec_B0[..., 2] = new[2]
vec_B0[~idx, :] = 0

# Save
basename, ext = FILE1.split(os.extsep, 1)
img = nb.Nifti1Image(vec_B0, affine=nii1.affine, header=nii1.header)
nb.save(img, "{}_B0vector.{}".format(basename, ext))

# -----------------------------------------------------------------------------
# Load vector nifti
nii2 = nb.load(FILE2)
vec_local = np.asarray(nii2.dataobj)

# Angular difference
term1 = np.sum(vec_B0 ** 2, axis=-1)
term2 = np.sum(vec_local ** 2, axis=-1)
temp_dot = np.sum(vec_B0 * vec_local, axis=-1)
temp_angle = np.arccos(temp_dot / np.sqrt(term1 * term2))
temp_angle = temp_angle * 180 / np.pi;
temp_angle[~idx] = 0
temp_angle[np.isnan(temp_angle)] = 0
temp_angle[idx] = 90 - np.abs(temp_angle[idx] - 90)

# Save
img = nb.Nifti1Image(temp_angle, affine=nii1.affine, header=nii1.header)
nb.save(img, "{}_B0angdif.{}".format(basename, ext))

print("Finished.")
