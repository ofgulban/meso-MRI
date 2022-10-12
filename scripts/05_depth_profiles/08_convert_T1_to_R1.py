"""Convert T1 in miliseconds to R1 in 1/seconds."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

INPUTS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T1/07_register_to_T2s/sub-01_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/T1/07_register_to_T2s/sub-02_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-03/T1/07_register_to_T2s/sub-03_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/T1/07_register_to_T2s/sub-04_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/07_register_to_T2s/sub-05_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz"
    ]

MAX = 1.2

# -----------------------------------------------------------------------------
for i in INPUTS:
    nii = nb.load(i)
    data = nii.get_fdata()
    data_new = np.reciprocal(data / 1000, where=data!=0, dtype=np.float32)

    # Clip extremes
    data_new[data_new > MAX] = MAX

    # Save
    basename = i.split(os.extsep, 1)[0]
    outname = "{}_R1_inOneDivSec.nii.gz".format(basename)
    out = nb.Nifti1Image(data_new, header=nii.header, affine=nii.affine)
    nb.save(out, outname)

print('Finished.\n')
