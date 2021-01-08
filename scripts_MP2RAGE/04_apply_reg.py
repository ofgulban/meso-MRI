"""Apply registration."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-02_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-03_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-04_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-05_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-06_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-02_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-03_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-04_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-05_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-06_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz",
    ]

AFFINES = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-02_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-03_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-04_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-05_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-06_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-02_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-03_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-04_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-05_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct/sub-01_ses-T1_run-06_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X_affine.mat",
]

REFERENCE = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-01_dir-AP_MP2RAGE_uni_crop_ups2X.nii.gz"

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/04_apply_reg"

# =============================================================================
print("MP2RAGE Step 04: Apply registration to UNI images.")

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
