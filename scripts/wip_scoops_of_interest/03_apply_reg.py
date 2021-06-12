"""Register each run to one reference run."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/00_resample_to_pt7/sub-01_ses-T2s_MP2RAGE_inv2_pt7_reframed.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/00_resample_to_pt7/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed.nii.gz',
    ]

NII_TARGET = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T2s/12_T2star/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_S0.nii.gz"

# NOTE: Use ITK-SNAP manually to find the best registration
# 1. Might require a few iterations at 2x to 1x levels
# 2. Might require using the brain edge mask to improve registration.
AFFINE = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/03_register_to_T1reg/sub-01_ses-T2s_wholebrain_to_T1reg.mat"

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/03_register_to_T1reg"

# =============================================================================
print("Step_03: Apply registration from wholebrain to T2s registered T1")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# -------------------------------------------------------------------------
# Apply affine transformation matrix
# -------------------------------------------------------------------------
for i in range(0, len(NII_NAMES)):
    # Prepare inputs
    in_moving = NII_NAMES[i]
    in_affine = AFFINE

    # Prepare output
    basename, ext = in_moving.split(os.extsep, 1)
    basename = os.path.basename(basename)
    print(basename)
    out_moving = os.path.join(OUTDIR, "{}_reg.nii.gz".format(basename))

    command2 = "greedy "
    command2 += "-d 3 "
    command2 += "-rf {} ".format(NII_TARGET)  # reference
    command2 += "-ri LINEAR "
    command2 += "-rm {} {} ".format(in_moving, out_moving)  # moving resliced
    command2 += "-r {} ".format(in_affine)
    print(command2)

    # Execute command
    subprocess.run(command2, shell=True)

    # Substitude header with target nifti
    nii_target = nb.load(NII_TARGET)
    nii_moving = nb.load(out_moving)
    nii_out = nb.Nifti1Image(nii_moving.get_fdata(), header=nii_target.header,
                             affine=nii_target.affine)
    nb.save(nii_out, out_moving)

print('\n\nFinished.')
