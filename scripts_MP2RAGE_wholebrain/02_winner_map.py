"""Winner maps from tissue probabilities."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-1_Background.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-2_White_matter.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-3_Grey_matter.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-4_CSF_extra-cerebral.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-5_Ventricles_Lateral_5th.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-6_Subcortical_structures.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-7_Blood_vessels.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-8_Sagittal_sinus.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/02_segmentation"
OUT_NAME = "sub-01_ses-T2s_MP2RAGE_uni_segm"

# =============================================================================
print("Step_02: Create winner maps.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# -----------------------------------------------------------------------------
# Prepare
nii = nb.load(NII_NAMES[0])
dims = nii.shape
nr_files = len(NII_NAMES)

# Load probability maps
temp = np.zeros(dims + (nr_files,))
for i in range(nr_files):
    nii_temp = nb.load(NII_NAMES[i])
    temp[..., i] = nii_temp.get_fdata()

    # Tweaks
    if i == 1:  # WM
        temp[..., i] *= 2
    elif i == 3:  # CSF
        temp[..., i] *= 0.1


# Winner maps
winner = np.argmax(temp, axis=-1)
img = nb.Nifti1Image(winner, affine=nii.affine, header=nii.header)
nb.save(img, os.path.join(OUTDIR, '{}_winner.nii.gz'.format(OUT_NAME)))

# Brain mask
mask = np.zeros(dims)
for i in [1, 2, 3, 6, 7]:
    mask[winner == i] = 1
img = nb.Nifti1Image(mask, affine=nii.affine, header=nii.header)
nb.save(img, os.path.join(OUTDIR, '{}_brainmask.nii.gz'.format(OUT_NAME)))

# Rim file
rim = np.zeros(dims)
rim[winner == 1] = 2  # inner gm
rim[winner == 2] = 1  # pure gm
rim[winner == 3] = 3  # outer gm
rim[winner == 6] = 3  # outer gm
rim[winner == 7] = 3  # outer gm
img = nb.Nifti1Image(rim, affine=nii.affine, header=nii.header)
nb.save(img, os.path.join(OUTDIR, '{}_rim.nii.gz'.format(OUT_NAME)))

print('Finished.')
