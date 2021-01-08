"""Split each echo to prepare for registration."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/01_crop/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/01_crop/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/01_crop/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/01_crop/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes"

# =============================================================================
print("Step_05: Split echoes.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# Average across echoes
for i, nii_name in enumerate(NII_NAMES):
    # Load data
    nii = nb.load(nii_name)
    temp = np.squeeze(np.asanyarray(nii.dataobj))

    # Save each echo separately
    basename, ext = nii.get_filename().split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_name = os.path.join(OUTDIR, basename)
    for j in range(temp.shape[-1]):
        echo = np.squeeze(temp[..., j])
        img = nb.Nifti1Image(echo, affine=nii.affine, header=nii.header)
        nb.save(img, '{}_echo{}.nii.gz'.format(out_name, j+1))

print('  Finished.')
