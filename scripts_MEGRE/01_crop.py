"""Reduce bounding box to decrease filesize."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-23_ses-T2s/MEGRE/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-23_ses-T2s/MEGRE/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-23_ses-T2s/MEGRE/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-23_ses-T2s/MEGRE/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/01_crop"

# # sub-01
# RANGE_X = [90, 400]  # xmin xsize
# RANGE_Y = [50, 300]  # ymin ysize
# RANGE_Z = [0, -1]  # zmin zsize

# # sub-02
# RANGE_X = [100, 380]  # xmin xsize
# RANGE_Y = [10, 360]  # ymin ysize
# RANGE_Z = [0, -1]  # zmin zsize

# # sub-03
# RANGE_X = [90, 390]  # xmin xsize
# RANGE_Y = [40, 310]  # ymin ysize
# RANGE_Z = [0, -1]  # zmin zsize

# # sub-04
# RANGE_X = [100, 390]  # xmin xsize
# RANGE_Y = [20, 300]  # ymin ysize
# RANGE_Z = [0, -1]  # zmin zsize

# # sub-05
# RANGE_X = [80, 410]  # xmin xsize
# RANGE_Y = [40, 300]  # ymin ysize
# RANGE_Z = [0, -1]  # zmin zsize

# sub-23
RANGE_X = [90, 410]  # xmin xsize
RANGE_Y = [50, 440]  # ymin ysize
RANGE_Z = [0, -1]  # zmin zsize

# =============================================================================
print("Step_01: Crop region of interest.")

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
    command1 += "{} {} ".format(RANGE_Z[0], RANGE_Z[1])  # ymin ysize
    command1 += "0 -1 "  # tmin tsize
    # Execute command
    subprocess.run(command1, shell=True)

print('\n\nFinished.')
