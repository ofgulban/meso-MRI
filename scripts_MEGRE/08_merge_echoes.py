"""Split each echo to prepare for registration."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo1_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo2_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo3_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo4_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo5_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo6_ups2X.nii.gz"
    ], [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo1_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo2_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo3_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo4_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo5_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo6_ups2X_reg.nii.gz"
    ], [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo1_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo2_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo3_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo4_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo5_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo6_ups2X_reg.nii.gz"
    ], [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo1_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo2_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo3_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo4_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo5_ups2X_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo6_ups2X_reg.nii.gz"
    ]
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/08_merge_echos"
OUT_NAMES = [
    "sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_ups2X_prepped.nii.gz",
    "sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_ups2X_prepped.nii.gz",
    "sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_ups2X_prepped.nii.gz",
    "sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_ups2X_prepped.nii.gz",
];

# =============================================================================
print("Step_08: Merge echoes.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# Average across echoes
dims = nb.load(NII_NAMES[0][0]).shape
for i in range(len(NII_NAMES)):
    print("Merging file {}...".format(i+1))
    temp = np.zeros(dims + (6,))
    for j in range(len(NII_NAMES[i])):
        # Load data
        nii = nb.load(NII_NAMES[i][j])
        temp[..., j] = np.squeeze(np.asanyarray(nii.dataobj))

    # Save echos as timeseries
    out_name = os.path.join(OUTDIR, OUT_NAMES[i])
    img = nb.Nifti1Image(temp, affine=nii.affine, header=nii.header)
    nb.save(img, out_name)

print('  Finished.')
