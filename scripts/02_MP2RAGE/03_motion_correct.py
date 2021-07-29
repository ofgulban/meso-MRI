"""Register each run to one reference run, computed once on INV2 images."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-01_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-02_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-03_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-04_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-05_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_run-06_dir-AP_part-mag_MP2RAGE_inv2_crop_ups2X.nii.gz',
    ]

# Create this file manually in ITK-SNAP (C chape centered at occipical)
MASK_FILE = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/02_upsample/sub-01_ses-T1_regmask_ups2X.nii.gz"

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/03_motion_correct"

# =============================================================================
print("MP2RAGE Step 03: Register average echoes (motion correction).")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i in range(1, len(NII_NAMES)):
    # -------------------------------------------------------------------------
    # Compute affine transformation matrix
    # -------------------------------------------------------------------------
    # Prepare inputs
    in_fixed = NII_NAMES[0]  # Keep target image constant
    in_moving = NII_NAMES[i]
    in_mask = MASK_FILE

    # Prepare output
    basename, ext = in_moving.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_affine = os.path.join(OUTDIR, "{}_affine.mat".format(basename))

    # Prepare command
    command1 = "greedy "
    command1 += "-d 3 "
    command1 += "-a -dof 6 "  # 6=rigid, 12=affine
    command1 += "-m NCC 2x2x2 "
    command1 += "-i {} {} ".format(in_fixed, in_moving)  # fixed moving
    command1 += "-o {} ".format(out_affine)
    command1 += "-ia-image-centers "
    command1 += "-n 100x50x10 "
    command1 += "-mm {} ".format(in_mask)
    command1 += "-float "

    # Execute command
    subprocess.run(command1, shell=True)

    # -------------------------------------------------------------------------
    # Apply affine transformation matrix
    # -------------------------------------------------------------------------
    # Prepare output
    basename, ext = in_moving.split(os.extsep, 1)
    basename = os.path.basename(basename)
    print(basename)
    out_moving = os.path.join(OUTDIR, "{}_reg.nii.gz".format(basename))

    command2 = "greedy "
    command2 += "-d 3 "
    command2 += "-rf {} ".format(in_fixed)  # reference
    command2 += "-ri LINEAR "
    command2 += "-rm {} {} ".format(in_moving, out_moving)  # moving resliced
    command2 += "-r {} ".format(out_affine)

    print(command2)

    # Execute command
    subprocess.run(command2, shell=True)

print('\n\nFinished.')
