"""Register Neurosynth motion map to individual subjects.

I have used ITKSNAP v3.8.0 registration menu. Automatic option and mask based
options mostly failed or perfomed suboptimally. I have used corpus callosum to
guide my intial manual alignment. Then I have matched heschl's gyri with manual
alignment. Then I have matched the cerebellum with manual alignment. I have
also used mild scaling factors (+0.1 to 0.25 range in x, y, z) to approximately
match the convex hull of the brain.

As the meta analysis activation is not too precise, such alignment is good
enough to justify the hMT vicinity. I will use these transformed maps to
determine the segmentation ball.

NOTE: Manual registration was absolutely necessary because the automatic
methods completely failed. This is due to the contrast differences between the
MNI template and my data, as well as due to the partial coverage. A more
automatic MNI registration might have worked with using whole brain reference
data but such increased precision is not needed anyway.

"""

import os
import subprocess

TARGET = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz"
MOVING = "/home/faruk/data2/DATA_MRI_NIFTI/data-neurosynth/motion_association-test_z_FDR_0pt01.nii.gz"
AFFINE = "/home/faruk/data2/DATA_MRI_NIFTI/data-neurosynth/reg_to_sub-05.txt"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/data-neurosynth"
SUFFIX = "reg_to_sub-05"

# -------------------------------------------------------------------------
# Apply affine transformation matrix
# -------------------------------------------------------------------------
# Prepare output
basename, ext = MOVING.split(os.extsep, 1)
basename = os.path.basename(basename)
print(basename)
out_moving = os.path.join(OUTDIR, "{}_{}.nii.gz".format(basename, SUFFIX))

command2 = "greedy "
command2 += "-d 3 "
command2 += "-rf {} ".format(TARGET)  # reference
command2 += "-ri LINEAR "
command2 += "-rm {} {} ".format(MOVING, out_moving)  # moving resliced
command2 += "-r {} ".format(AFFINE)

# Execute command
subprocess.run(command2, shell=True)

print(command2)
