"""Combine for flow artifact mitigated average (composite) image."""

import os
import numpy as np
import nibabel as nb

NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/09_average/sub-23_ses-T2s_dir-Mx_part-mag_MEGRE_crop_ups2X_prepped_avg.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/09_average/sub-23_ses-T2s_dir-My_part-mag_MEGRE_crop_ups2X_prepped_avg.nii.gz'
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/10_composite"
OUT_NAME = "sub-23_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite"

# =============================================================================
print("Step_10: Composite.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# Load data
nii1 = nb.load(NII_NAMES[0])
nii2 = nb.load(NII_NAMES[1])
data1 = np.squeeze(nii1.get_fdata())
data2 = np.squeeze(nii2.get_fdata())

# -----------------------------------------------------------------------------
# Compositing
diff = data1 - data2

idx_neg = diff < 0
idx_pos = diff > 0

data1[idx_pos] -= diff[idx_pos]
data2[idx_neg] += diff[idx_neg]

# Average
data1 += data2
data1 /= 2.
# -----------------------------------------------------------------------------

# Save
out_name = nii1.get_filename().split(os.extsep, 1)[0]
img = nb.Nifti1Image(data1, affine=nii1.affine)
nb.save(img, os.path.join(OUTDIR, "{}.nii.gz".format(OUT_NAME)))

print('Finished.')
