"""Split odd and even echoes."""

import os
import numpy as np
import nibabel as nb

# =============================================================================

NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-04_ses-T2s/MEGRE/sub-04_ses-T2s_run-01_dir-AP_part-mag_MEGRE.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-04_ses-T2s/MEGRE/sub-04_ses-T2s_run-02_dir-RL_part-mag_MEGRE.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-04_ses-T2s/MEGRE/sub-04_ses-T2s_run-03_dir-PA_part-mag_MEGRE.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-04_ses-T2s/MEGRE/sub-04_ses-T2s_run-04_dir-LR_part-mag_MEGRE.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-04/01_odd_even"

# =============================================================================
# Check output dir
if os.path.exists(OUTDIR):
    print("Output directory already exists: \n{}".format(OUTDIR))
else:
    os.makedirs(OUTDIR)
    print("Output directory created: {}".format(OUTDIR))

# Split odd-even echoes
for i, nii_name in enumerate(NII_NAMES):
    # Load data
    nii = nb.load(nii_name)
    temp = np.squeeze(np.asanyarray(nii.dataobj))

    # Save
    basename, ext = nii.get_filename().split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_name = os.path.join(OUTDIR, basename)
    # Odd
    img = nb.Nifti1Image(temp[..., 0::2], affine=nii.affine, header=nii.header)
    nb.save(img, '{}_TE_1_3_5.{}'.format(out_name, ext))
    # Even
    img = nb.Nifti1Image(temp[..., 1::2], affine=nii.affine, header=nii.header)
    nb.save(img, '{}_TE_2_4_6.{}'.format(out_name, ext))

print('Finished.')
