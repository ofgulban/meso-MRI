"""Average images."""

import os
import numpy as np
import nibabel as nb

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/05_average"

NII_NAMES = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/02_upsample/sub-05_ses-T1_run-01_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-02_dir-RL_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-03_dir-PA_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-04_dir-LR_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-05_dir-AP_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-06_dir-RL_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-07_dir-PA_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-08_dir-LR_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    ]

OUT_NAME = "sub-05_ses-T1_MP2RAGE_uni_crop_ups2X_avg"

# -----------------------------------------------------------------------------

# NII_NAMES = [
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/02_upsample/sub-05_ses-T1_run-01_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz",
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-02_dir-RL_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-03_dir-PA_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-04_dir-LR_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-05_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-06_dir-RL_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-07_dir-PA_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
#     "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/04_apply_reg/sub-05_ses-T1_run-08_dir-LR_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
#     ]
#
# OUT_NAME = "sub-05_ses-T1_MP2RAGE_inv2_crop_ups2X_avg"

# =============================================================================
print("MP2RAGE Step 05: Average.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# -----------------------------------------------------------------------------

# Load first file
nii = nb.load(NII_NAMES[0])
data = np.squeeze(nii.get_fdata()) * 0
for i in NII_NAMES:
    nii = nb.load(i)
    data += np.squeeze(nii.get_fdata())
print("  Nr nifti files:{}".format(len(NII_NAMES)))
data /= len(NII_NAMES)

# Save
img = nb.Nifti1Image(data, affine=nii.affine, header=nii.header)
nb.save(img, os.path.join(OUTDIR, "{}.nii.gz".format(OUT_NAME)))

print('Finished.')
