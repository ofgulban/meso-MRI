"""Register Lusebrink images to their 0.25 mm iso T1w data.

I have used ITKSNAP v3.8.0 registration menu with a C shaped segmentation mask
around the outer edges of the occipical cortex to compute the transformation
matrix.
"""

import os
import subprocess

TARGET = "/home/faruk/data2/DATA_MRI_NIFTI/data-lusebrink/derived/derivatives_sub-yv98_250um_averages_sub-yv98_ses-3512+3555+3589+3637+3681_offline_reconstruction_denoised-BM4D-manual_T1w_biasCorrected_crop_ups2X.nii.gz"
MOVING = "/home/faruk/data2/DATA_MRI_NIFTI/data-lusebrink/source/sub-yv98_ses-3943_anat_sub-yv98_ses-3943_ToF.nii.gz"
AFFINE = "/home/faruk/data2/DATA_MRI_NIFTI/data-lusebrink/derived/sub-yv97_TOF150um_to_T1w_v01.txt"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/data-lusebrink/derived/"

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
