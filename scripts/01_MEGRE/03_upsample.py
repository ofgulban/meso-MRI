"""Upsample images."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/02_avg/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_avg.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/02_avg/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_avg.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/02_avg/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_avg.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/02_avg/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_avg.nii.gz',
    ]

# Create this file manually in ITK-SNAP (C chape centered at occipical)
MASK_FILE = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/02_avg/sub-23_ses-T2s_crop_regmask.nii.gz"

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/03_upsample"

# =============================================================================
print("Step_03: Upsample.")

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
