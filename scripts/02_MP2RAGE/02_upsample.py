"""Upsample images."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-01_dir-AP_MP2RAGE_T1_crop.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-02_dir-RL_MP2RAGE_T1_crop.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-03_dir-PA_MP2RAGE_T1_crop.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-04_dir-LR_MP2RAGE_T1_crop.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-05_dir-AP_MP2RAGE_T1_crop.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-06_dir-RL_MP2RAGE_T1_crop.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-07_dir-PA_MP2RAGE_T1_crop.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_run-08_dir-LR_MP2RAGE_T1_crop.nii.gz',
    ]

# Create this file manually in ITK-SNAP (C chape centered at occipical)
MASK_FILE = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop/sub-05_ses-T1_regmask.nii.gz"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/02_upsample"

# =============================================================================
print("MP2RAGE Step 02: Upsample.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i, f in enumerate(NII_NAMES):
    print("  Processing file {}...".format(i+1))
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file = os.path.join(OUTDIR, "{}_ups2X.nii.gz".format(basename))

    # Prepare command
    command1 = "c3d {} ".format(f)
    command1 += "-interpolation Cubic "
    command1 += "-resample 200% "
    command1 += "-o {}".format(out_file)
    # Execute command
    subprocess.run(command1, shell=True)

# -----------------------------------------------------------------------------
# Also upsample registration mask
basename, ext = MASK_FILE.split(os.extsep, 1)
basename = os.path.basename(basename)
out_file = os.path.join(OUTDIR, "{}_ups2X.nii.gz".format(basename))

# Prepare command
print("  Processing mask file...")
command2 = "c3d {} ".format(MASK_FILE)
command2 += "-interpolation NearestNeighbor "
command2 += "-resample 200% "
command2 += "-o {}".format(out_file)
# Execute command
subprocess.run(command2, shell=True)

print('\n\nFinished.')
