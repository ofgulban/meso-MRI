"""Register Federau images to their 0.25 mm iso MP2RAGE UNI (T1w) data.

I have used ITKSNAP v3.8.0 registration menu with a C shaped segmentation mask
around the outer edges of the occipical cortex to compute the transformation
matrix. I have used "affine" option.
"""

import os
import subprocess

TARGET = "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/derived/sub-federau2016_MP2RAGE350_crop_ups2X.nii.gz"
MOVING = "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/source/sub-federau2016_GRE380_flipX.nii.gz"
AFFINE = "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/derived/sub-federau2016_GRE_to_UNI_v01.txt"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/derived"

# -------------------------------------------------------------------------
# Apply affine transformation matrix
# -------------------------------------------------------------------------
# Prepare output
basename, ext = MOVING.split(os.extsep, 1)
basename = os.path.basename(basename)
print(basename)
out_moving = os.path.join(OUTDIR, "{}_reg.nii.gz".format(basename))

command2 = "greedy "
command2 += "-d 3 "
command2 += "-rf {} ".format(TARGET)  # reference
command2 += "-ri LINEAR "
command2 += "-rm {} {} ".format(MOVING, out_moving)  # moving resliced
command2 += "-r {} ".format(AFFINE)

# Execute command
subprocess.run(command2, shell=True)

print(command2)
