"""Separate scoops of interest (SOI)."""

import os
import nibabel as nb
import numpy as np

SOI = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation_reg_to_T2s/sub-05_ses-T2s_MP2RAGE_uni_SOI.nii.gz"
RIM = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation_reg_to_T2s/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim.nii.gz"

TAGS = ["HG_RH", "HG_LH", "CS_RH", "CS_LH"]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns"

# -----------------------------------------------------------------------------
# Load data
nii_SOI = nb.load(SOI)
data_SOI = np.asarray(nii_SOI.dataobj)

nii_RIM = nb.load(RIM)
data_RIM = np.asarray(nii_RIM.dataobj)

# Separate tissues
filename = os.path.basename(RIM)
basename, ext = filename.split(os.extsep, 1)
for i, j in enumerate([1, 2, 3, 4]):

    # Binarize SOI
    idx = data_SOI == j
    temp = np.copy(data_SOI)
    temp[idx] = 1
    temp[~idx] = 0

    # Mask rim
    temp = temp * data_RIM
    temp = temp.astype("int")

    # Output directory
    out_target = os.path.join(OUTDIR, TAGS[i])
    if not os.path.exists(out_target):
        os.makedirs(out_target)
        print("  Output directory: {}".format(out_target))

    # Save as nifti
    out = nb.Nifti1Image(temp, header=nii_RIM.header, affine=nii_RIM.affine)
    out_name = "{}_{}.{}".format(os.path.join(out_target, basename), TAGS[i], ext)
    nb.save(out, out_name)

print('Finished.')
