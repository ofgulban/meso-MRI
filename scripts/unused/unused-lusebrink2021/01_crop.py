"""Reduce bounding box to decrease filesize."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    "/home/faruk/gdrive/paper-350_micron/data-lusebrink2021/derivatives_sub-yv98_250um_averages_sub-yv98_ses-3512+3555+3589+3637+3681_offline_reconstruction_denoised-BM4D-manual_T1w_biasCorrected.nii.gz"
    ]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/data-lusebrink2021/derived"

# sub=yv98_250um_t1w
RANGE_X = [42, 590-42]  # xmin xsize
RANGE_Y = [50, 572-50]  # ymin ysize
RANGE_Z = [350, 590-350]  # zmin, zsize

# =============================================================================
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
