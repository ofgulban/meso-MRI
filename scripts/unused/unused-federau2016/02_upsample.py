"""Upsample images."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/derived/sub-federau2016_MP2RAGE350_crop.nii.gz",
    ]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/derived/"

# =============================================================================
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

print('\n\nFinished.')
