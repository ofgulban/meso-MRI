"""Average runs with same phase encoding axis."""

import os
import numpy as np
import nibabel as nb

NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/08_merge_echos/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_ups2X_prepped.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/08_merge_echos/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_ups2X_prepped.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/09_average"
OUT_NAME = "sub-23_ses-T2s_dir-Mx_part-mag_MEGRE_crop_ups2X_prepped_avg"

# NII_NAMES = [
#     '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/08_merge_echos/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_ups2X_prepped.nii.gz',
#     '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/08_merge_echos/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_ups2X_prepped.nii.gz',
#     ]
#
# OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/09_average"
# OUT_NAME = "sub-23_ses-T2s_dir-My_part-mag_MEGRE_crop_ups2X_prepped_avg"

# =============================================================================
print("Step_09: Average.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))
# =============================================================================

# Load first file
nii = nb.load(NII_NAMES[0])
data = np.squeeze(nii.get_fdata())
for i in range(1, len(NII_NAMES)):
    nii = nb.load(NII_NAMES[i])
    data += np.squeeze(nii.get_fdata())
data /= len(NII_NAMES)

# Save
img = nb.Nifti1Image(data, affine=nii.affine)
nb.save(img, os.path.join(OUTDIR, "{}.nii.gz".format(OUT_NAME)))

print('Finished.')
