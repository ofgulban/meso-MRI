"""Apply registration."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo1_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo2_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo3_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo4_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo5_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo6_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo1_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo2_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo3_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo4_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo5_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo6_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo1_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo2_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo3_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo4_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo5_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo6_ups2X.nii.gz',
    ]

AFFINES = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/04_motion_correct/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_avg_ups2X_affine.mat",
]

REFERENCE = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/03_upsample/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_avg_ups2X.nii.gz"

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/07_apply_reg"

# =============================================================================
print("Step_07: Apply registration to each echo.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i in range(0, len(NII_NAMES)):
    # -------------------------------------------------------------------------
    # Apply affine transformation matrix
    # -------------------------------------------------------------------------
    # Prepare inputs
    in_moving = NII_NAMES[i]
    affine = AFFINES[i]

    # Prepare output
    basename, ext = in_moving.split(os.extsep, 1)
    basename = os.path.basename(basename)
    print(basename)
    out_moving = os.path.join(OUTDIR, "{}_reg.nii.gz".format(basename))

    command = "greedy "
    command += "-d 3 "
    command += "-rf {} ".format(REFERENCE)  # reference
    command += "-ri LINEAR "  # No other better options than linear
    command += "-rm {} {} ".format(in_moving, out_moving)  # moving resliced
    command += "-r {} ".format(affine)

    # Execute command
    subprocess.run(command, shell=True)

print('\n\nFinished.')
