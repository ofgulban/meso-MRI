"""Average images."""

import os
import numpy as np
import nibabel as nb

NII_NAMES = [[
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-01_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-02_dir-AP_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-03_dir-AP_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-04_dir-AP_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-05_dir-AP_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-06_dir-AP_MP2RAGE_uni_crop_ups2X_reg.nii.gz",
    ], [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-01_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-02_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-03_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-04_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-05_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg/sub-01_ses-T1_run-06_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_reg.nii.gz",
    ]]

OUT_NAMES = [
    "sub-01_ses-T1_MP2RAGE_uni_crop_ups2X_avg",
    "sub-01_ses-T1_MP2RAGE_inv2_crop_ups2X_avg",
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/05_average"

# =============================================================================
print("MP2RAGE Step 05: Average.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# -----------------------------------------------------------------------------

for j in range(len(NII_NAMES)):
    # Load first file
    nii = nb.load(NII_NAMES[j][0])
    data = np.squeeze(nii.get_fdata())
    for i in range(1, len(NII_NAMES[j])):
        nii = nb.load(NII_NAMES[j][i])
        data += np.squeeze(nii.get_fdata())
    data /= len(NII_NAMES)

    # Save
    img = nb.Nifti1Image(data, affine=nii.affine)
    nb.save(img, os.path.join(OUTDIR, "{}.nii.gz".format(OUT_NAMES[j])))

print('Finished.')
