"""Reduce bounding box to decrease filesize."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-02_ses-T2s/MP2RAGE_650micron/sub-02_ses-T2s_MP2RAGE_inv1.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-02_ses-T2s/MP2RAGE_650micron/sub-02_ses-T2s_MP2RAGE_inv2.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-02_ses-T2s/MP2RAGE_650micron/sub-02_ses-T2s_MP2RAGE_uni.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-02_ses-T2s/MP2RAGE_650micron/sub-02_ses-T2s_MP2RAGE_T1.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-02/T1_wholebrain/03_crop"

# Subject 01
RANGE_Z = [10, 200]  # xmin xsize
RANGE_X = [50, 230]  # ymin ysize
RANGE_Y = [90, 180]  # zmin zsize

# Subject 02
# RANGE_Z = [10, 200]  # xmin xsize
# RANGE_X = [40, 260]  # ymin ysize
# RANGE_Y = [120, 170]  # zmin zsize

# Subject 03
# RANGE_Z = [10, 200]  # xmin xsize
# RANGE_X = [40, 260]  # ymin ysize
# RANGE_Y = [120, 170]  # zmin zsize

# Subject 04
# RANGE_Z = [10, 200]  # xmin xsize
# RANGE_X = [40, 260]  # ymin ysize
# RANGE_Y = [120, 170]  # zmin zsize

# Subject 05
# RANGE_X = [40, 260]  # xmin xsize
# RANGE_Y = [120, 180]  # ymin ysize
# RANGE_Z = [10, 210]  # zmin zsize

# =============================================================================
print("Step_03: Crop region of interest.")

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
