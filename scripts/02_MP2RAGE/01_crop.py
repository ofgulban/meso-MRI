"""Reduce bounding box to decrease filesize."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-01_dir-AP_MP2RAGE_T1.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-02_dir-RL_MP2RAGE_T1.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-03_dir-PA_MP2RAGE_T1.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-04_dir-LR_MP2RAGE_T1.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-05_dir-AP_MP2RAGE_T1.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-06_dir-RL_MP2RAGE_T1.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-07_dir-PA_MP2RAGE_T1.nii.gz',
    '/home/faruk/data2/DATA_MRI_NIFTI/src/sub-05_ses-T1/MP2RAGE/sub-05_ses-T1_run-08_dir-LR_MP2RAGE_T1.nii.gz',
    ]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/01_crop"

# # subject 01
# RANGE_X = [100, 400]  # xmin xsize
# RANGE_Y = [60, 310]  # ymin ysize
# RANGE_Z = [10, -1]  # zmin, zsize

# # subject 02
# RANGE_X = [90, 380]  # xmin xsize
# RANGE_Y = [20, 360]  # ymin ysize
# RANGE_Z = [10, -1]  # zmin, zsize

# # subject 03
# RANGE_X = [100, 390]  # xmin xsize
# RANGE_Y = [40, 320]  # ymin ysize
# RANGE_Z = [10, -1]  # zmin, zsize

# # subject 04
# RANGE_X = [100, 390]  # xmin xsize
# RANGE_Y = [40, 340]  # ymin ysize
# RANGE_Z = [10, -1]  # zmin, zsize

# subject 05
RANGE_X = [100, 410]  # xmin xsize
RANGE_Y = [40, 300]  # ymin ysize
RANGE_Z = [10, -1]  # zmin, zsize

# =============================================================================
print("MP2RAGE Step 01: Crop region of interest.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i, f in enumerate(NII_NAMES):
    print("  Processing file {} ...".format(i+1))
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file = os.path.join(OUTDIR, "{}_crop.nii.gz".format(basename))

    # Prepare command
    command1 = "fslroi "
    command1 += "{} ".format(f)  # input
    command1 += "{} ".format(out_file)  # output
    command1 += "{} {} ".format(RANGE_X[0], RANGE_X[1])  # xmin xsize
    command1 += "{} {} ".format(RANGE_Y[0], RANGE_Y[1])  # ymin ysize
    command1 += "{} {} ".format(RANGE_Z[0], RANGE_Z[1])  # zmin zsize
    command1 += "0 -1 "  # tmin tsize
    # Execute command
    subprocess.run(command1, shell=True)

print('\n\nFinished.')
